#!/usr/bin/env python3
"""Generate committed MP3 narration with the original collection's Kokoro voice.

Install site/requirements-tts.txt first. Models are cached under .cache/kokoro
unless --model-dir is supplied. Text stays on the machine running this script.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import urllib.request

from narration import (AUDIO_DIR, BIT_RATE, ENGINE, MANIFEST_PATH, ROOT, SAMPLE_RATE,
                       SPEED, VOICE, essay_to_segments, fingerprint, read_manifest)

MODEL_BASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODEL_FILES = ("kokoro-v1.0.onnx", "voices-v1.0.bin")
_kokoro = None


def ensure_models(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for name in MODEL_FILES:
        target = directory / name
        if not target.exists():
            print(f"Downloading {name}...", flush=True)
            temporary = target.with_suffix(target.suffix + ".part")
            urllib.request.urlretrieve(MODEL_BASE + name, temporary)
            temporary.replace(target)


def initialize_worker(model_dir: str, threads: int) -> None:
    global _kokoro
    import onnxruntime as ort
    from kokoro_onnx import Kokoro
    options = ort.SessionOptions()
    options.intra_op_num_threads = threads
    options.inter_op_num_threads = 1
    options.log_severity_level = 3
    session = ort.InferenceSession(str(Path(model_dir) / MODEL_FILES[0]), sess_options=options,
                                   providers=["CPUExecutionProvider"])
    _kokoro = Kokoro.from_session(session, str(Path(model_dir) / MODEL_FILES[1]))


def synthesize(path: Path, voice: str, speed: float) -> tuple[str, dict]:
    import lameenc
    import numpy as np
    source = path.read_bytes()
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(BIT_RATE)
    encoder.set_in_sample_rate(SAMPLE_RATE)
    encoder.set_channels(1)
    encoder.set_quality(2)
    out = AUDIO_DIR / f"{path.stem}.mp3"
    temporary = out.with_suffix(".mp3.part")
    language = "en-gb" if voice.startswith(("bf_", "bm_")) else "en-us"
    samples_written = 0
    with temporary.open("wb") as stream:
        def write(samples) -> None:
            nonlocal samples_written
            samples_written += len(samples)
            pcm = (np.clip(samples, -1, 1) * 32767).astype(np.int16)
            stream.write(encoder.encode(pcm.tobytes()))

        for text, before, after in essay_to_segments(source.decode("utf-8")):
            if before:
                write(np.zeros(round(before * SAMPLE_RATE), dtype=np.float32))
            if text:
                samples, rate = _kokoro.create(text, voice=voice, speed=speed, lang=language)
                if rate != SAMPLE_RATE:
                    raise RuntimeError(f"Unexpected sample rate: {rate}")
                write(samples)
            if after:
                write(np.zeros(round(after * SAMPLE_RATE), dtype=np.float32))
        stream.write(encoder.flush())
    temporary.replace(out)
    return path.stem, {
        "fingerprint": fingerprint(source, voice, speed),
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "audio_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "duration_seconds": round(samples_written / SAMPLE_RATE, 2),
        "voice": voice, "speed": speed, "engine": ENGINE,
        "sample_rate": SAMPLE_RATE, "bit_rate_kbps": BIT_RATE,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slugs", nargs="*", help="Essay slugs; defaults to all")
    parser.add_argument("--voice", default=VOICE)
    parser.add_argument("--speed", type=float, default=SPEED)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--threads", type=int, default=2, help="ONNX threads per worker")
    parser.add_argument("--model-dir", type=Path, default=ROOT / ".cache" / "kokoro")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not 0.5 <= args.speed <= 2 or args.workers < 1 or args.threads < 1:
        parser.error("Speed must be 0.5–2; workers and threads must be positive.")
    targets = sorted((ROOT / "essays").glob("*.md"))
    unknown = set(args.slugs) - {p.stem for p in targets}
    if unknown:
        parser.error(f"Unknown essay slugs: {', '.join(sorted(unknown))}")
    if args.slugs:
        targets = [p for p in targets if p.stem in args.slugs]
    if not targets:
        parser.error("No essays found.")
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    manifest = read_manifest()
    pending = []
    for path in targets:
        old = manifest.get(path.stem, {})
        audio = AUDIO_DIR / f"{path.stem}.mp3"
        fresh = (audio.exists() and old.get("fingerprint") == fingerprint(path.read_bytes(), args.voice, args.speed)
                 and old.get("audio_sha256") == hashlib.sha256(audio.read_bytes()).hexdigest())
        if fresh and not args.force:
            print(f"Skipping {path.stem} (current)", flush=True)
        else:
            pending.append(path)
    if not pending:
        return
    ensure_models(args.model_dir)
    print(f"Generating {len(pending)} essays with {args.voice}; {args.workers} worker(s).", flush=True)
    with ProcessPoolExecutor(max_workers=args.workers, initializer=initialize_worker,
                             initargs=(str(args.model_dir), args.threads)) as pool:
        futures = [pool.submit(synthesize, path, args.voice, args.speed) for path in pending]
        for future in as_completed(futures):
            slug, record = future.result()
            manifest[slug] = record
            temporary = MANIFEST_PATH.with_suffix(".json.part")
            temporary.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            os.replace(temporary, MANIFEST_PATH)
            print(f"Saved {slug}: {record['duration_seconds'] / 60:.1f} minutes", flush=True)


if __name__ == "__main__":
    main()
