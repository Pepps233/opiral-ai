from pydantic import BaseModel


class EmailRequest(BaseModel):
    session_id: str
    lab_id: str


class EmailResponse(BaseModel):
    lab_id: str
    opening: str
    subject_line: str
