import mock

from actions.twitter_alerting.ryax_handler import handle


@mock.patch("apprise.Apprise", autospec=True)
def test_handle(apprise):
    test_mock = mock.MagicMock()
    test_mock.add = mock.MagicMock()
    apprise.return_value = test_mock
    req = {
        "ConsumerKey": "AAAAAAAA",
        "ConsumerSecret": "BBBBBBBB",
        "AccessToken": "CCCCCCCCCCCCC",
        "AccessSecret": "DDDDDDDDDDD",
        "title": "A test notification",
        "message": "Hello! This test with apprise is working just fine ^^",
    }
    handle(req)
    apprise.assert_called()
    test_mock.add.assert_called_once_with(
        "twitter://AAAAAAAA/BBBBBBBB/CCCCCCCCCCCCC/DDDDDDDDDDD?mode=tweet"
    )
    test_mock.notify.assert_called_once_with(
        title="A test notification",
        body="""Hello! This test with apprise is working just fine ^^""",
    )
