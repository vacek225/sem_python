from __future__ import annotations

from pydantic import BaseModel, Field


class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0, description="Sepal length in centimeters")
    sepal_width: float = Field(gt=0, description="Sepal width in centimeters")
    petal_length: float = Field(gt=0, description="Petal length in centimeters")
    petal_width: float = Field(gt=0, description="Petal width in centimeters")


class PredictionResponse(BaseModel):
    class_id: int
    species: str


class ModelInfoResponse(BaseModel):
    name: str
    version: str
    feature_types: dict[str, str]
    classes: list[str]


class HealthResponse(BaseModel):
    status: str
