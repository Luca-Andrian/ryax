import mock
import pytest

from triggers.gitlab_release.ryax_run import receive_notification, run


class TestGitlabMergeRequest:
    @pytest.mark.asyncio
    @mock.patch("aiohttp.web", mock.MagicMock())
    @mock.patch("aiohttp.web.TCPSite")
    async def test_handler(self, TCPSite_mock):
        TCPSite_mock.return_value = mock.AsyncMock()
        await run(None, {})

    @pytest.mark.asyncio
    async def test_receive_notification(self, service_mock):
        input_values = {"secret_token": "aze"}
        request_mock = mock.AsyncMock()
        request_mock.headers = {"X-Gitlab-Token": "aze"}
        data = {
            "object_kind": "release",
            "id": "test_id",
            "description": "test_description",
            "name": "test_name",
            "released_at": "test_released_at",
            "tag": "test_tag",
            "url": "test_url",
            "action": "test_action",
            "project": {
                "name": "project-name",
            },
        }
        request_json_mock = mock.AsyncMock(return_value=data)
        request_mock.json = request_json_mock

        response = await receive_notification(request_mock, service_mock, input_values)
        assert response.status == 200
        service_mock.create_run.assert_called_once_with(
            {
                "id": "test_id",
                "description": "test_description",
                "name": "test_name",
                "released_at": "test_released_at",
                "tag": "test_tag",
                "url": "test_url",
                "action": "test_action",
                "projectname": "project-name",
            }
        )

    @pytest.mark.asyncio
    async def test_receive_notification_when_invalid_event(self, service_mock):
        request_mock = mock.AsyncMock()
        request_mock.headers = {"X-Gitlab-Token": "aze"}
        request_json_mock = mock.AsyncMock(return_value={"object_kind": "not_release"})
        request_mock.json = request_json_mock
        input_values = {"secret_token": "aze"}
        response = await receive_notification(request_mock, service_mock, input_values)
        assert response.status == 400
        assert response.text == '"Invalid event"'

    @pytest.mark.asyncio
    async def test_receive_notification_when_invalid_token(self, service_mock):
        request_mock = mock.AsyncMock()
        request_mock.headers = {"X-Gitlab-Token": "aze"}
        input_values = {"secret_token": "azerty"}
        response = await receive_notification(request_mock, service_mock, input_values)
        assert response.status == 401
        assert response.text == '"Invalid Token"'
