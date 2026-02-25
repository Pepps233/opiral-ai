from fastapi import APIRouter
from app.api.v1.endpoints import resume, match, email

api_router = APIRouter()
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(match.router, prefix="/match", tags=["match"])
api_router.include_router(email.router, prefix="/email", tags=["email"])
