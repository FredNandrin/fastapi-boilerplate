
from pydantic import BaseModel, Field, ConfigDict


class PostSchema(BaseModel):
    model_config = ConfigDict(json_schema_extra = {
            "example": {
                "title": "Post Title.",
                "content": "Post content. This should accept <b>HTML</b> content."
            }
        }
    )
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)
