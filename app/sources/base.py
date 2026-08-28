from abc import ABC, abstractmethod
from typing import List, Dict, Any


class JobSource(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the job source."""
        pass

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Fetch jobs from the source."""
        pass