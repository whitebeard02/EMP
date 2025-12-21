from typing import List

from supabase import Client

from app.config import get_supabase_admin_client
from app.logs.schemas import LogCreate, LogRead


class LogsService:
    def __init__(self, admin_client: Client | None = None) -> None:
        self.admin = admin_client or get_supabase_admin_client()

    # Helper: get patient_id from an auth user_id (patient)
    def get_patient_id_for_user(self, user_id: str) -> str:
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

    def create_log_for_patient(self, patient_id: str, payload: LogCreate) -> LogRead:
        data = {
            "patient_id": patient_id,
            "date": payload.date.isoformat() if payload.date else "now()",
            # ML Data
            "hours_of_sleep": payload.hours_of_sleep,
            "stress_level": payload.stress_level,
            "medication_taken": payload.medication_taken,
            "seizure_occurred": payload.seizure_occurred,
            # UI Data
            "mood": payload.mood,
            "notes": payload.notes,
        }
        # CHANGED: Table name is now 'patient_logs'
        resp = self.admin.table("patient_logs").insert(data).execute()
        if not resp.data:
            raise RuntimeError("Failed to create log")
        return LogRead(**resp.data[0])

    def list_logs_for_patient(self, patient_id: str) -> List[LogRead]:
        resp = (
            self.admin.table("patient_logs") # CHANGED: Table name
            .select("*") # Select all columns
            .eq("patient_id", patient_id)
            .order("date", desc=True) # CHANGED: Sort by 'date'
            .execute()
        )
        rows = resp.data or []
        return [LogRead(**row) for row in rows]
