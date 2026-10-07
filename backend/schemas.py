from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobAnalysisRequest(BaseModel):
    """Request payload for analyzing a job posting."""

    model_config = ConfigDict(str_strip_whitespace=True)

    job_description: str = Field(..., min_length=1)
    rag_context: Optional[str] = None

    @field_validator("job_description")
    @classmethod
    def validate_job_description(cls, value: str) -> str:
        if value is None or not value.strip():
            raise ValueError("job_description cannot be empty")
        return value.strip()


class RedFlag(BaseModel):
    """A single suspicious signal returned by the AI pipeline."""

    category: str
    description: str
    evidence: str
    weight: int | float


class JobAnalysisResponse(BaseModel):
    """Response structure returned by ai.pipeline.run_job_analysis_pipeline()."""

    risk_score: int | float
    risk_level: str
    red_flags: list[RedFlag] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    recommendation: str