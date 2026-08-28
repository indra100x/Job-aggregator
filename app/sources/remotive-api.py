import requests
from typing import List, Dict, Any

from .base import JobSource


class RemotiveAPI(JobSource):

    BASE_URL = "https://remotive.com/api/remote-jobs"

    @property
    def name(self) -> str:
        return "remotive_api"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        response = requests.get(
            self.BASE_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])