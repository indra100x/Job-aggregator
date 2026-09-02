from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .company import Company
from .source import Source
from .tag import Tag


@dataclass
class Job:
    external_id: str
    title: str
    company: Company
    source: Source
    url: str
    category: str|None

    location: Optional[str] = None
    salary: Optional[str] = None
    job_type: Optional[str] = None

    tags: list[Tag] = field(default_factory=list)

    description: str = ""

    posted_at: Optional[datetime] = None
    fetched_at: Optional[datetime] = None

    @property
    def unique_key(self) -> tuple[str, str]:
        return (self.source.name, self.external_id)