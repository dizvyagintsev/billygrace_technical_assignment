from datetime import datetime
from typing import Dict, List
from unittest.mock import AsyncMock, MagicMock

import pytest
from starlette.testclient import TestClient

from app.dependencies import get_creatives_repository
from app.main import app
from app.repository.creatives.schemas import DateRange, FilterOptions, Metrics

mocked_creatives_storage = MagicMock()
app.dependency_overrides[get_creatives_repository] = lambda: mocked_creatives_storage


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
                Metrics(
                    ad_copy="Ad copy",
                    spend=100,
                    clicks=100,
                    impressions=1000,
                    sessions=1000,
                    roas=1.0,
                ),
                Metrics(
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
    fetched_metrics: List[Metrics],
    expected_response: List[Dict],
) -> None:
    mocked_creatives_storage.fetch_metrics.return_value.__aiter__.return_value = (
        fetched_metrics
    )

    response = client.get(
        f"/api/customer/{customer}/creatives/{event}/metrics",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "currency_sign": currency_sign,
            "round_to": round_to,
        },
    )

    assert response.status_code == expected_status_code
    assert response.json() == {
        "columns": [
            {
                "align": "center",
                "field": "ad_copy",
                "flex": 3,
                "headerAlign": "center",
                "headerName": "Ad Copy",
            },
            {
                "align": "center",
                "field": "spend",
                "flex": 1,
                "headerAlign": "center",
                "headerName": "Spend",
            },
            {
                "align": "center",
                "field": "clicks",
                "flex": 1,
                "headerAlign": "center",
                "headerName": "Clicks",
            },
            {
                "align": "center",
                "field": "impressions",
                "flex": 1,
                "headerAlign": "center",
                "headerName": "Impressions",
            },
            {
                "align": "center",
                "field": "sessions",
                "flex": 1,
                "headerAlign": "center",
                "headerName": "Sessions",
            },
            {
                "align": "center",
                "field": "roas",
                "flex": 1,
                "headerAlign": "center",
                "headerName": "ROAS",
            },
        ],
        "rows": [
            {
                "ad_copy": "Ad copy",
                "clicks": "100",
                "id": 1,
                "impressions": "1,000",
                "roas": "1.0%",
                "sessions": "1,000",
                "spend": "€100",
            },
            {
                "ad_copy": "Ad copy 2",
                "clicks": "200",
                "id": 2,
                "impressions": "2,000",
                "roas": "2.0%",
                "sessions": "2,000",
                "spend": "€200",
            },
        ],
    }

    date_range = DateRange(
        start=datetime.strptime(start_date, "%Y-%m-%d").date(),
        end=datetime.strptime(end_date, "%Y-%m-%d").date(),
    )
    mocked_creatives_storage.fetch_metrics.assert_called_once_with(
        customer_name=customer,
        event=event,
        date_range=date_range,
    )


@pytest.mark.parametrize(
    "customer, expected_status_code, fetched_filter_option, expected_response",
    [
        (
            "23",
            200,
            FilterOptions(
                events=["event1", "event2"],
                date_range=DateRange(
                    start=datetime(2024, 6, 15).date(),
                    end=datetime(2024, 7, 1).date(),
                ),
            ),
            {
                "events": ["event1", "event2"],
                "default_date_range": {
                    "start": "2024-06-15",
                    "end": "2024-07-01",
                },
                "date_range": {
                    "start": "2024-06-15",
                    "end": "2024-07-01",
                },
                "default_event": "event1",
            },
        ),
        (
            "-1",
            200,
            FilterOptions(
                events=[],
                date_range=None,
            ),
            {
                "events": [],
                "date_range": None,
                "default_event": None,
                "default_date_range": None,
            },
        ),
    ],
)
def test_get_filter_options(
    client: TestClient,
    customer: str,
    expected_status_code: int,
    fetched_filter_option: FilterOptions,
    expected_response: Dict,
) -> None:
    mocked_creatives_storage.fetch_filter_options = AsyncMock(
        return_value=fetched_filter_option
    )

    response = client.get(
        f"/api/customer/{customer}/creatives/filter-options",
    )

    assert response.status_code == expected_status_code
    assert response.json() == expected_response

    mocked_creatives_storage.fetch_filter_options.assert_awaited_once_with(
        customer_name=customer
    )
