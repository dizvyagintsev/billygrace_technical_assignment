import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_creatives_storage
from app.storage.creatives import DateRange, Metrics, Creatives

router = APIRouter(
    prefix="/api/customer/{customer}/creatives",
    tags=["Creatives"],
)


class FormattedMetrics(BaseModel):
    id: int
    ad_copy: str
    spend: str
    clicks: str
    impressions: str
    sessions: str
    roas: str

    @classmethod
    def from_metrics(
        cls, metrics: Metrics, currency_sign: str, round_to: int, id: int
    ) -> "FormattedMetrics":
        return cls(
            id=id,
            ad_copy=metrics.ad_copy.replace("['", "").replace("']", "").strip(),
            spend=f"{currency_sign}{round(metrics.spend, round_to):,}",
            clicks=f"{int(metrics.clicks):,}",
            impressions=f"{int(metrics.impressions):,}",
            sessions=f"{int(metrics.sessions):,}",
            roas=f"{round(metrics.roas, round_to)}%",
        )


class Column(BaseModel):
    field: str
    headerName: str
    flex: int
    headerAlign: str
    align: str


class MetricsDataGridConfig(BaseModel):
    columns: List[Column]
    rows: List[FormattedMetrics]


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
    columns = [
        Column(field='ad_copy', headerName='Ad Copy', flex=3, headerAlign='center', align='center'),
        Column(field='spend', headerName='Spend', flex=1, headerAlign='center', align='center'),
        Column(field='clicks', headerName='Clicks', flex=1, headerAlign='center', align='center'),
        Column(field='impressions', headerName='Impressions', flex=1, headerAlign='center', align='center'),
        Column(field='sessions', headerName='Sessions', flex=1, headerAlign='center', align='center'),
        Column(field='roas', headerName='ROAS', flex=1, headerAlign='center', align='center'),
    ]

    rows = [
        metrics async for metrics in creatives_storage.fetch_metrics(
            customer_name=customer,
            event=event,
            date_range=DateRange(start_date, end_date)
        )
    ]

    formatted_metrics = [
        FormattedMetrics.from_metrics(row, currency_sign, round_to, row_id)
        for row_id, row in enumerate(rows, start=1)
    ]

    return MetricsDataGridConfig(columns=columns, rows=formatted_metrics)


class FilterOptions(BaseModel):
    events: list[str]
    date_range: Optional[DateRange]
    default_event: Optional[str]
    default_date_range: Optional[DateRange]


@router.get("/filter-options", response_model=Optional[FilterOptions])
async def get_filter_options(
        customer: str,
        creatives_storage: Creatives = Depends(get_creatives_storage),
) -> FilterOptions:
    options = await creatives_storage.get_filter_options(customer_name=customer)

    if not options.events:
        return FilterOptions(events=[], date_range=None, default_event=None, default_date_range=None)

    default_start_date = datetime.date(2024, 5, 15)
    default_end_date = datetime.date(2024, 7, 5)

    if options.date_range:
        if options.date_range.start and options.date_range.start > default_start_date:
            default_start_date = options.date_range.start
        if options.date_range.end and options.date_range.end < default_end_date:
            default_end_date = options.date_range.end

    if default_start_date > default_end_date:
        default_start_date, default_end_date = default_end_date, default_start_date

    return FilterOptions(
        events=options.events,
        date_range=options.date_range,
        default_event="order_completed" if "order_completed" in options.events else options.events[0],
        default_date_range=DateRange(start=default_start_date, end=default_end_date)
    )
