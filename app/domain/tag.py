from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    value: str