import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

import requests

logger = logging.getLogger(__name__)


class JobSource(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the job source."""
        pass

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """Fetch jobs from the source. Should not raise; return [] on failure."""
        pass

    def _get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> Optional[requests.Response]:
        """Shared GET with logging/error handling. Returns None on failure."""
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.name}] Request failed: {e}")
            return None

    def _normalize(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Attach the source name to a job dict."""
        job.setdefault("source", self.name)
        return job