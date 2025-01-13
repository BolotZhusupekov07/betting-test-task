from typing import TypeVar

from pydantic import BaseModel, model_validator

Schema = TypeVar("Schema", bound=BaseModel)

class UpdateInBaseModel(BaseModel):
    @model_validator(mode="before")
    def ensure_at_least_one_field_updated(cls, values: dict) -> dict:
        if not {
            field: value
            for field, value in values.items()
            if value is not None
        }:
            raise ValueError("Ensure at least one field has been updated.")

        return values
