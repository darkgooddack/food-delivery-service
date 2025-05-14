from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    telephone: str
    address: str

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    telephone: str
    address: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
