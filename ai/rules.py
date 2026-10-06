"""Deterministic red-flag detection for job postings."""

from __future__ import annotations

import re


def _flag(category: str, description: str, evidence: str, weight: int) -> dict[str, object]:
	return {
		"category": category,
		"description": description,
		"evidence": evidence,
		"weight": weight,
	}


def _matches(text: str, patterns: tuple[str, ...]) -> list[str]:
	return [match.group(0) for pattern in patterns if (match := re.search(pattern, text, re.IGNORECASE))]


def detect_rule_flags(text: str) -> list[dict[str, object]]:
	"""Detect common job-scam signals and return evidence-bearing flag records."""
	if not isinstance(text, str):
		raise TypeError("text must be a string")

	checks: tuple[tuple[str, str, tuple[str, ...], int], ...] = (
		(
			"UPFRONT_PAYMENT",
			"The applicant may be asked to pay an upfront fee.",
			(r"(?:pay|send|wire|transfer|deposit).{0,30}(?:fee|money|payment|cost)",
			 r"(?:registration|training|starter|equipment|processing)\s+fee",
			 r"pay\s+(?:to|for)\s+(?:apply|start|register)"),
			35,
		),
		(
			"UNREALISTIC_SALARY",
			"The compensation or experience requirements appear unusually unrealistic.",
			(r"(?:\$|€|£)\s?[0-9][0-9,]*(?:\s*(?:per|/)?\s*(?:day|hour|week))?", 
			 r"(?:high|guaranteed|earn|make|salary).{0,35}(?:no experience|data entry|from home)",
			 r"no\s+experience.{0,35}(?:high|guaranteed|salary|income|pay)"),
			25,
		),
		(
			"SUSPICIOUS_CONTACT",
			"The listing relies on informal or disposable contact channels.",
			(r"(?:telegram|whatsapp)\s*(?:only|preferred|required)?",
			 r"(?:contact|email|send your CV).{0,40}(?:@(?:gmail|yahoo|hotmail|outlook|protonmail)\.(?:com|net|org))"),
			20,
		),
		(
			"URGENCY_PRESSURE",
			"The listing uses urgency or scarcity to pressure applicants.",
			(r"hiring\s+immediately", r"limited\s+spots?", r"act\s+now", r"urgent(?:ly)?", r"apply\s+today"),
			15,
		),
	)

	flags: list[dict[str, object]] = []
	for category, description, patterns, weight in checks:
		evidence = _matches(text, patterns)
		if evidence:
			flags.append(_flag(category, description, "; ".join(evidence), weight))
	return flags


if __name__ == "__main__":
	print(detect_rule_flags("Hiring immediately. Pay a registration fee and contact us on Telegram only."))
