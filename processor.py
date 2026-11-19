from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


# Prevent Windows from showing a separate console for each FFmpeg process.
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)


@dataclass(frozen=True)
class ProcessResult:
    source: str
    clips: tuple[str, ...]


def ffprobe_duration(source: str, ffprobe: str = "ffprobe") -> float:
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", source],
        capture_output=True,
        text=True,
        check=True,
        creationflags=NO_WINDOW,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def cut_video(source: str, output_dir: str, clip_length: float,
              ffmpeg: str = "ffmpeg", progress=None) -> ProcessResult:
    source_path = Path(source)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    duration = ffprobe_duration(source, ffmpeg.replace("ffmpeg", "ffprobe"))
    count = int(duration // clip_length)
    clips: list[str] = []

    for index in range(count):
        start = index * clip_length
        output = destination / f"{source_path.stem}_clip_{index + 1:05d}.mp4"
        subprocess.run(
            [ffmpeg, "-y", "-ss", str(start), "-i", source,
             "-t", str(clip_length), "-map", "0:v:0", "-map", "0:a?",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            creationflags=NO_WINDOW,
        )
        clips.append(str(output))
        if progress:
            progress(index + 1, count)

    return ProcessResult(source=source, clips=tuple(clips))
