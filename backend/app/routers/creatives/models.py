from typing import List

from pydantic import BaseModel


class FormattedMetrics(BaseModel):
    id: int
    ad_copy: str
    spend: str
    clicks: str
    impressions: str
    sessions: str
    roas: str


class Column(BaseModel):
    field: str
    headerName: str
    flex: int
    headerAlign: str
    align: str


class MetricsDataGridConfig(BaseModel):
    columns: List[Column]
    rows: List[FormattedMetrics]
