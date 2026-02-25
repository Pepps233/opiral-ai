"""Resume structuring via GPT-4o."""
import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.resume import ParsedResume
import uuid

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a resume parser. Given raw resume text, extract and return ONLY valid JSON with these keys:
name, email, skills (list), coursework (list), research (list), projects (list), desired_roles (list), summary (string).
Return nothing but the JSON object."""


async def parse_resume(raw_text: str) -> ParsedResume:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return ParsedResume(session_id=str(uuid.uuid4()), **data)
