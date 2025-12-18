from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.clinicians.schemas import (
    ClinicianProfile,
    ClinicianDashboard,
)
from app.clinicians.service import ClinicianService

router = APIRouter()


def get_clinician_service() -> ClinicianService:
    return ClinicianService()


def _ensure_clinician(request: Request) -> str:
    """Get clinician_id from JWT context and ensure role is clinician."""
    user_id = getattr(request.state, "user_id", None)
    role = getattr(request.state, "role", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    if role != "clinician":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinician access required",
        )

    # In your schema, clinician_id == auth user_id
    return user_id


@router.get("/me", response_model=ClinicianProfile)
async def get_my_profile(
    request: Request,
    service: ClinicianService = Depends(get_clinician_service),
) -> ClinicianProfile:
    clinician_id = _ensure_clinician(request)
    try:
        return service.get_clinician_profile(clinician_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get("/me/dashboard", response_model=ClinicianDashboard)
async def get_my_dashboard(
    request: Request,
    service: ClinicianService = Depends(get_clinician_service),
) -> ClinicianDashboard:
    clinician_id = _ensure_clinician(request)
    return service.get_dashboard(clinician_id)
