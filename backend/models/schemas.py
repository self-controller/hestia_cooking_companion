from pydantic import BaseModel, Field

class User_in(BaseModel):
    username: str
    password: str
    email: str

class User_out(BaseModel):
    id: int
    username: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str
