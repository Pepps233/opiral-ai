from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Request
from app.schemas.resume import ResumeParseResponse
from app.core.rate_limit import check_rate_limit
from app.core.config import settings

router = APIRouter()


@router.post("/upload", response_model=ResumeParseResponse)
async def upload_resume(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    """Upload a PDF resume; parse and embed in background."""
    # TODO: implement in Step 3
    raise NotImplementedError
