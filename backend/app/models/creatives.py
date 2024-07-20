from typing import List

from pydantic import BaseModel

from app.storage.creatives import Metrics


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
