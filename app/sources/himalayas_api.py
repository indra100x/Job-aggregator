import logging
from typing import List, Dict, Any, Optional

from .base import JobSource

logger = logging.getLogger(__name__)


class HimalayasAPI(JobSource):

    BASE_URL = "https://himalayas.app/jobs/api"

    @property
    def name(self) -> str:
        return "himalayas_api"

    def fetch_jobs(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset

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