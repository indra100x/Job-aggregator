import feedparser
from typing import List, Dict, Any

from .base import JobSource


class HimalayasRSS(JobSource):

    FEED_URL = "https://himalayas.app/jobs/rss"

    @property
    def name(self) -> str:
        return "himalayas_rss"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        feed = feedparser.parse(self.FEED_URL)

        jobs: List[Dict[str, Any]] = []

        for entry in feed.entries:
            jobs.append({
                "title": entry.get("title"),
                "description": entry.get("description"),
                "url": entry.get("link"),
                "published_at": entry.get("published"),
            })

        return jobs