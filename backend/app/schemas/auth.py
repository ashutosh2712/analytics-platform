from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    organization_name: str = Field(
        min_length=2,
        max_length=255,
    )


class LoginRequest(BaseModel):
    email: EmailStr

    password: str


class TokenResponse(BaseModel):
    access_token: str

    refresh_token: str

    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int

    email: EmailStr

    organization_id: int

    role: str

    model_config = {
        "from_attributes": True
    }