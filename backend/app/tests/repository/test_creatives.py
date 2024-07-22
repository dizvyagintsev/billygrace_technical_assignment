import datetime

import pytest

from app.repository.creatives.creatives import Creatives
from app.repository.creatives.schemas import DateRange, Metrics


class TestCreatives:
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_fetch_metrics(self, creatives_repository: Creatives) -> None:
        assert {
            metric
            async for metric in creatives_repository.fetch_metrics(
                customer_name="23",
                event="order_completed",
                date_range=DateRange(
                    start=datetime.date(1970, 1, 1), end=datetime.date(2025, 1, 31)
                ),
            )
        } == {
            Metrics(
                ad_copy="['Experience the Future Today! 🚀 The all-new ProTech X5 "
                "Smartwatch – Fitness, calls, music, and more on your wrist. "
                "Grab yours now and get a FREE wireless charger!']",
                spend=33507.27,
                clicks=48981.0,
                impressions=8394077.0,
                sessions=2517857.0,
                roas=1438.7743316599651,
            ),
            Metrics(
                ad_copy="['Escape to Paradise 🌴 Book your dream vacation to Bali now "
                "and enjoy an early bird discount of 20%. Adventure is just a "
                "click away!']",
                spend=6980.55,
                clicks=16850.0,
                impressions=1739955.0,
                sessions=521775.0,
                roas=1510.0529327918287,
            ),
            Metrics(
                ad_copy="['Hungry? 🍕 Get your first bite of our delicious wood-fired "
                "Margherita Pizza! Use code ‘FIRSTORDER’ for 10% off. Fast "
                "delivery guaranteed. Order now!']",
                spend=1517.6,
                clicks=1064.0,
                impressions=379106.0,
                sessions=111118.0,
                roas=1380.9963099630995,
            ),
        }
