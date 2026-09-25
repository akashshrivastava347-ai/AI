"""Hinglish, Devanagari and technician-shorthand vocabulary.

This is the moat, not the model. A general-purpose LLM handles Hindi fine; what it
does not know is that in an Indian plant "m/c band tha" means the machine was
stopped, that "6205ZZ" is a bearing, or that "2 ghante" is two hours.

The same dictionary is applied in two places on purpose:

* as hints in the extraction prompt, so the model reads shorthand correctly;
* in search query expansion (Story 3), so retrieval behaves identically.

Using one table for both is what stops extraction and search from quietly
disagreeing about what "brng" means.
"""

from __future__ import annotations

import re
import unicodedata

# --- shorthand -> canonical English ------------------------------------------------
SHORTHAND: dict[str, str] = {
    # components
    "brng": "bearing",
    "brg": "bearing",
    "bearng": "bearing",
    "beyring": "bearing",
    "mtr": "motor",
    "m/c": "machine",
    "mc": "machine",
    "conv": "conveyor",
    "cnvyr": "conveyor",
    "gbx": "gearbox",
    "cplg": "coupling",
    "vlv": "valve",
    "cyl": "cylinder",
    "prox": "proximity sensor",
    "plc": "programmable logic controller",
    "vfd": "variable frequency drive",
    "hyd": "hydraulic",
    "pnmtc": "pneumatic",
    "lub": "lubrication",
    # conditions and actions
    "algnmnt": "alignment",
    "algn": "alignment",
    "replcd": "replaced",
    "repl": "replaced",
    "chkd": "checked",
    "chk": "check",
    "ovrhtng": "overheating",
    "vibrtn": "vibration",
    "temp": "temperature",
    "abnrml": "abnormal",
    "bkdwn": "breakdown",
    "pm": "preventive maintenance",
    "ok": "resolved",
    # Hinglish (Latin script)
    "band": "stopped",
    "bandh": "stopped",
    "chalu": "running",
    "kharab": "faulty",
    "garam": "hot",
    "awaaz": "noise",
    "aawaz": "noise",
    "badla": "replaced",
    "badal": "replace",
    "badli": "replaced",
    "lagaya": "installed",
    "nikala": "removed",
    "saaf": "cleaned",
    "kasa": "tightened",
    "tuta": "broken",
    "leak": "leakage",
    "marammat": "repair",
    "ghisa": "worn",
    "jam": "jammed",
    # Devanagari (Hindi / Marathi)
    "बेयरिंग": "bearing",
    "बेअरिंग": "bearing",
    "मोटर": "motor",
    "मशीन": "machine",
    "कन्वेयर": "conveyor",
    "पंप": "pump",
    "बंद": "stopped",
    "खराब": "faulty",
    "गरम": "hot",
    "आवाज": "noise",
    "बदला": "replaced",
    "बदलले": "replaced",
    "साफ": "cleaned",
    "गळती": "leakage",
    "दुरुस्ती": "repair",
    "तुटले": "broken",
    # Devanagari asset vocabulary. Without these, a technician who writes the machine
    # name in Hindi or Marathi scores ~0.21 against a Latin-script asset register and
    # never resolves — measured, not assumed.
    "लाइन": "line",
    "ओळ": "line",
    "कैपिंग": "capping",
    "फिलिंग": "filling",
    "पैकिंग": "packing",
    "लेबलर": "labeller",
    "कंप्रेसर": "compressor",
    "कॉम्प्रेसर": "compressor",
    "गियरबॉक्स": "gearbox",
    "गिअरबॉक्स": "gearbox",
    "पंखा": "fan",
    "ब्लोअर": "blower",
    "यूटिलिटी": "utilities",
    "यूटिलिटीज": "utilities",
    "बेल्ट": "belt",
    "सील": "seal",
    "वाल्व": "valve",
    "सेंसर": "sensor",
    "मशिन": "machine",
}

# --- duration phrases --------------------------------------------------------------
# Technicians write downtime a dozen ways. Parsing it deterministically matters:
# downtime is the number the whole business case rests on, so it must never be a
# generated guess.
#
# Boundary handling note: Devanagari vowel signs and the nukta are NOT word
# characters in Python's ``re`` ("े".isalnum() is False), so a trailing ``\b`` after
# "घंटे" can never match. Every boundary here is expressed as a ``\w`` lookaround,
# which behaves correctly for Latin and Devanagari alike.
_NOT_WORD_BEFORE = r"(?<!\w)"
_NOT_WORD_AFTER = r"(?!\w)"

# "डेढ़" appears with and without the nukta, and sometimes as precomposed U+095D.
_DERH = r"(?:derh|ded|डेढ़?|डे\u095d|दीड)"

_HOUR_WORDS = r"(?:hours?|hrs?|h|ghante|ghanta|घंटे|घंटा|तास|तासात)"
# Bare "m" is deliberately excluded: "6205 M" is a part suffix far more often than
# it is six thousand minutes of downtime.
_MIN_WORDS = r"(?:minutes?|mins?|मिनट|मिनिट)"

_DURATION_PATTERNS: list[tuple[re.Pattern[str], float]] = [
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(\d+(?:\.\d+)?)\s*{_HOUR_WORDS}{_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        1.0,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(\d+(?:\.\d+)?)\s*{_MIN_WORDS}{_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        1 / 60,
    ),
]

# Fractional and idiomatic phrases that carry no digit at all.
_WORD_DURATIONS: list[tuple[re.Pattern[str], float]] = [
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(?:aadha|adha|आधा|अर्धा)\s*"
            rf"(?:ghanta|ghante|घंटा|घंटे|तास){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        0.5,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(?:paune|पौने)\s*(?:ek|एक)?\s*"
            rf"(?:ghanta|घंटा){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        0.75,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(?:sawa|सवा)\s*(?:ghanta|घंटा){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        1.25,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}{_DERH}\s*"
            rf"(?:ghanta|ghante|घंटा|घंटे|तास){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        1.5,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(?:ek|एक)\s*(?:shift|शिफ्ट){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        8.0,
    ),
    (
        re.compile(
            rf"{_NOT_WORD_BEFORE}(?:poora|पूरा)\s*(?:din|दिन){_NOT_WORD_AFTER}",
            re.IGNORECASE,
        ),
        8.0,
    ),
]

_WS_RE = re.compile(r"\s+")
# Devanagari vowel signs, matras and the nukta are combining marks, which Python's
# ``\w`` does not match. A plain ``[\w/]+`` therefore shreds "मोटर" into "म" and
# "टर", and every Devanagari dictionary entry silently becomes unreachable. Including
# the Devanagari block keeps such words whole.
_TOKEN_RE = re.compile(r"[\w\u0900-\u097F/]+", re.UNICODE)


def normalize(text: str) -> str:
    """Case-fold, strip accents-in-compatibility-forms and collapse whitespace.

    Used for alias lookup so that "Conv Motor-3", "conv  motor 3" and
    "CONV MOTOR-3" all hit the same key.
    """
    if not text:
        return ""
    folded = unicodedata.normalize("NFKC", text).strip().lower()
    folded = folded.replace("-", " ").replace("_", " ")
    return _WS_RE.sub(" ", folded)


def expand_shorthand(text: str) -> str:
    """Rewrite known shorthand into canonical English, preserving everything else.

    Non-destructive by design: the original text is always kept on the raw record,
    and this expansion is only ever used to help matching and prompting.
    """
    if not text:
        return ""

    def _replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return SHORTHAND.get(token.lower(), token)

    return _TOKEN_RE.sub(_replace, text)


def parse_downtime_hours(text: str) -> float | None:
    """Best-effort deterministic downtime in decimal hours.

    Returns ``None`` when nothing is stated. Null is honest and is counted in
    coverage reporting; zero would silently corrupt every downtime total.
    """
    if not text:
        return None

    # Compose to a canonical form first so nukta spellings match the patterns.
    text = unicodedata.normalize("NFC", text)

    for pattern, hours in _WORD_DURATIONS:
        if pattern.search(text):
            return hours

    total: float | None = None
    for pattern, multiplier in _DURATION_PATTERNS:
        for raw in pattern.findall(text):
            try:
                value = float(raw) * multiplier
            except ValueError:  # pragma: no cover - regex guarantees numeric
                continue
            total = value if total is None else total + value

    if total is None:
        return None
    return round(total, 3)


def prompt_hints(limit: int = 40) -> str:
    """A compact glossary for the extraction prompt.

    Kept short and stable: it sits in the cached prompt prefix, so it is paid for
    once per cache window rather than once per message.
    """
    items = list(SHORTHAND.items())[:limit]
    return ", ".join(f"{k}={v}" for k, v in items)
