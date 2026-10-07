from __future__ import annotations

from ai.pipeline import run_job_analysis_pipeline


def analyze_job(job_description: str, rag_context: str = "") -> dict:
    """
    Call the existing AI pipeline without duplicating its logic.

    Person 1 owns the preprocessing, rules, LLM integration, scoring,
    and risk-level calculation. This backend is only responsible for
    passing the request to that pipeline and returning its result.
    """
    return run_job_analysis_pipeline(
        raw_job_text=job_description,
        rag_context=rag_context or "",
    )