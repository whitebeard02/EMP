from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# CHANGE CLASS NAME HERE TO MATCH MAIN.PY
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        
        # 1. Define Public Paths (The Whitelist)
        public_paths = [
            "/docs",            # Swagger UI
            "/redoc",           # ReDoc UI
            "/openapi.json",    # API Schema
            "/favicon.ico",     # Browser Icon
            "/",                # Root/Health check
        ]

        # 2. Check if the path is public or is an Auth route
        if request.url.path in public_paths or request.url.path.startswith("/auth"):
            return await call_next(request)

        # 3. Verify Token
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            # Return JSON instead of raising Exception to prevent 500 crashes
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid Authorization header"}
            )

        return await call_next(request)