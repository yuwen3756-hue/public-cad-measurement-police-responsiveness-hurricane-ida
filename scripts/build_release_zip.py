"""Create the distributable public R16.2 ZIP beside the repository."""

from __future__ import annotations

import os
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
TARGET = PACKAGE.parent / f"{PACKAGE.name}-r16-2.zip"

PRIVATE_ONLY_MARKERS = tuple(
    value.encode("ascii").lower()
    for value in (
        "LA" + "PD",
        "PRIVATE" + "_R16_2",
        "LA" + "PD_EXTRACT_ROOT",
        "beland ppt" + "_260521_164810",
        "May 2026" + " seminar deck",
        "Online_Reviewer" + "\\R16_2",
    )
)
PUBLIC_TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".html",
    ".json",
    ".lean",
    ".md",
    ".ps1",
    ".py",
    ".sha256",
    ".tex",
    ".toml",
    ".txt",
}


def long_root() -> Path:
    if os.name == "nt" and not str(PACKAGE).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(PACKAGE))
    return PACKAGE


def included(relative: Path) -> bool:
    if relative.parts and relative.parts[0] in {".git", "tmp"}:
        return False
    if "__pycache__" in relative.parts or relative.suffix == ".pyc":
        return False
    return True


def assert_public_only(files: list[tuple[Path, Path]]) -> None:
    for path, relative in files:
        relative_bytes = relative.as_posix().encode("utf-8").lower()
        if any(marker in relative_bytes for marker in PRIVATE_ONLY_MARKERS):
            raise RuntimeError(f"private-only filename entered public ZIP inputs: {relative}")
        if path.suffix.lower() in PUBLIC_TEXT_SUFFIXES:
            payload = path.read_bytes().lower()
            if any(marker in payload for marker in PRIVATE_ONLY_MARKERS):
                raise RuntimeError(f"private-only content entered public ZIP inputs: {relative}")


def iter_files() -> list[tuple[Path, Path]]:
    root = long_root()
    files: list[tuple[Path, Path]] = []
    for directory, child_dirs, names in os.walk(root):
        relative_directory = Path(directory).relative_to(root)
        child_dirs[:] = [
            name for name in child_dirs
            if included(relative_directory / name)
        ]
        for name in names:
            relative = relative_directory / name
            if included(relative):
                files.append((Path(directory) / name, relative))
    return sorted(files, key=lambda item: item[1].as_posix())


def main() -> None:
    temporary = TARGET.with_suffix(".zip.tmp")
    if temporary.exists():
        temporary.unlink()
    files = iter_files()
    assert_public_only(files)
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, relative in files:
            archive.write(path, (Path(PACKAGE.name) / relative).as_posix())
    temporary.replace(TARGET)
    print(f"ZIP_BUILD_PASS files={len(files)} path={TARGET}")


if __name__ == "__main__":
    main()
