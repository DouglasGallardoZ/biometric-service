from pydantic import BaseModel


class EnrollResponse(BaseModel):
    persona_id: int
    status: str


class VerifyResponse(BaseModel):
    persona_id: int
    match: bool
    distance: float


class ValidateResponse(BaseModel):
    match: bool
    distance: float
