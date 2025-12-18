"""EMP Backend API main entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.middleware.auth import JWTAuthMiddleware
from app.clinicians.router import router as clinicians_router
from app.patients.router import router as patients_router
from app.logs.router import router as logs_router
from app.ml_engine.router import router as ml_router
from app.csv_demo import router as csv_demo_router

app = FastAPI(
    title="EMP Backend API",
    description="Epilepsy Management Platform API",
    version="0.1.0"
)

# CORS for frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001","http://localhost:5173"],  # patient/clinician frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    JWTAuthMiddleware,
    public_paths=[
        "/",              # root
        "/health",        # health
        "/docs",
        "/openapi.json",
        "/redoc",
        "/auth/admin",
        "/ml/predict",
        "/demo"    # keep invite endpoints open for now (optional)
    ],
)
# Mount routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(clinicians_router, prefix="/clinicians", tags=["clinicians"])
app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(logs_router, prefix="/logs", tags=["logs"])
app.include_router(ml_router)
app.include_router(csv_demo_router)

@app.get("/")
async def root():
    return {"message": "EMP Backend API is running"}
@app.get("/health")
async def health():
    return {"status": "healthy"}