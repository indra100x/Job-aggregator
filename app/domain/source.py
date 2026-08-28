from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    display_name: str
    base_url: str