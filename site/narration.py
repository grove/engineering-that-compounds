"""Text preparation and provenance shared by the build and TTS tools (stdlib only).

Adapted from the narration script in Software that improves with age.
"""
from __future__ import annotations

import hashlib
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "site" / "audio"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"
VOICE = "bf_emma"
SPEED = 0.95
SAMPLE_RATE = 24000
BIT_RATE = 64
ENGINE = "kokoro-onnx 0.4.9 / Kokoro v1.0"
MAX_CHUNK_CHARS = 420


def clean_inline(text: str) -> str:
    """Keep link labels, including URLs with balanced parentheses."""
    result: list[str] = []
    i = 0
    while i < len(text):
        if text[i] == "[":
            end = text.find("](", i)
            if end >= 0:
                j, depth = end + 2, 1
                while j < len(text) and depth:
                    depth += (text[j] == "(") - (text[j] == ")")
                    j += 1
                if not depth:
                    result.append(text[i + 1:end])
                    i = j
                    continue
        result.append(text[i])
        i += 1
    text = re.sub(r"[`*_~]", "", "".join(result))
    text = re.sub(r"\b(AI|API|APIs|CI|SQL|SRE|SDK|TTS)\b", lambda m: " ".join(m[0]), text)
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    chunks: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        for part in textwrap.wrap(sentence, width=max_chars, break_long_words=True, break_on_hyphens=False):
            if current and len(current) + len(part) + 1 > max_chars:
                chunks.append(current)
                current = ""
            current = f"{current} {part}".strip()
    if current:
        chunks.append(current)
    return chunks


def essay_to_segments(md: str) -> list[tuple[str, float, float]]:
    """Spoken text and pauses. Source lists and code blocks are not narrated."""
    segments: list[tuple[str, float, float]] = []
    paragraph: list[str] = []
    in_code = False

    def flush() -> None:
        text = clean_inline(" ".join(paragraph))
        paragraph.clear()
        chunks = split_sentences(text)
        for i, chunk in enumerate(chunks):
            segments.append((chunk, 0.0, 0.7 if i == len(chunks) - 1 else 0.14))

    for raw in md.replace("\r\n", "\n").splitlines():
        line = raw.strip()
        if line.startswith("```"):
            flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^## (Sources|References|Further reading)(?:\s|$)", line, re.I):
            break
        if not line:
            flush()
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)", line)
        if heading:
            flush()
            segments.append((clean_inline(heading[2]), 0.0 if len(heading[1]) == 1 else 1.35, 0.8))
            continue
        if re.fullmatch(r"(-{3,}|\*{3,}|_{3,})", line):
            flush()
            segments.append(("", 0.5, 0.0))
            continue
        paragraph.append(re.sub(r"^([-*>]|\d+\.)\s+", "", line))
    flush()
    return segments


def pipeline_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes() + (ROOT / "site" / "tts.py").read_bytes()).hexdigest()


def fingerprint(source: bytes, voice: str = VOICE, speed: float = SPEED) -> str:
    settings = json.dumps({"voice": voice, "speed": speed, "engine": ENGINE,
                           "pipeline": pipeline_hash(), "sample_rate": SAMPLE_RATE,
                           "bit_rate": BIT_RATE}, sort_keys=True).encode()
    return hashlib.sha256(settings + b"\n" + source).hexdigest()


def read_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.exists() else {}


def validate_audio(essays: list[Path]) -> dict:
    manifest = read_manifest()
    expected = {p.stem for p in essays}
    if set(manifest) != expected:
        raise RuntimeError("Narration manifest must contain exactly the listed essays. Run site/tts.py.")
    if {p.stem for p in AUDIO_DIR.glob("*.mp3")} != expected:
        raise RuntimeError("The MP3 files do not match the essays. Run site/tts.py.")
    for essay in essays:
        record = manifest[essay.stem]
        audio = AUDIO_DIR / f"{essay.stem}.mp3"
        if record.get("fingerprint") != fingerprint(essay.read_bytes(), record["voice"], record["speed"]):
            raise RuntimeError(f"Stale narration for {essay.name}. Run site/tts.py {essay.stem}.")
        if record.get("audio_sha256") != hashlib.sha256(audio.read_bytes()).hexdigest():
            raise RuntimeError(f"Narration checksum mismatch for {audio.name}.")
        if record.get("duration_seconds", 0) <= 0 or audio.stat().st_size < 1024:
            raise RuntimeError(f"Empty narration for {essay.name}.")
    return manifest
