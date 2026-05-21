from pydantic import BaseModel


class WebsiteCreate(BaseModel):
    url: str
    interval: int


class WebsiteOut(BaseModel):
    id: int
    url: str
    interval: int
    is_active: bool
    user_id: int
