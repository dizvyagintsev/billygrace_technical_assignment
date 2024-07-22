import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_creatives_repository
from app.repository.creatives.creatives import Creatives
from app.repository.creatives.schemas import DateRange, Metrics
from app.routers.creatives.constants import (
    DEFAULT_FILTER_OPTIONS,
    METRICS_DATA_GRID_COLUMNS,
)
from app.routers.creatives.models import FormattedMetrics, MetricsDataGridConfig

router = APIRouter(
    prefix="/api/customer/{customer}/creatives",
    tags=["Creatives"],
)


def format_metrics(
    metrics: Metrics, currency_sign: str, round_to: int, row_id: int
) -> FormattedMetrics:
    return FormattedMetrics(
        id=row_id,
        ad_copy=metrics.ad_copy.replace("['", "").replace("']", "").strip(),
        spend=f"{currency_sign}{round(metrics.spend, round_to):,}",
        clicks=f"{int(metrics.clicks):,}",
        impressions=f"{int(metrics.impressions):,}",
        sessions=f"{int(metrics.sessions):,}",
        roas=f"{round(metrics.roas, round_to)}%",
    )


@router.get("/{event}/metrics", response_model=MetricsDataGridConfig)
async def get_creative_metrics(
    customer: str,
    event: str,
    start_date: datetime.date,
    end_date: datetime.date,
    currency_sign: str = "€",
    round_to: int = 2,
    creative_repository: Creatives = Depends(get_creatives_repository),
) -> MetricsDataGridConfig:
    columns = METRICS_DATA_GRID_COLUMNS

    metrics = [
        metrics
        async for metrics in creative_repository.fetch_metrics(
            customer_name=customer,
            event=event,
            date_range=DateRange(start_date, end_date),
        )
    ]

    formatted_metrics = [
        format_metrics(metrics, currency_sign, round_to, i)
        for i, metrics in enumerate(metrics, start=1)
    ]

    return MetricsDataGridConfig(columns=columns, rows=formatted_metrics)


class FilterOptionsWithDefaults(BaseModel):
    events: list[str]
    date_range: Optional[DateRange]
    default_event: Optional[str]
    default_date_range: Optional[DateRange]


@router.get("/filter-options", response_model=Optional[FilterOptionsWithDefaults])
async def get_filter_options(
    customer: str,
    creatives_repository: Creatives = Depends(get_creatives_repository),
) -> FilterOptionsWithDefaults:
    options = await creatives_repository.fetch_filter_options(customer_name=customer)

    if not options.events or not options.date_range:
        return FilterOptionsWithDefaults(
            events=[], date_range=None, default_event=None, default_date_range=None
        )

    default_start_date = DEFAULT_FILTER_OPTIONS.date_range.start
    default_end_date = DEFAULT_FILTER_OPTIONS.date_range.end

    if options.date_range.start and options.date_range.start > default_start_date:
        default_start_date = options.date_range.start
    if options.date_range.end and options.date_range.end < default_end_date:
        default_end_date = options.date_range.end

    return FilterOptionsWithDefaults(
        events=options.events,
        date_range=options.date_range,
        default_event=DEFAULT_FILTER_OPTIONS.event
        if DEFAULT_FILTER_OPTIONS.event in options.events
        else options.events[0],
        default_date_range=DateRange(start=default_start_date, end=default_end_date),
    )
