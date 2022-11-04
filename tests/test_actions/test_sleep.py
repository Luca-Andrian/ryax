import time

import mock

from actions.sleep.ryax_handler import handle as sleep_handler


def test_sleep():
    time.sleep = mock.MagicMock(return_value=None)
    input_dict = {"sleepfor": 1}
    sleep_handler(input_dict)
    time.sleep.assert_called_with(1)
