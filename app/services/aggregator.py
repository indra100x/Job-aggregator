import logging
from typing import List, Dict, Any

from app.sources.base import JobSource

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, sources: List[JobSource]):
        self.sources = sources

    def aggregate_jobs(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []

        for source in self.sources:
            try:
                jobs = source.fetch_jobs()
            except Exception as e:
               
                logger.error(f"[{source.name}] Unexpected error: {e}")
                continue

            logger.info(f"[{source.name}] Contributed {len(jobs)} jobs")
            all_jobs.extend(jobs)

        logger.info(f"Aggregated {len(all_jobs)} jobs from {len(self.sources)} sources")
        return all_jobs