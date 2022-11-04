import pytest

from triggers.one_run.ryax_run import run


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_values_mock",
    [
        {},
        {"meaningless_input": "foo"},
        {"meaningless_input2": 2},
        {"meaningless_input3": "bar", "meaningless_input4": 100},
    ],
)
async def test_one_run(service_mock, input_values_mock):
    """One run should always send execution once with no parameters"""
    await run(service_mock, input_values_mock)
    service_mock.create_run.assert_called_with({})
