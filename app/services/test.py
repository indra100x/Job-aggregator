"""Utility script to test the job aggregator and normalizer.

Run this script to:
1. Fetch jobs from all configured sources.
2. Print a sample of raw aggregated jobs.
3. Optionally write raw jobs to a JSON file.
4. Optionally normalize jobs and write them as JSONL.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from typing import Any

# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


# ---------------------------------------------------------------------------
# Project imports
# ---------------------------------------------------------------------------

from app.services.aggregator import Aggregator
from app.services.normalizer import normalize_jobs
from app.services.deduplicator import Deduplicator
from app.sources.himalayas_api import HimalayasAPI
from app.sources.jobicy_api import JobicyAPI
from app.sources.remotive_api import RemotiveAPI


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def job_to_dict(job: Any) -> dict:
    """Convert a dataclass-based object into a JSON-serializable dictionary."""
    return asdict(job)


def print_raw_jobs(jobs: list[dict], limit: int = 10) -> None:
    """Print a sample of raw aggregated jobs grouped by source."""

    grouped: dict[str, list[dict]] = {}

    for job in jobs:
        source = job.get("source", "unknown")
        grouped.setdefault(source, []).append(job)

    for source, source_jobs in grouped.items():

        print(
            f"=== Source: {source} "
            f"({len(source_jobs)} jobs) ===\n"
        )

        for i, job in enumerate(
            source_jobs[:limit],
            start=1,
        ):
            print(f"--- {source} Job {i} ---")

            print(
                json.dumps(
                    job,
                    indent=2,
                    ensure_ascii=False,
                )
            )

            print()


def write_raw_jobs(
    path: str,
    jobs: list[dict],
    limit: int = 10,
) -> None:
    """Write a sample of raw aggregated jobs to a JSON file."""

    dirpath = os.path.dirname(path)

    if dirpath:
        os.makedirs(
            dirpath,
            exist_ok=True,
        )

    grouped: dict[str, list[dict]] = {}

    for job in jobs:
        source = job.get("source", "unknown")
        grouped.setdefault(source, []).append(job)

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as fh:

        fh.write(
            f"Total jobs aggregated: {len(jobs)}\n\n"
        )

        for source, source_jobs in grouped.items():

            fh.write(
                f"=== Source: {source} "
                f"({len(source_jobs)} jobs) ===\n\n"
            )

            for i, job in enumerate(
                source_jobs[:limit],
                start=1,
            ):

                fh.write(
                    f"--- {source} Job {i} ---\n"
                )

                fh.write(
                    json.dumps(
                        job,
                        indent=2,
                        ensure_ascii=False,
                    )
                )

                fh.write("\n\n")


def print_normalized_jobs(
    jobs: list,
    limit: int = 10,
) -> None:
    """Print normalized Job domain objects."""

    print(
        f"Total normalized jobs: {len(jobs)}\n"
    )

    for i, job in enumerate(
        jobs[:limit],
        start=1,
    ):

        print(f"--- Normalized Job {i} ---")

        print(
            json.dumps(
                job_to_dict(job),
                indent=2,
                ensure_ascii=False,
                default=str,
            )
        )

        print()


def write_normalized_jobs(
    path: str,
    jobs: list,
) -> None:
    """Write a list of already-normalized Job objects as JSONL."""

    dirpath = os.path.dirname(path)

    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    with open(path, "w", encoding="utf-8") as fh:
        for job in jobs:
            fh.write(
                json.dumps(
                    job_to_dict(job),
                    ensure_ascii=False,
                    default=str,
                )
            )
            fh.write("\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:

    parser = argparse.ArgumentParser(
        description="Test the job aggregator and normalizer"
    )

    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=10,
        help="Number of jobs to print per source",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        default=None,
        help="Optional output path for raw sample jobs",
    )

    parser.add_argument(
        "--normalize-out",
        type=str,
        default="output/normalized_jobs.jsonl",
        help="Optional output path for normalized jobs (JSONL)",
    )

    parser.add_argument(
        "--unique-out",
        type=str,
        default="output/unique_jobs.jsonl",
        help="Optional output path for deduplicated unique jobs (JSONL)",
    )

    args = parser.parse_args()

    # -----------------------------------------------------------------------
    # Create sources
    # -----------------------------------------------------------------------

    sources = [
        JobicyAPI(),
        HimalayasAPI(),
        RemotiveAPI(),
    ]

    # -----------------------------------------------------------------------
    # Aggregate
    # -----------------------------------------------------------------------

    aggregator = Aggregator(sources)

    try:
        jobs = aggregator.aggregate_jobs()

    except Exception as exc:
        logger.error(
            "Aggregation failed",
            exc_info=True,
        )

        print(
            f"Aggregation failed: {exc}"
        )

        raise SystemExit(1)

    # -----------------------------------------------------------------------
    # Raw jobs
    # -----------------------------------------------------------------------

    print(
        f"Total jobs aggregated: {len(jobs)}\n"
    )

    print_raw_jobs(
        jobs,
        limit=args.limit,
    )

    # -----------------------------------------------------------------------
    # Write raw jobs
    # -----------------------------------------------------------------------

    if args.out:

        write_raw_jobs(
            args.out,
            jobs,
            limit=args.limit,
        )

        print(
            f"Wrote raw sample jobs to {args.out}"
        )

    # -----------------------------------------------------------------------
    # Normalize
    # -----------------------------------------------------------------------

    if args.normalize_out:

        normalized_jobs = normalize_jobs(jobs)

        print(
            f"\nSuccessfully normalized "
            f"{len(normalized_jobs)} / {len(jobs)} jobs."
        )

        write_normalized_jobs(
            args.normalize_out,
            normalized_jobs,
        )

        print(
            f"Wrote normalized jobs to "
            f"{args.normalize_out}"
        )

        # -------------------------------------------------------------------
        # Deduplicate normalized jobs and write unique set
        # -------------------------------------------------------------------

        if args.unique_out:

            deduper = Deduplicator()

            try:
                unique_jobs = deduper.deduplicate(normalized_jobs)

            except Exception as exc:
                logger.error("Deduplication failed", exc_info=True)
                print(f"Deduplication failed: {exc}")
                raise SystemExit(1)

            write_normalized_jobs(
                args.unique_out,
                unique_jobs,
            )

            print(
                f"Wrote deduplicated unique jobs to {args.unique_out} "
                f"({len(unique_jobs)} unique)"
            )


if __name__ == "__main__":
    main()
