# D1 · Write UserIn. See the slide for the rules.
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class UserIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=32)]

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("name")
    @classmethod
    def letters_only(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("name must contain letters only")
        return v
