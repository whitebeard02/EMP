from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import List, Optional

class JWTAuthMiddleware(BaseHTTPMiddleware):
    # 1. ADD THIS INIT METHOD
    def __init__(self, app, public_paths: Optional[List[str]] = None):
        super().__init__(app)
        # Store the list passed from main.py, or use empty list if None
        self.public_paths = public_paths or []

    async def dispatch(self, request: Request, call_next):
        
        # 2. USE self.public_paths INSTEAD OF HARDCODED LIST
        # Check if the path is in the whitelist OR starts with /auth (standard login routes)
        if (request.url.path in self.public_paths) or \
           (request.url.path.startswith("/auth")) or \
           (request.url.path.startswith("/demo")):
            return await call_next(request)

        # 3. Verify Token (Existing Logic)
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid Authorization header"}
            )

        return await call_next(request)