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
            "seizure_occurred": payload.seizure_occurred,
            "mood": payload.mood,
            "notes": payload.notes,
        }
        resp = self.admin.table("logs").insert(data).execute()
        if not resp.data:
            raise RuntimeError("Failed to create log")
        return LogRead(**resp.data[0])

    def list_logs_for_patient(self, patient_id: str) -> List[LogRead]:
        resp = (
            self.admin.table("logs")
            .select(
                "log_id, patient_id, created_at, seizure_occurred, mood, notes"
            )
            .eq("patient_id", patient_id)
            .order("created_at", desc=True)
            .execute()
        )
        rows = resp.data or []
        return [LogRead(**row) for row in rows]
