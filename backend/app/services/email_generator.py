"""GPT-4o personalized email opening generator."""
from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.resume import ParsedResume
from app.schemas.email import EmailResponse

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert academic outreach writer helping a Purdue University student reach out to a research lab.
Write a personalized, professional 3-4 sentence email opening that:
1. Mentions the professor by name and their specific research area
2. Highlights 1-2 of the student's most relevant skills or experiences
3. Expresses genuine interest in the lab's work
4. Does NOT include subject line in the body

Also provide a compelling subject line separately.
Return JSON with keys: opening (string), subject_line (string)."""


async def generate_opening(
    parsed: ParsedResume, lab_meta: dict, lab_id: str
) -> EmailResponse:
    user_prompt = f"""Student profile:
- Skills: {', '.join(parsed.skills[:8])}
- Research: {', '.join(parsed.research[:3])}
- Projects: {', '.join(parsed.projects[:2])}

Lab info:
- Professor: {lab_meta.get('professor')}
- Department: {lab_meta.get('department')}
- Research areas: {', '.join(lab_meta.get('research_areas', []))}
- Description: {lab_meta.get('description', '')}"""

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    import json
    data = json.loads(response.choices[0].message.content)
    return EmailResponse(
        lab_id=lab_id,
        opening=data["opening"],
        subject_line=data["subject_line"],
    )
