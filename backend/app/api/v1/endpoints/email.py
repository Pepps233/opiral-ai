from fastapi import APIRouter, Request
from app.schemas.email import EmailRequest, EmailResponse
from app.core.rate_limit import check_rate_limit
from app.core.config import settings

router = APIRouter()


@router.post("/generate", response_model=EmailResponse)
async def generate_email(request: Request, body: EmailRequest):
    """Generate a personalized outreach email opening."""
    await check_rate_limit(request, "email", settings.DAILY_EMAIL_LIMIT)
    # TODO: implement in Step 5
    raise NotImplementedError
