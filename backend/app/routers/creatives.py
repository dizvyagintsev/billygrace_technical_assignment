import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies import get_creatives_storage
from app.storage.creatives import Event, DateRange, RawMetrics, Creatives

router = APIRouter(
    prefix="/customer/{customer}/creatives/{event}",
    tags=["Creatives"],
)


class Metrics(BaseModel):
    ad_copy: str
    spend: str
    clicks: str
    impressions: str
    sessions: str
    roas: str

    @classmethod
    def from_raw_metrics(
        cls, raw_metrics: RawMetrics, currency_sign, round_to
    ) -> "Metrics":
        return cls(
            ad_copy=raw_metrics.ad_copy.replace("['", "").replace("']", "").strip(),
            spend=f"{currency_sign}{round(raw_metrics.spend, round_to):,}",
            clicks=f"{int(raw_metrics.clicks):,}",
            impressions=f"{int(raw_metrics.impressions):,}",
            sessions=f"{int(raw_metrics.sessions):,}",
            roas=f"{round(raw_metrics.roas, 2)}%",
        )


@router.get("/metrics", response_model=list[Metrics])
async def get_creative_metrics(
    customer: str,
    event: Event,
    start_date: datetime.date,
    end_date: datetime.date,
    currency_sign: str = "€",
    round_to: int = 2,
    creatives_storage: Creatives = Depends(get_creatives_storage),
):
    return [
        Metrics.from_raw_metrics(metrics, currency_sign, round_to)
        async for metrics in creatives_storage.fetch_metrics(
            customer_name=customer,
            event=event,
            date_range=DateRange(start_date, end_date),
        )
    ]
