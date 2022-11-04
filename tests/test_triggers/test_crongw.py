import asyncio

import crontab
import mock
import pytest

from triggers.crongw.ryax_run import run


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_values_mock, sleep_time",
    [
        ({"foreach": "5 0 * 8 *"}, 1),
    ],
)
@mock.patch("asyncio.sleep", mock.AsyncMock(side_effect=[lambda _: _, RuntimeError]))
async def test_crongw(
    input_values_mock, sleep_time, module_outputs, module_metadata, service_mock
):
    metadata = module_metadata(run)
    output_vals = module_outputs(metadata)

    crontab.CronTab.next = mock.MagicMock(return_value=sleep_time)
    with pytest.raises(RuntimeError):
        await run(service_mock, input_values_mock)
        asyncio.sleep.assert_called_with(sleep_time)
        service_mock.create_run.assert_called_with(output_vals)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_values_mock",
    [
        {"foreach": "invalid cron time value not gonna work"},
    ],
)
async def test_crongw_when_invalid_input(service_mock, input_values_mock):
    with pytest.raises(ValueError):
        await run(service_mock, input_values_mock)
