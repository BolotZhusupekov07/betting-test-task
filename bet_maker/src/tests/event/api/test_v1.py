import pytest


@pytest.mark.asyncio
async def test_event_state_webhook(async_client, mocker, event_mock):
    mock_service_method = mocker.patch(
        "src.event.api.v1.endpoints.EventService.handle_event_state_webhook",
    )

    data_in = {"state": "FINISHED_WIN"}
    response = await async_client.post(
        f"api/v1/events/{event_mock.guid}/state/webhook/", json=data_in
    )

    assert response.status_code == 204

    mock_service_method.assert_called_once()


@pytest.mark.asyncio
async def test_get_events__success(async_client, mocker, event_mock):
    mock_service_method = mocker.patch(
        "src.event.api.v1.endpoints.EventService.get_events",
        return_value=[event_mock],
    )

    response = await async_client.get("api/v1/events/")

    assert response.status_code == 200

    mock_service_method.assert_called_once_with()
