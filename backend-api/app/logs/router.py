from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List

from app.logs.schemas import LogCreate, LogRead
from app.logs.service import LogsService
from app.patients.service import PatientService  # reuse to check mappings

router = APIRouter()


def get_logs_service() -> LogsService:
    return LogsService()


def get_patient_service() -> PatientService:
    return PatientService()


def _require_auth(request: Request) -> tuple[str, str]:
    user_id = getattr(request.state, "user_id", None)
    role = getattr(request.state, "role", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    if role not in ("patient", "clinician"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient or clinician access required",
        )
    return user_id, role


@router.post("/me", response_model=LogRead)
async def create_my_log(
    request: Request,
    payload: LogCreate,
    logs_service: LogsService = Depends(get_logs_service),
) -> LogRead:
    user_id, role = _require_auth(request)
    if role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can create their own logs",
        )

    # For patients, find their patient_id via patient_accounts
    patient_id = logs_service.get_patient_id_for_user(user_id)
    return logs_service.create_log_for_patient(patient_id, payload)


@router.get("/me", response_model=List[LogRead])
async def list_my_logs(
    request: Request,
    logs_service: LogsService = Depends(get_logs_service),
) -> List[LogRead]:
    user_id, role = _require_auth(request)
    if role != "patient":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients can read their own logs",
        )

    patient_id = logs_service.get_patient_id_for_user(user_id)
    return logs_service.list_logs_for_patient(patient_id)


@router.get("/patient/{patient_id}", response_model=List[LogRead])
async def list_logs_for_patient(
    patient_id: str,
    request: Request,
    logs_service: LogsService = Depends(get_logs_service),
    patient_service: PatientService = Depends(get_patient_service),
) -> List[LogRead]:
    user_id, role = _require_auth(request)
    if role != "clinician":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clinician access required",
        )

    # Optional: ensure this patient is assigned to this clinician
    # by checking patients.primary_clinician_id
    patient = patient_service.get_patient_profile(patient_id)
    if patient.primary_clinician_id and patient.primary_clinician_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the primary clinician for this patient",
        )

    return logs_service.list_logs_for_patient(patient_id)
