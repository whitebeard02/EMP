from typing import List

from supabase import Client

from app.config import get_supabase_admin_client
from app.clinicians.schemas import (
    ClinicianProfile,
    PatientSummary,
    ClinicianDashboard,
)


class ClinicianService:
    def __init__(self, admin_client: Client | None = None) -> None:
        self.admin = admin_client or get_supabase_admin_client()

    def get_clinician_profile(self, clinician_id: str) -> ClinicianProfile:
        """Fetch clinician row by clinician_id."""
        resp = (
            self.admin.table("clinicians")
            .select("clinician_id, email, full_name, specialty, is_active")
            .eq("clinician_id", clinician_id)
            .single()
            .execute()
        )

        if not resp.data:
            raise ValueError("Clinician not found")

        return ClinicianProfile(**resp.data)

    def get_clinician_patients(self, clinician_id: str) -> List[PatientSummary]:
        """
        Fetch patients assigned to this clinician.
        Assumes patients table has primary_clinician_id FK.
        """
        resp = (
            self.admin.table("patients")
            .select("patient_id, has_logs")
            .eq("primary_clinician_id", clinician_id)
            .execute()
        )

        data = resp.data or []
        return [PatientSummary(**row) for row in data]

    def get_dashboard(self, clinician_id: str) -> ClinicianDashboard:
        clinician = self.get_clinician_profile(clinician_id)
        patients = self.get_clinician_patients(clinician_id)
        return ClinicianDashboard(clinician=clinician, patients=patients)
