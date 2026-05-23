from pydantic import BaseModel, ConfigDict

class WebsiteCreate(BaseModel):
    url: str
    interval: int


class WebsiteOut(BaseModel):
    id: int
    url: str
    interval: int
    is_active: bool
    user_id: int

    model_config = ConfigDict(from_attributes=True)
