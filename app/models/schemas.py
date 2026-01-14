from pydantic import BaseModel


class EnrollResponse(BaseModel):
    user_id: str
    status: str


class VerifyResponse(BaseModel):
    user_id: str
    match: bool
    distance: float


class ValidateResponse(BaseModel):
    match: bool
    distance: float
