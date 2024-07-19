import datetime
from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator

import asyncpg


class Event(Enum):
    AD_CALLS = "ad_calls"
    ADD_TO_CART = "add_to_cart"
    BEL_AFSPRAAK = "bel_afspraak"
    CHECK_STOCK = "check_stock"
    LANDINGPAGE_VISIT = "landingpage_visit"
    ORDER_COMPLETED = "order_completed"
    ORDER_COMPLETED_CV = "order_completed_cv"
    PRODUCT_VIEW = "product_view"
    SOLLICITATIE_VERZONDEN = "sollicitatie_verzonden"
    SUBSCRIBE = "subscribe"
    WINKEL_AFSPRAAK = "winkel_afspraak"


@dataclass
class DateRange:
    start: datetime.date
    end: datetime.date


@dataclass(frozen=True)
class RawMetrics:
    ad_copy: str
    spend: float
    clicks: float
    impressions: float
    sessions: float
    roas: float


class Creatives:
    def __init__(self, db: asyncpg.pool.Pool):
        self.db = db

    async def fetch_metrics(
        self, customer_name: str, event: Event, date_range: DateRange
    ) -> AsyncIterator[RawMetrics]:
        """
        Fetch metrics for a given customer, event and date range.

        :param customer_name: customer name
        :param event: event type
        :param date_range: start and end date
        :return: not formatted metrics
        """
        query = """
        WITH filtered_data AS (
    SELECT ad_id, spend, clicks, impressions, sessions, event_value
    FROM creatives.pixel_event_integrated_data
    WHERE customer_name = $1
      AND ev = $2
      AND date_column BETWEEN $3 AND $4
)
SELECT
    ad_copy,
    SUM(spend) AS spend,
    SUM(clicks) AS clicks,
    SUM(impressions) AS impressions,
    SUM(sessions) AS sessions,
    CASE
        WHEN SUM(spend) = 0 THEN 0
        ELSE SUM(event_value) / SUM(spend) * 100
    END AS roas
FROM filtered_data
JOIN creatives.dim_combined_creative USING (ad_id)
GROUP BY ad_copy;
        """

        async with self.db.acquire() as connection:
            async with connection.transaction():
                async for record in connection.cursor(
                    query,
                    customer_name,
                    event.value,
                    date_range.start,
                    date_range.end,
                ):
                    yield RawMetrics(**dict(record))
