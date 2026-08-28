import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any

from .base import JobSource

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, sources: List[JobSource], max_workers: int = 5):
        self.sources = sources
        self.max_workers = max_workers

    def aggregate_jobs(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_source = {
                executor.submit(source.fetch_jobs): source
                for source in self.sources
            }

            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    jobs = future.result()
                except Exception as e:
                    logger.error(f"[{source.name}] Unexpected error: {e}")
                    continue

                logger.info(f"[{source.name}] Contributed {len(jobs)} jobs")
                all_jobs.extend(jobs)

        logger.info(f"Aggregated {len(all_jobs)} jobs from {len(self.sources)} sources")
        return all_jobs