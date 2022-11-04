import mock

from actions.slack_alerting.ryax_handler import handle


@mock.patch("apprise.Apprise", autospec=True)
def test_handle(apprise):
    test_mock = mock.MagicMock()
    test_mock.add = mock.MagicMock()
    apprise.return_value = test_mock
    req = {
        "title": "My notif",
        "message": """cool notif message.\ngood day ^^""",
        "tokenA": "AAAAAAAA",
        "tokenB": "BBBBBBBB",
        "tokenC": "CCCCCCCCCCCCC",
        "notify_type": "info",
    }
    handle(req)
    apprise.assert_called()
    test_mock.add.assert_called_once_with("slack://AAAAAAAA/BBBBBBBB/CCCCCCCCCCCCC")
    test_mock.notify.assert_called_once_with(
        title="My notif",
        body="""cool notif message.\ngood day ^^""",
        notify_type="info",
    )
