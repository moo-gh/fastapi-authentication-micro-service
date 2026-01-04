import uuid
from pydantic import BaseModel, EmailStr

class SendCodeRequest(BaseModel):
    email: EmailStr
    project_id: str

class VerifyCodeRequest(BaseModel):
    email: EmailStr
    project_id: str
    code: str

class VerificationProof(BaseModel):
    auth_user_id: uuid.UUID
    email: str
    project_id: str
    verified: bool
    issued_at: int
    signature: str

class HealthResponse(BaseModel):
    status: str

