from __future__ import annotations

from pathlib import Path


def weighted_waveform_average(
    inputs: list[Path], output: Path, weights: list[float] | None = None
) -> Path:
    if len(inputs) < 2:
        raise ValueError("At least two input stems are required")
    try:
        import numpy as np
        import soundfile as sf
    except ImportError as exc:
        raise RuntimeError(
            'Install ensemble support with: pip install "omnistem[ensemble]"'
        ) from exc

    weights = weights or [1.0] * len(inputs)
    if len(weights) != len(inputs) or sum(weights) <= 0:
        raise ValueError("Weights must match inputs and sum to more than zero")

    arrays = []
    sample_rate = None
    shape = None
    for path in inputs:
        audio, rate = sf.read(path, always_2d=True, dtype="float32")
        if sample_rate is None:
            sample_rate, shape = rate, audio.shape
        if rate != sample_rate or audio.shape != shape:
            raise ValueError("All stems must have the same sample rate, channels, and duration")
        arrays.append(audio)

    normalized = np.asarray(weights, dtype=np.float32)
    normalized /= normalized.sum()
    mixed = np.zeros_like(arrays[0])
    for weight, audio in zip(normalized, arrays, strict=True):
        mixed += audio * weight
    output.parent.mkdir(parents=True, exist_ok=True)
    sf.write(output, mixed, sample_rate, subtype="FLOAT")
    return output
