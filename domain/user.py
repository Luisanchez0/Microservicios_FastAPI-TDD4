
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime
    
    class Config:
        use_enum_values = True
    
    def activate(self):
        self.status = UserStatus.ACTIVE
    
    def deactivate(self):
        self.status = UserStatus.INACTIVE
    
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[UserStatus] = None