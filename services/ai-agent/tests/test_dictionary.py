"""Hinglish, shorthand and duration parsing."""

from __future__ import annotations

import pytest

from logsense_ai.extraction.dictionary import (
    expand_shorthand,
    normalize,
    parse_downtime_hours,
)


@pytest.mark.parametrize(
    ("raw", "expected_fragment"),
    [
        ("MTR brng noise", "motor bearing"),
        ("replcd 6205ZZ", "replaced"),
        ("algnmnt chk", "alignment check"),
        ("m/c band tha", "machine stopped"),
        # Devanagari must survive tokenisation: a plain \w tokeniser shreds these
        # words at their vowel signs and every entry below becomes unreachable.
        ("लाइन 2 कैपिंग मोटर", "line 2 capping motor"),
        ("बेयरिंग बदला", "bearing replaced"),
        ("कन्वेयर बंद", "conveyor stopped"),
        ("मशीन खराब", "machine faulty"),
    ],
)
def test_expand_shorthand(raw: str, expected_fragment: str) -> None:
    assert expected_fragment in expand_shorthand(raw).lower()


def test_expand_preserves_unknown_tokens() -> None:
    """Expansion is additive, never lossy: a part code must survive untouched."""
    assert "6205ZZ" in expand_shorthand("replcd 6205ZZ today")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2 ghante", 2.0),
        ("2 घंटे", 2.0),
        ("3 तास", 3.0),
        ("30 min", 0.5),
        ("45 मिनट", 0.75),
        ("1.5 hrs", 1.5),
        ("2 h", 2.0),
        ("1 hr 30 min", 1.5),
        ("aadha ghanta", 0.5),
        ("आधा तास", 0.5),
        ("डेढ़ घंटा", 1.5),
        ("डेढ घंटे", 1.5),
        ("sawa ghanta", 1.25),
        ("ek shift", 8.0),
        ("एक शिफ्ट", 8.0),
    ],
)
def test_parse_downtime(text: str, expected: float) -> None:
    assert parse_downtime_hours(text) == pytest.approx(expected)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "machine kharab hai",
        "replaced bearing 6205ZZ",  # a part code is not a duration
        "SKF-6205 fitted",
    ],
)
def test_parse_downtime_returns_none_when_absent(text: str) -> None:
    """Null is correct when nothing is stated. Zero would corrupt every downtime total."""
    assert parse_downtime_hours(text) is None


def test_normalize_collapses_separators() -> None:
    assert normalize("  Conv  Motor-3 ") == "conv motor 3"
    assert normalize("CONV_MOTOR-3") == "conv motor 3"
