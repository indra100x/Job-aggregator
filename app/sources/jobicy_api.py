import logging
from typing import Any, Dict, List, Optional

from .base import JobSource

logger = logging.getLogger(__name__)


class JobicyAPI(JobSource):

    BASE_URL = "https://jobicy.com/api/v2/remote-jobs"

    @property
    def name(self) -> str:
        return "jobicy_api"

    def fetch_jobs(
        self,
        count: Optional[int] = None,
        geo: Optional[str] = None,
        industry: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if count:
            params["count"] = count
        if geo:
            params["geo"] = geo
        if industry:
            params["industry"] = industry
        if tag:
            params["tag"] = tag

        response = self._get(self.BASE_URL, params=params)
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