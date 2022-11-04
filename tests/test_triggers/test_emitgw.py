from datetime import datetime

import mock
import pytest

from triggers.emitgw.ryax_run import emit_time, run, time_to_seconds


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_values_mock",
    [
        {"days": 0, "hours": 0, "minutes": 0, "seconds": 2},
    ],
)
@mock.patch("asyncio.sleep", mock.MagicMock(side_effect=RuntimeError))
async def test_emit_every(
    service_mock, input_values_mock, module_outputs, module_metadata
):
    "Emit every is an infinite loop, but it should run an execution with a timestamp"
    metadata = module_metadata(run)
    output_vals = module_outputs(metadata)
    with pytest.raises(RuntimeError):
        await run(service_mock, input_values_mock)
        service_mock.create_run.assert_called_with(output_vals)


@pytest.mark.asyncio
async def test_emit_time():
    """Emit time returns iso format and throws no errors when converting to iso"""
    date_iso_format = emit_time()
    datetime.fromisoformat(date_iso_format)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_values_mock,expected_value",
    [
        (
            {"days": 100, "hours": 0, "minutes": 0.1, "seconds": 1000.123},
            8641006.123,
        ),
        ({"days": 3.5, "hours": 1, "minutes": 0, "seconds": 100}, 306100.0),
        (
            {"days": 0.13, "hours": 100.13, "minutes": 1000.23, "seconds": 1},
            431714.8,
        ),
        ({"days": 0, "hours": 45, "minutes": 50.342, "seconds": 0}, 165020.52),
        ({"days": 0, "hours": 0.12, "minutes": 12, "seconds": 0}, 1152.0),
        ({"days": 0, "hours": 0, "minutes": 0, "seconds": 0}, 0),
    ],
)
async def test_time_to_seconds(input_values_mock, expected_value, module_metadata):
    """Time_to_seconds returns the correct time span in seconds"""
    time_seconds = time_to_seconds(input_values_mock)
    assert time_seconds == expected_value
