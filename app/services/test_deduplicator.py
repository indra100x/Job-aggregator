
import os
import sys

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from app.domain.job import Job
from app.domain.company import Company
from app.domain.source import Source
from app.services.deduplicator import Deduplicator


REMOTIVE_SOURCE = Source(
    name="remotive_api",
    display_name="Remotive",
    base_url="https://remotive.com",
)

HIMALAYAS_SOURCE = Source(
    name="himalayas_api",
    display_name="Himalayas",
    base_url="https://himalayas.app",
)


job1 = Job(
    external_id="123",
    title="Python Developer",
    company=Company(name="Google"),
    source=REMOTIVE_SOURCE,
    url="https://remotive.com/123",
    location="Remote",
)

job2 = Job(
    external_id="abc-999",
    title=" python developer ",
    company=Company(name=" GOOGLE "),
    source=HIMALAYAS_SOURCE,
    url="https://himalayas.app/abc-999",
    location=" remote ",
)


def main() -> None:
    deduplicator = Deduplicator()

    unique_jobs = deduplicator.deduplicate(
        [job1, job2],
        strategy="content",
    )

    print(f"Input jobs: 2")
    print(f"Unique jobs: {len(unique_jobs)}")
    print()

    for job in unique_jobs:
        print(
            f"source={job.source.name} "
            f"external_id={job.external_id} "
            f"title={job.title} "
            f"company={job.company.name} "
            f"location={job.location}"
        )


if __name__ == "__main__":
    main()

