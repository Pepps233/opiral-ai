"""OpenAI embeddings + Pinecone vector search."""
from openai import AsyncOpenAI
from pinecone import Pinecone
from app.core.config import settings
from app.schemas.resume import ParsedResume
from app.schemas.match import LabMatch
from typing import List

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
pc = Pinecone(api_key=settings.PINECONE_API_KEY)


async def embed_text(text: str) -> List[float]:
    response = await client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return response.data[0].embedding


def resume_to_query_text(parsed: ParsedResume) -> str:
    parts = [
        "Skills: " + ", ".join(parsed.skills),
        "Coursework: " + ", ".join(parsed.coursework),
        "Research: " + ", ".join(parsed.research),
        "Projects: " + ", ".join(parsed.projects),
        "Desired roles: " + ", ".join(parsed.desired_roles),
    ]
    if parsed.summary:
        parts.insert(0, parsed.summary)
    return "\n".join(parts)


async def query_similar_labs(
    parsed: ParsedResume, top_k: int = 10
) -> List[LabMatch]:
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    query_text = resume_to_query_text(parsed)
    embedding = await embed_text(query_text)
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    matches = []
    for match in results.matches:
        meta = match.metadata or {}
        matches.append(
            LabMatch(
                lab_id=match.id,
                professor=meta.get("professor", ""),
                department=meta.get("department", ""),
                research_areas=meta.get("research_areas", []),
                similarity_score=round(match.score, 4),
                contact_email=meta.get("contact_email"),
            )
        )
    return matches
