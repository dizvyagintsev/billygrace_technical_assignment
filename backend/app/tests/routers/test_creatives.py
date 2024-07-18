from datetime import datetime
from typing import List, Dict
from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_creatives_storage
from app.main import app
from app.storage.creatives import RawMetrics, DateRange, Event

mocked_creatives_storage = MagicMock()
app.dependency_overrides[get_creatives_storage] = lambda: mocked_creatives_storage


@pytest.mark.parametrize(
    "customer, event, start_date, end_date, currency_sign, round_to, expected_status_code,"
    "fetched_metrics, expected_response",
    [
        (
            "23",
            "order_completed",
            "2024-05-15",
            "2024-07-05",
            "€",
            2,
            200,
            [
                RawMetrics(
                    ad_copy="Ad copy",
                    spend=100,
                    clicks=100,
                    impressions=1000,
                    sessions=1000,
                    roas=1.0,
                ),
                RawMetrics(
                    ad_copy="Ad copy 2",
                    spend=200,
                    clicks=200,
                    impressions=2000,
                    sessions=2000,
                    roas=2.0,
                ),
            ],
            [
                {
                    "ad_copy": "Ad copy",
                    "spend": "€100",
                    "clicks": "100",
                    "impressions": "1,000",
                    "sessions": "1,000",
                    "roas": "1.0%",
                },
                {
                    "ad_copy": "Ad copy 2",
                    "spend": "€200",
                    "clicks": "200",
                    "impressions": "2,000",
                    "sessions": "2,000",
                    "roas": "2.0%",
                },
            ],
        ),
    ],
)
def test_get_creative_metrics(
    client: TestClient,
    customer: str,
    event: str,
    start_date: str,
    end_date: str,
    currency_sign: str,
    round_to: int,
    expected_status_code: int,
    fetched_metrics: List[RawMetrics],
    expected_response: List[Dict],
):
    mocked_creatives_storage.fetch_metrics.return_value.__aiter__.return_value = (
        fetched_metrics
    )

    response = client.get(
        f"/customer/{customer}/creatives/{event}/metrics",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "currency_sign": currency_sign,
            "round_to": round_to,
        },
    )

    assert response.status_code == expected_status_code
    assert response.json() == expected_response

    date_range = DateRange(
        start=datetime.strptime(start_date, "%Y-%m-%d").date(),
        end=datetime.strptime(end_date, "%Y-%m-%d").date(),
    )
    mocked_creatives_storage.fetch_metrics.assert_called_once_with(
        customer_name=customer,
        event=Event(event),
        date_range=date_range,
    )
