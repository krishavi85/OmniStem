from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class ProcessOutput:
    return_code: int
    stdout: str
    stderr: str


async def run_command(
    command: list[str],
    on_line: Callable[[str], None] | None = None,
) -> ProcessOutput:
    if not command or not command[0]:
        raise ValueError("Command must contain an executable")

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout_lines: list[str] = []
    stderr_lines: list[str] = []

    async def consume(stream: asyncio.StreamReader | None, target: list[str]) -> None:
        if stream is None:
            return
        while True:
            raw = await stream.readline()
            if not raw:
                break
            line = raw.decode(errors="replace").rstrip()
            target.append(line)
            if on_line:
                on_line(line)

    await asyncio.gather(
        consume(process.stdout, stdout_lines), consume(process.stderr, stderr_lines)
    )
    return_code = await process.wait()
    return ProcessOutput(return_code, "\n".join(stdout_lines), "\n".join(stderr_lines))
