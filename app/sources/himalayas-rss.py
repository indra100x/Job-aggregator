import logging
import feedparser
from typing import List, Dict, Any

from .base import JobSource

logger = logging.getLogger(__name__)


class HimalayasRSS(JobSource):

    FEED_URL = "https://himalayas.app/jobs/rss"

    @property
    def name(self) -> str:
        return "himalayas_rss"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        response = self._get(self.FEED_URL)
        if response is None:
            return []

        feed = feedparser.parse(response.content)

        if feed.bozo:
            logger.warning(
                f"[{self.name}] Feed parsed with issues: {feed.bozo_exception}"
            )
            if not feed.entries:
                return []

        jobs: List[Dict[str, Any]] = []
        for entry in feed.entries:
            jobs.append(self._normalize({
                "title": entry.get("title"),
                "description": entry.get("description"),
                "url": entry.get("link"),
                "published_at": entry.get("published"),
            }))

        logger.info(f"[{self.name}] Fetched {len(jobs)} jobs")
        return jobs