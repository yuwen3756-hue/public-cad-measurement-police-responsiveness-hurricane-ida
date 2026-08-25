"""Build the deterministic SHA-256 manifest for the R14 release package."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = PACKAGE / "PACKAGE_MANIFEST.sha256"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def long_root() -> Path:
    if os.name == "nt" and not str(PACKAGE).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(PACKAGE))
    return PACKAGE


def included(relative: Path) -> bool:
    if relative == Path("PACKAGE_MANIFEST.sha256"):
        return False
    if relative.parts and relative.parts[0] == "tmp":
        return False
    if "__pycache__" in relative.parts or relative.suffix == ".pyc":
        return False
    if relative.suffix.lower() == ".zip":
        return False
    return True


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
    lines = [
        f"{sha256(path)}  {relative.as_posix()}"
        for path, relative in iter_files()
    ]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"MANIFEST_BUILD_PASS files={len(lines)}")


if __name__ == "__main__":
    main()
