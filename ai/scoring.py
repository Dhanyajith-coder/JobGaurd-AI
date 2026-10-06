"""Risk-score calculation for heuristic and LLM assessments."""

from __future__ import annotations

from typing import Any


def calculate_risk_score(rule_flags: list[dict[str, Any]], llm_assessment: dict[str, Any]) -> dict[str, Any]:
	"""Blend rule weights and an LLM score into a normalized risk result."""
	rule_score = min(100, sum(max(0, int(flag.get("weight", 0))) for flag in rule_flags))
	try:
		llm_score = max(0, min(100, int(float(llm_assessment.get("risk_score", rule_score)))))
	except (TypeError, ValueError):
		llm_score = rule_score

	score = round((rule_score * 0.6) + (llm_score * 0.4))
	level = "HIGH" if score >= 65 else "MEDIUM" if score >= 30 else "LOW"
	return {"risk_score": score, "risk_level": level, "rule_score": rule_score, "llm_score": llm_score}


if __name__ == "__main__":
	print(calculate_risk_score([{"weight": 35}], {"risk_score": 40}))
