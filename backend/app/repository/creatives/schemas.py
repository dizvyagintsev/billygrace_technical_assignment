import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class DateRange:
    start: datetime.date
    end: datetime.date


@dataclass(frozen=True)
class Metrics:
    ad_copy: str
    spend: float
    clicks: float
    impressions: float
    sessions: float
    roas: float


@dataclass
class FilterOptions:
    events: List[str]
    date_range: Optional[DateRange] = None
