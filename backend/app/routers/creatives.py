import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.constants.common import DateRange
from app.constants.creatives import DEFAULT_FILTER_OPTIONS, METRICS_DATA_GRID_COLUMNS
from app.dependencies import get_creatives_storage
from app.models.creatives import FormattedMetrics, MetricsDataGridConfig
from app.storage.creatives import Creatives

router = APIRouter(
    prefix="/api/customer/{customer}/creatives",
    tags=["Creatives"],
)


@router.get("/{event}/metrics", response_model=MetricsDataGridConfig)
async def get_creative_metrics(
    customer: str,
    event: str,
    start_date: datetime.date,
    end_date: datetime.date,
    currency_sign: str = "€",
    round_to: int = 2,
    creatives_storage: Creatives = Depends(get_creatives_storage),
) -> MetricsDataGridConfig:
    columns = METRICS_DATA_GRID_COLUMNS

    rows = [
        metrics
        async for metrics in creatives_storage.fetch_metrics(
            customer_name=customer,
            event=event,
            date_range=DateRange(start_date, end_date),
        )
    ]

    formatted_metrics = [
        FormattedMetrics.from_metrics(row, currency_sign, round_to, row_id)
        for row_id, row in enumerate(rows, start=1)
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
    creatives_storage: Creatives = Depends(get_creatives_storage),
) -> FilterOptionsWithDefaults:
    options = await creatives_storage.fetch_filter_options(customer_name=customer)

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
