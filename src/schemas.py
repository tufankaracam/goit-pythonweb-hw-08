from pydantic import BaseModel, Field, EmailStr, PastDate
from datetime import datetime
from typing import List, Optional


class ContactModel(BaseModel):
    firstname: str = Field(max_length=50)
    lastname: str = Field(max_length=50)
    email: str = EmailStr()
    phone: str = Field(max_length=50)
    birthdate: datetime = PastDate()
    additional: Optional[str] = None


class ContactResponse(ContactModel):
    id: int
