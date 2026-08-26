"""Create the distributable ZIP beside the R16 release-package directory."""

from __future__ import annotations

import os
import zipfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parents[1]
TARGET = PACKAGE.with_suffix(".zip")


def long_root() -> Path:
    if os.name == "nt" and not str(PACKAGE).startswith("\\\\?\\"):
        return Path("\\\\?\\" + str(PACKAGE))
    return PACKAGE


def included(relative: Path) -> bool:
    if relative.parts and relative.parts[0] == "tmp":
        return False
    if "__pycache__" in relative.parts or relative.suffix == ".pyc":
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
    temporary = TARGET.with_suffix(".zip.tmp")
    if temporary.exists():
        temporary.unlink()
    files = iter_files()
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, relative in files:
            archive.write(path, (Path(PACKAGE.name) / relative).as_posix())
    temporary.replace(TARGET)
    print(f"ZIP_BUILD_PASS files={len(files)} path={TARGET}")


if __name__ == "__main__":
    main()
