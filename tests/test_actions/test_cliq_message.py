import mock

from actions.cliq_message.ryax_handler import handle


@mock.patch("requests.post")
def test_handle(post_mock):
    req = {
        "url": "cliq_channel_endpoint",
        "token": "aaa",
        "message": "Hello world !",
        "bot_name": "Bot name",
        "bot_logo": "path_to_logo",
    }
    handle(req)
    post_mock.assert_called_once_with(
        "cliq_channel_endpoint",
        headers={"Content-Type": "application/json"},
        params={"zapikey": "aaa"},
        data="{'text': 'Hello world !', 'bot': {'name': 'Bot name', 'image': 'path_to_logo'}}",
    )
