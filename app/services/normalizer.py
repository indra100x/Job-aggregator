import html
import logging
import re

from datetime import datetime, timezone
from typing import Any, Callable

from app.domain import Job, Company, Source, Tag


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_html(text: str | None) -> str:
 
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def _format_salary(
    min_salary: float | None,
    max_salary: float | None,
    period: str | None,
    currency: str | None,
) -> str | None:
   

    if min_salary is None and max_salary is None:
        return None

    currency = currency or ""

    if (
        min_salary is not None
        and max_salary is not None
        and min_salary != max_salary
    ):
        amount = (
            f"{currency}{min_salary:,.0f} - "
            f"{currency}{max_salary:,.0f}"
        )
    else:
        value = max_salary if max_salary is not None else min_salary
        amount = f"{currency}{value:,.0f}"

    if period:
        amount += f" / {period}"

    return amount


def _epoch_to_datetime(
    epoch: int | float | None,
) -> datetime | None:
    """Convert a Unix timestamp into a UTC datetime."""
    if epoch is None:
        return None

    try:
        return datetime.fromtimestamp(
            epoch,
            tz=timezone.utc,
        )
    except (ValueError, OSError, OverflowError, TypeError):
        return None


def _string_to_datetime(
    value: str | None,
) -> datetime | None:
 
    if not value:
        return None

    try:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except (ValueError, TypeError):
        return None


def _make_tags(values: list[str] | None) -> list[Tag]:
    """Convert raw tag strings into Tag domain objects."""
    if not values:
        return []

    return [
        Tag(value=value.strip())
        for value in values
        if isinstance(value, str) and value.strip()
    ]


# ---------------------------------------------------------------------------
# Source definitions
# ---------------------------------------------------------------------------

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

JOBICY_SOURCE = Source(
    name="jobicy_api",
    display_name="Jobicy",
    base_url="https://jobicy.com",
)


# ---------------------------------------------------------------------------
# Source-specific normalizers
# ---------------------------------------------------------------------------

def _normalize_remotive(job: dict[str, Any]) -> Job:
    

    return Job(
        external_id=str(job.get("id", "")),
        title=job.get("title", ""),

        company=Company(
            name=job.get("company_name", ""),
        ),

        source=REMOTIVE_SOURCE,

        url=job.get("url", ""),

        location=job.get(
            "candidate_required_location"
        ) or None,

        salary=job.get("salary") or None,

        job_type=job.get("job_type") or None,

        tags=_make_tags(
            job.get("tags")
        ),

        description=_strip_html(
            job.get("description")
        ),

        posted_at=_string_to_datetime(
            job.get("publication_date")
        ),
    )


def _normalize_himalayas(job: dict[str, Any]) -> Job:
    

    location_list = job.get(
        "locationRestrictions"
    ) or []

    categories = job.get(
        "categories"
    ) or []

    external_id = (
        job.get("guid")
        or job.get("applicationLink")
        or ""
    )

    return Job(
        external_id=str(external_id),

        title=job.get("title", ""),

        company=Company(
            name=job.get("companyName", ""),
            slug=job.get("companySlug"),
        ),

        source=HIMALAYAS_SOURCE,

        url=job.get("applicationLink", ""),

        location=(
            ", ".join(location_list)
            if location_list
            else "Worldwide"
        ),

        salary=_format_salary(
            job.get("minSalary"),
            job.get("maxSalary"),
            job.get("salaryPeriod"),
            job.get("currency"),
        ),

        job_type=job.get(
            "employmentType"
        ) or None,

        tags=_make_tags(
            categories
        ),

        description=_strip_html(
            job.get("description")
        ),

        posted_at=_epoch_to_datetime(
            job.get("pubDate")
        ),
    )


def _normalize_jobicy(job: dict[str, Any]) -> Job:
    

    industries = job.get(
        "jobIndustry"
    ) or []

    job_types = job.get(
        "jobType"
    ) or []

    return Job(
        external_id=str(
            job.get("id", "")
        ),

        title=job.get(
            "jobTitle",
            "",
        ),

        company=Company(
            name=job.get(
                "companyName",
                "",
            ),
        ),

        source=JOBICY_SOURCE,

        url=job.get(
            "url",
            "",
        ),

        location=job.get(
            "jobGeo",
            "",
        ) or None,

        salary=_format_salary(
            job.get("salaryMin"),
            job.get("salaryMax"),
            job.get("salaryPeriod"),
            job.get("salaryCurrency"),
        ),

        job_type=(
            ", ".join(job_types)
            if job_types
            else None
        ),

        tags=_make_tags(
            industries
        ),

        description=_strip_html(
            job.get("jobDescription")
        ),

        posted_at=_string_to_datetime(
            job.get("pubDate")
        ),
    )


# ---------------------------------------------------------------------------
# Normalizer registry
# ---------------------------------------------------------------------------

_NORMALIZERS: dict[str, Callable[[dict[str, Any]], Job]] = {
    "remotive_api": _normalize_remotive,
    "himalayas_api": _normalize_himalayas,
    "jobicy_api": _normalize_jobicy,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def normalize_job(job: dict[str, Any]) -> Job:
   

    source = job.get("source")

    normalizer = _NORMALIZERS.get(source)

    if normalizer is None:
        raise ValueError(
            f"No normalizer registered for source: {source!r}"
        )

    return normalizer(job)


def normalize_jobs(
    jobs: list[dict[str, Any]],
) -> list[Job]:
    

    normalized: list[Job] = []

    for job in jobs:
        try:
            normalized.append(
                normalize_job(job)
            )

        except Exception as exc:
            logger.warning(
                "Skipping unnormalizable job "
                "(source=%s): %s",
                job.get("source"),
                exc,
            )

    return normalized
