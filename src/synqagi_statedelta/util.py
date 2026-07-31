from __future__ import annotations

from typing import Any, Iterable


def get_path(data: Any, path: str) -> Any:
    """Resolve a dotted path in nested dictionaries and lists."""
    current = data
    for token in path.split("."):
        if isinstance(current, dict):
            if token not in current:
                raise KeyError(path)
            current = current[token]
        elif isinstance(current, list):
            try:
                current = current[int(token)]
            except (ValueError, IndexError) as exc:
                raise KeyError(path) from exc
        else:
            raise KeyError(path)
    return current


def first_present(data: dict[str, Any], paths: Iterable[str]) -> tuple[str, Any] | None:
    for path in paths:
        try:
            return path, get_path(data, path)
        except KeyError:
            continue
    return None


def major_version(version: str) -> int:
    head, _, _ = version.partition(".")
    if not head.isdigit():
        raise ValueError(f"Invalid semantic version: {version!r}")
    return int(head)
