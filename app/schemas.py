from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserBaseSchema(BaseModel):

    first_name: str
    last_name: str
    company: str
    phone_number: str
    email: str
    role: str = 'user'
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        orm_mode = True
    

class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    active: bool = False 


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)



class ReportBaseSchema(BaseModel):
    user_id: str | None = None
    type: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    title: str
    content: str
    attachment: str
    status: str
    operator_call: bool = False
    personal_data_source: str | None = None
    pd_operator_relation: str | None = None

    class Config:
        orm_mode = True
