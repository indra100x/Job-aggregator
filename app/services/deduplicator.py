
import logging

from app.domain.job import Job


logger = logging.getLogger(__name__)


class Deduplicator:
    

    def deduplicate(self, jobs: list[Job]) -> list[Job]:
       
        if not isinstance(jobs, list):
            raise TypeError(
                f"Expected a list of Job objects, "
                f"got {type(jobs).__name__}"
            )

        seen: set[tuple[str, str]] = set()
        unique_jobs: list[Job] = []

        duplicates = 0

        for index, job in enumerate(jobs):

            if not isinstance(job, Job):
                logger.error(
                    "Invalid job at index %d: expected Job, got %s",
                    index,
                    type(job).__name__,
                )

                raise TypeError(
                    f"Invalid job at index {index}: "
                    f"expected Job, got {type(job).__name__}"
                )

            key = job.unique_key

            if key in seen:
                duplicates += 1

                logger.debug(
                    "Duplicate job skipped: "
                    "source=%s, external_id=%s",
                    job.source.name,
                    job.external_id,
                )

                continue

            seen.add(key)
            unique_jobs.append(job)

        logger.info(
            "Deduplication completed: "
            "input=%d, unique=%d, duplicates=%d",
            len(jobs),
            len(unique_jobs),
            duplicates,
        )

        return unique_jobs

