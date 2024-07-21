import datetime
from dataclasses import dataclass

from app.routers.creatives.models import Column


@dataclass(frozen=True)
class DateRange:
    start: datetime.date
    end: datetime.date


@dataclass(frozen=True)
class DefaultFilterOptions:
    event: str
    date_range: DateRange


DEFAULT_FILTER_OPTIONS = DefaultFilterOptions(
    event="order_completed",
    date_range=DateRange(
        start=datetime.date(2024, 5, 15), end=datetime.date(2024, 7, 5)
    ),
)


METRICS_DATA_GRID_COLUMNS = [
    Column(
        field="ad_copy",
        headerName="Ad Copy",
        flex=3,
        headerAlign="center",
        align="center",
    ),
    Column(
        field="spend",
        headerName="Spend",
        flex=1,
        headerAlign="center",
        align="center",
    ),
    Column(
        field="clicks",
        headerName="Clicks",
        flex=1,
        headerAlign="center",
        align="center",
    ),
    Column(
        field="impressions",
        headerName="Impressions",
        flex=1,
        headerAlign="center",
        align="center",
    ),
    Column(
        field="sessions",
        headerName="Sessions",
        flex=1,
        headerAlign="center",
        align="center",
    ),
    Column(
        field="roas",
        headerName="ROAS",
        flex=1,
        headerAlign="center",
        align="center",
    ),
]
