from pydantic import BaseModel
from typing import List, Optional


class ParsedResume(BaseModel):
    session_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = []
    coursework: List[str] = []
    research: List[str] = []
    projects: List[str] = []
    desired_roles: List[str] = []
    summary: Optional[str] = None


class ResumeParseResponse(BaseModel):
    session_id: str
    parsed: ParsedResume
    storage_path: Optional[str] = None
