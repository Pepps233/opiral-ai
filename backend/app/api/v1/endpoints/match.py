from fastapi import APIRouter, Request
from app.schemas.match import MatchRequest, MatchResponse
from app.core.rate_limit import check_rate_limit
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=MatchResponse)
async def match_labs(request: Request, body: MatchRequest):
    """Return ranked research lab matches for a parsed resume."""
    await check_rate_limit(request, "match", settings.DAILY_MATCH_LIMIT)
    # TODO: implement in Step 4
    raise NotImplementedError
