from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    role: str
    trip_info: str
    message: str
