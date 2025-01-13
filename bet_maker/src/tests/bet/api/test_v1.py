import pytest

from src.bet.schemas import BetCreate
from src.common.utils.test import convert_datetime_to_str


@pytest.mark.asyncio
async def test_create_bet__success(async_client, mocker, bet_mock):
    mock_service_method = mocker.patch(
        "src.bet.api.v1.endpoints.BetService.create",
        return_value=bet_mock,
    )

    data_in = {
        "event_guid": str(bet_mock.event_guid),
        "amount": 100,
    }
    response = await async_client.post("api/v1/bets/", json=data_in)

    assert response.status_code == 201
    assert response.json() == {
        "guid": str(bet_mock.guid),
        "event_guid": str(bet_mock.event_guid),
        "amount": str(bet_mock.amount),
        "status": bet_mock.status,
        "created_at": convert_datetime_to_str(bet_mock.created_at),
    }

    mock_service_method.assert_called_once_with(BetCreate(**data_in))


@pytest.mark.asyncio
async def test_get_bets__success(async_client, mocker, bet_mock):
    mock_service_method = mocker.patch(
        "src.bet.api.v1.endpoints.BetService.find_all", return_value=[bet_mock]
    )

    response = await async_client.get("api/v1/bets/")

    assert response.status_code == 200

    mock_service_method.assert_called_once_with()
