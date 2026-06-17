from pydantic import BaseModel,EmailStr
from enum import Enum

class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"

class NotificationCreate(BaseModel):
    recipient: EmailStr
    title: str
    message: str
    channel: NotificationChannel



class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    channel: str
    status: str
    sent_by: int

    class Config:
        from_attributes = True

class NotificationUpdate(BaseModel):
    status: str