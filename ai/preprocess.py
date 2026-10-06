"""Text normalization helpers for job descriptions."""

from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser


class _TextExtractor(HTMLParser):
	"""Collect visible text while ignoring markup."""

	def __init__(self) -> None:
		super().__init__(convert_charrefs=True)
		self.parts: list[str] = []

	def handle_data(self, data: str) -> None:
		self.parts.append(data)


def clean_job_description(raw_text: str) -> str:
	"""Return readable plain text with HTML and inconsistent whitespace removed."""
	if not isinstance(raw_text, str):
		raise TypeError("raw_text must be a string")

	extractor = _TextExtractor()
	extractor.feed(unescape(raw_text))
	extractor.close()
	text = " ".join(extractor.parts)
	text = text.replace("\xa0", " ").replace("\t", " ")
	text = text.replace("\r\n", "\n").replace("\r", "\n")
	text = re.sub(r"[ \f\v]+", " ", text)
	text = re.sub(r" *\n+ *", "\n", text)
	return text.strip()


if __name__ == "__main__":
	sample = "<h1>Data Entry</h1>\r\nPay&nbsp; $5,000\tweekly"
	print(clean_job_description(sample))
