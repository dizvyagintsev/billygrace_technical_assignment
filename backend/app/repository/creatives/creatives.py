from typing import AsyncIterator

import asyncpg

from app.repository.creatives.schemas import DateRange, FilterOptions, Metrics


class Creatives:
    def __init__(self, db: asyncpg.pool.Pool):
        self.db = db

    async def fetch_filter_options(self, customer_name: str) -> FilterOptions:
        query = """
        SELECT ev, MIN(date_column), MAX(date_column)
        FROM creatives.pixel_event_integrated_data
        WHERE customer_name = $1 group by ev;
        """

        async with self.db.acquire() as connection:
            async with connection.transaction():
                records = await connection.fetch(query, customer_name)
                if not records:
                    return FilterOptions(events=[], date_range=None)

                events = [record["ev"] for record in records]
                start_date = records[0]["min"]
                end_date = records[0]["max"]
                return FilterOptions(
                    events=events, date_range=DateRange(start_date, end_date)
                )

    async def fetch_metrics(
        self, customer_name: str, event: str, date_range: DateRange
    ) -> AsyncIterator[Metrics]:
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
                    event,
                    date_range.start,
                    date_range.end,
                ):
                    yield Metrics(**dict(record))
