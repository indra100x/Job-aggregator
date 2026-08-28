from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Company:
    name: str
    slug: Optional[str] = None
    logo_url: Optional[str] = None