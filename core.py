from dataclasses import dataclass
from pathlib import Path
import random

@dataclass(frozen=True)
class Clip:
    source: str
    path: str


def plan_clips(duration_seconds: float, clip_length: float) -> list[tuple[float, float]]:
    """Return complete (start, duration) ranges; discard the final incomplete part."""
    if duration_seconds <= 0:
        return []
    if clip_length <= 0:
        raise ValueError("clip_length must be positive")
    count = int(duration_seconds // clip_length)
    return [(i * clip_length, clip_length) for i in range(count)]


def shuffle_clips(clips: list[Clip], seed: int | None = None) -> list[Clip]:
    """Shuffle while reducing adjacent clips from the same source."""
    rng = random.Random(seed)
    remaining = {}
    for clip in clips:
        remaining[clip.source] = remaining.get(clip.source, 0) + 1

    result = []
    last_source = None
    while remaining:
        candidates = [source for source, count in remaining.items()
                      if count > 0 and source != last_source]
        if not candidates:
            candidates = [source for source, count in remaining.items() if count > 0]
        source = rng.choice(candidates)

        pool = [clip for clip in clips if clip.source == source and clip not in result]
        result.append(rng.choice(pool))
        remaining[source] -= 1
        if remaining[source] == 0:
            del remaining[source]
        last_source = source
    return result
