from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Image(BaseModel):
    query: str
    image_url: str
    image_data: bytes
    width: int
    height: int
    downloaded_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(frozen=True)

    @field_validator("width", "height")
    def validate_dimensions(cls, value):
        if value <= 0:
            raise ValueError("Width and height must be positive integers.")
        return value
