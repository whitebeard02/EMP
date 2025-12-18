from pydantic import BaseModel, EmailStr


class InviteClinicianRequest(BaseModel):
    email: EmailStr
    full_name: str
    specialty: str | None = None


class InvitePatientRequest(BaseModel):
    email: EmailStr
    full_name: str | None = None
    phone: str | None = None


class InviteResponse(BaseModel):
    user_id: str
    email: EmailStr
    role: str
