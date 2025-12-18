from supabase import Client

from app.config import get_supabase_admin_client
from app.patients.schemas import PatientProfile


class PatientService:
    def __init__(self, admin_client: Client | None = None) -> None:
        self.admin = admin_client or get_supabase_admin_client()

    def get_patient_id_for_user(self, user_id: str) -> str:
        """
        Look up patient_id in patient_accounts for this auth user.
        """
        resp = (
            self.admin.table("patient_accounts")
            .select("patient_id")
            .eq("user_id", user_id)
            .single()
            .execute()
        )

        if not resp.data:
            raise ValueError("No patient account linked to this user")

        return resp.data["patient_id"]

    def get_patient_profile(self, patient_id: str) -> PatientProfile:
        """
        Fetch patient row by patient_id.
        """
        resp = (
            self.admin.table("patients")
            .select("patient_id, assigned_model_id, primary_clinician_id")
            .eq("patient_id", patient_id)
            .single()
            .execute()
        )

        if not resp.data:
            raise ValueError("Patient not found")

        return PatientProfile(**resp.data)
