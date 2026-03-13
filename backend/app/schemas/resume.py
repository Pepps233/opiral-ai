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


class ResumeUploadResponse(BaseModel):
    session_id: str
    storage_path: str


class ResumeStatusResponse(BaseModel):
    session_id: str
    status: str  # "pending" | "done"
    parsed: Optional[ParsedResume] = None
