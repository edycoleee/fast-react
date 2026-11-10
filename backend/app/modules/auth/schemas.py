from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=255)


class AuthUserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    permissions: list[str]

