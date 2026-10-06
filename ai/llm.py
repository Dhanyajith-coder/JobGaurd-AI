"""LLM-assisted holistic job-risk assessment with an offline fallback."""

from __future__ import annotations

import json
import os
from typing import Any


def _build_prompt(job_text: str, detected_flags: list[dict[str, Any]], rag_context: str) -> str:
	return f"""You are a job-scam risk analyst. Return only valid JSON with keys:
risk_score (integer 0-100), risk_level (LOW, MEDIUM, or HIGH), reasoning (string),
evidence (list of strings), and recommendation (string).

Job description:
{job_text}

Heuristic flags:
{json.dumps(detected_flags, ensure_ascii=True)}

Relevant reference context (optional):
{rag_context or "No reference context supplied."}

Assess the whole listing, distinguish evidence from speculation, and do not invent facts."""


def _offline_assessment(detected_flags: list[dict[str, Any]]) -> dict[str, Any]:
	"""Produce a deterministic assessment when no LLM credentials are configured."""
	score = min(100, sum(int(flag.get("weight", 0)) for flag in detected_flags))
	level = "HIGH" if score >= 65 else "MEDIUM" if score >= 30 else "LOW"
	evidence = [str(flag["evidence"]) for flag in detected_flags if flag.get("evidence")]
	return {
		"risk_score": score,
		"risk_level": level,
		"reasoning": "Offline assessment based on detected scam indicators.",
		"evidence": evidence,
		"recommendation": "Do not pay fees or share sensitive information until the employer is independently verified." if score >= 30 else "Verify the employer and role through independent sources before applying.",
		"source": "offline_fallback",
	}


def analyze_context_with_llm(
	job_text: str,
	detected_flags: list[dict[str, Any]],
	rag_context: str = "",
) -> dict[str, Any]:
	"""Assess a posting using OpenAI when configured, otherwise use a safe fallback."""
	prompt = _build_prompt(job_text, detected_flags, rag_context)
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		assessment = _offline_assessment(detected_flags)
		assessment["prompt"] = prompt
		return assessment

	try:
		from openai import OpenAI

		client = OpenAI(api_key=api_key)
		response = client.chat.completions.create(
			model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
			messages=[{"role": "user", "content": prompt}],
			temperature=0,
			response_format={"type": "json_object"},
		)
		content = response.choices[0].message.content or "{}"
		assessment = json.loads(content)
		assessment["source"] = "llm"
		assessment["prompt"] = prompt
		return assessment
	except Exception as exc:
		assessment = _offline_assessment(detected_flags)
		assessment["llm_error"] = str(exc)
		assessment["prompt"] = prompt
		return assessment


if __name__ == "__main__":
	print(analyze_context_with_llm("Hiring immediately; pay a registration fee.", [{"evidence": "registration fee", "weight": 35}]))
