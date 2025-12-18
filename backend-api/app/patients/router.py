from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.patients.schemas import PatientMeResponse
from app.patients.service import PatientService

router = APIRouter()


def get_patient_service() -> PatientService:
    return PatientService()


def _ensure_patient(request: Request) -> tuple[str, str]:
    """
    Ensure the caller is authenticated and role == 'patient'.
    Returns (user_id, role).
    """
    user_id = getattr(request.state, "user_id", None)
    role = getattr(request.state, "role", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    if role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient access required",
        )

    return user_id, role


@router.get("/me", response_model=PatientMeResponse)
async def get_my_patient_profile(
    request: Request,
    service: PatientService = Depends(get_patient_service),
) -> PatientMeResponse:
    user_id, role = _ensure_patient(request)

    try:
        patient_id = service.get_patient_id_for_user(user_id)
        patient = service.get_patient_profile(patient_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return PatientMeResponse(
        user_id=user_id,
        role=role,
        patient=patient,
    )
