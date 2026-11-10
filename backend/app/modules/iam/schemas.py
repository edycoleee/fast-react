from pydantic import BaseModel, EmailStr, Field


class PermissionCreateRequest(BaseModel):
    code: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class PermissionUpdateRequest(BaseModel):
    code: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=255)


class RoleCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=255)
    permission_ids: list[str] = Field(default_factory=list)


class RoleUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=255)
    permission_ids: list[str] | None = None


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
    role_ids: list[str] = Field(default_factory=list)
    is_active: bool = True


class UserUpdateRequest(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=80)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=255)
    role_ids: list[str] | None = None
    is_active: bool | None = None

