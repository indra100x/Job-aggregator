

import logging
import re

from app.domain.job import Job


logger = logging.getLogger(__name__)


class Deduplicator:
    

    VALID_STRATEGIES = {"source_id", "content"}

    def deduplicate(
        self,
        jobs: list[Job],
        strategy: str = "source_id",
    ) -> list[Job]:
        
        if not isinstance(jobs, list):
            raise TypeError(
                f"Expected list[Job], "
                f"got {type(jobs).__name__}"
            )

        if strategy not in self.VALID_STRATEGIES:
            raise ValueError(
                f"Unsupported deduplication strategy: "
                f"{strategy!r}. "
                f"Expected one of {self.VALID_STRATEGIES}"
            )

        seen: set[tuple] = set()
        unique_jobs: list[Job] = []
        duplicates = 0

        for index, job in enumerate(jobs):

            if not isinstance(job, Job):
                raise TypeError(
                    f"Invalid job at index {index}: "
                    f"expected Job, "
                    f"got {type(job).__name__}"
                )

            key = self._build_key(job, strategy)

            
            if key is None:
                logger.warning(
                    "Job at index %d has insufficient "
                    "identity information; keeping it.",
                    index,
                )

                unique_jobs.append(job)
                continue

            if key in seen:
                duplicates += 1

                logger.debug(
                    "Duplicate job skipped: "
                    "strategy=%s, key=%s",
                    strategy,
                    key,
                )

                continue

            seen.add(key)
            unique_jobs.append(job)

        logger.info(
            "Deduplication completed: "
            "strategy=%s, input=%d, unique=%d, duplicates=%d",
            strategy,
            len(jobs),
            len(unique_jobs),
            duplicates,
        )

        return unique_jobs

    def _build_key(
        self,
        job: Job,
        strategy: str,
    ) -> tuple | None:
        """Build the identity key for a job."""

        if strategy == "source_id":
            source_name = self._normalize_text(
                job.source.name
            )

            external_id = self._normalize_text(
                job.external_id
            )

            if not source_name or not external_id:
                return None

            return (
                source_name,
                external_id,
            )

        return self._content_key(job)

    @staticmethod
    def _normalize_text(
        value: str | None,
    ) -> str:
        """Normalize text for comparison."""

        if not value:
            return ""

        value = value.lower().strip()
        value = re.sub(r"\s+", " ", value)

        return value

    def _content_key(
        self,
        job: Job,
    ) -> tuple[str, str, str] | None:
        

        company = self._normalize_text(
            job.company.name
        )

        title = self._normalize_text(
            job.title
        )

        location = self._normalize_text(
            job.location
        )

      
        if not company or not title or not location:
            return None

        return (
            company,
            title,
            location,
        )

