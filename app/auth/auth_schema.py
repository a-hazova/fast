from pydantic import BaseModel, ConfigDict, EmailStr

class BaseAuth(BaseModel):
    username: str

class AuthLogin(BaseAuth):
    password: str

class AuthSignUp(BaseAuth):
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class AuthUser(BaseAuth):
    id: int


class TokenData(BaseModel):
    access_token: str
    token_type: str

class Token(BaseModel):
    id: int