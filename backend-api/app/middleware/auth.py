from typing import Optional

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_supabase_client


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    Validates Supabase JWT from Authorization header.
    On success, sets:
      request.state.user_id  (string)
      request.state.role     (string, from app_metadata.role)
    """

    def __init__(self, app, public_paths: Optional[list[str]] = None) -> None:
        super().__init__(app)
        self.public_paths = public_paths or [
            "/",          # root
            "/health",    # health check
            "/docs",
            "/openapi.json",
            "/redoc",
        ]
        self.supabase = get_supabase_client()

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Allow public paths without auth
        if any(path == p or path.startswith(p + "/") for p in self.public_paths):
            return await call_next(request)

        # Read Authorization header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
            )

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Empty bearer token",
            )

        # Validate token with Supabase
        try:
            user_resp = self.supabase.auth.get_user(token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = getattr(user_resp, "user", None)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found for token",
            )

        # Attach to request.state
        request.state.user_id = str(user.id)
        # app_metadata is where we stored the role during invite
        role = None
        if hasattr(user, "app_metadata") and isinstance(user.app_metadata, dict):
            role = user.app_metadata.get("role")

        request.state.role = role

        # Continue request
        response = await call_next(request)
        return response
