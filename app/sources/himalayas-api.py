import requests
from typing import List, Dict, Any

from .base import JobSource


class HimalayasAPI(JobSource):

    BASE_URL = "https://himalayas.app/jobs/api"

    @property
    def name(self) -> str:
        return "himalayas_api"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        response = requests.get(
            self.BASE_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])