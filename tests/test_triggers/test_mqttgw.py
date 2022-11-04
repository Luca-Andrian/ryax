import asyncio

import mock
import paho.mqtt.client as mqtt
import pytest

from triggers.mqttgw.ryax_run import MQTTGateway


class TestMQTTGW:
    @pytest.fixture()
    def get_mqtt_message(self):
        class MQTTMessage:
            def decode(self):
                return "test_decode"

        return MQTTMessage

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "input_values_mock", [{"mqtt_topic": "foo", "mqtt_server": "bar"}]
    )
    async def test_mqtt_handler(
        self, input_values_mock, module_outputs, module_metadata, get_mqtt_message
    ):
        metadata = module_metadata(MQTTGateway)
        output_vals = module_outputs(metadata)
        service = mock.AsyncMock()
        service.create_run = mock.AsyncMock(side_effect=RuntimeError)
        mqttgw = MQTTGateway(service, input_values_mock)
        asyncio.get_event_loop().create_future = mock.AsyncMock(
            return_value=get_mqtt_message()
        )
        mqtt.Client = mock.MagicMock()
        with pytest.raises(RuntimeError):
            await mqttgw.handler()
            service.create_run.assert_called_with(output_vals)
