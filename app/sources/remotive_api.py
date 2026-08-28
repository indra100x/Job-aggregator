import logging
from typing import Any, Dict, List

from .base import JobSource

logger = logging.getLogger(__name__)


class RemotiveAPI(JobSource):

    BASE_URL = "https://remotive.com/api/remote-jobs"

    @property
    def name(self) -> str:
        return "remotive_api"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        response = self._get(self.BASE_URL)
        if response is None:
            return []

        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"[{self.name}] Invalid JSON: {e}")
            return []

        jobs = data.get("jobs", [])
        logger.info(f"[{self.name}] Fetched {len(jobs)} jobs")
        return [self._normalize(job) for job in jobs]