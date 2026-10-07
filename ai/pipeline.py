"""End-to-end job analysis orchestration."""

from __future__ import annotations

from typing import Any

try:
	from .llm import analyze_context_with_llm
	from .preprocess import clean_job_description
	from .rules import detect_rule_flags
	from .scoring import calculate_risk_score
except ImportError:  # Allow ``python ai/pipeline.py`` from the repository root.
	from llm import analyze_context_with_llm
	from preprocess import clean_job_description
	from rules import detect_rule_flags
	from scoring import calculate_risk_score


def run_job_analysis_pipeline(raw_job_text: str, rag_context: str = "") -> dict[str, Any]:
	"""Return the public JSON-compatible result for one job description."""
	job_text = clean_job_description(raw_job_text)
	red_flags = detect_rule_flags(job_text)
	llm_assessment = analyze_context_with_llm(job_text, red_flags, rag_context)
	score = calculate_risk_score(red_flags, llm_assessment)

	evidence = [str(flag["evidence"]) for flag in red_flags]
	evidence.extend(str(item) for item in llm_assessment.get("evidence", []) if str(item) not in evidence)
	return {
		"risk_score": score["risk_score"],
		"risk_level": score["risk_level"],
		"red_flags": red_flags,
		"evidence": evidence,
		"recommendation": llm_assessment.get(
			"recommendation",
			"Verify the employer and role through independent sources before applying.",
		),
	}


if __name__ == "__main__":
	job = """
	Customer support executive needed urgently.
	Earn ₹60,000 per month with no experience required.
	Contact us on Gmail for immediate joining.
	"""
	print(run_job_analysis_pipeline(job))
