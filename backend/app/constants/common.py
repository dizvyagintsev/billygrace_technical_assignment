import datetime
from dataclasses import dataclass


@dataclass
class DateRange:
    start: datetime.date
    end: datetime.date
