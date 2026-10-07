import logging

from fastapi import APIRouter, HTTPException, status

from backend.schemas import JobAnalysisRequest, JobAnalysisResponse
from backend.services import analyze_job

logger = logging.getLogger("jobguard_backend")

router = APIRouter()


@router.post(
    "/api/analyze-job",
    response_model=JobAnalysisResponse,
    status_code=status.HTTP_200_OK,
)
async def analyze_job_endpoint(payload: JobAnalysisRequest) -> dict:
    """
    Validate input, call the AI service, and return the result.

    This route stays thin; the actual job-analysis logic lives in the AI
    pipeline owned by Person 1.
    """
    try:
        result = analyze_job(
            job_description=payload.job_description,
            rag_context=payload.rag_context or "",
        )

        if not isinstance(result, dict):
            raise TypeError("AI pipeline returned an invalid response.")

        return result

    except ValueError as exc:
        logger.warning("Invalid job analysis request: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected error while analyzing a job description.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while analyzing the job description.",
        ) from exc