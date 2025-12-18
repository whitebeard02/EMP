from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.schemas import (
    InviteClinicianRequest,
    InvitePatientRequest,
    InviteResponse,
)
from app.auth.service import AuthService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/admin/invite-clinician", response_model=InviteResponse)
async def invite_clinician(
    payload: InviteClinicianRequest,
    service: AuthService = Depends(get_auth_service),
) -> InviteResponse:
    try:
        return service.invite_clinician(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invite clinician: {exc}",
        )


@router.post("/admin/invite-patient", response_model=InviteResponse)
async def invite_patient(
    payload: InvitePatientRequest,
    service: AuthService = Depends(get_auth_service),
) -> InviteResponse:
    try:
        return service.invite_patient(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to invite patient: {exc}",
        )
