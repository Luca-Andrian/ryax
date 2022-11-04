import time

import mock
import pytest
import requests
from influxdb import InfluxDBClient

from actions.floattoinfluxdb.ryax_handler import create_json_body
from actions.floattoinfluxdb.ryax_handler import handle as floattoinfluxdb_handler


@pytest.mark.parametrize(
    "float2db_input, list_dbs",
    [
        (
            {
                "host": "hoster",
                "port": 1,
                "user": "user1",
                "password": "pass1",
                "dbname": "db_name",
                "measurement_name": "measure",
                "value": 10.5,
            },
            [{"name": "db_name"}],
        ),
        (
            {
                "host": "hoster",
                "port": 1,
                "user": "user1",
                "password": "pass1",
                "dbname": "db_name",
                "measurement_name": "measure",
                "value": 10.5,
            },
            [{"name": "no_good_names"}],
        ),
    ],
)
def test_floattoinfluxdb(float2db_input, list_dbs):
    InfluxDBClient.get_list_database = mock.MagicMock(return_value=list_dbs)
    InfluxDBClient.create_database = mock.MagicMock()
    InfluxDBClient.switch_database = mock.MagicMock()
    InfluxDBClient.write_points = mock.MagicMock()
    InfluxDBClient.close = mock.MagicMock()
    assert floattoinfluxdb_handler(float2db_input) == {}


@pytest.mark.parametrize(
    "float2db_input, list_dbs",
    [
        (
            {
                "host": "hoster",
                "port": 1,
                "user": "user1",
                "password": "pass1",
                "dbname": "db_name",
                "measurement_name": "measure",
                "value": 10.5,
            },
            [{"name": "db_name"}],
        )
    ],
)
def test_floattoinfluxdb_when_connectionerrors(float2db_input, list_dbs, capfd):
    InfluxDBClient.get_list_database = mock.MagicMock(return_value=list_dbs)
    InfluxDBClient.create_database = mock.MagicMock()
    InfluxDBClient.switch_database = mock.MagicMock(
        side_effect=[requests.exceptions.ConnectionError, lambda _: _]
    )
    InfluxDBClient.write_points = mock.MagicMock()
    InfluxDBClient.close = mock.MagicMock()
    time.sleep = mock.MagicMock()
    assert floattoinfluxdb_handler(float2db_input) == {}
    time.sleep.assert_called_with(1)
    out, err = capfd.readouterr()
    assert out == "Connection Error! Retrying...\n"


@pytest.mark.parametrize(
    "measurement,time,value", [(1, 2, 3), ("1", "2", "3"), (True, False, None)]
)
def test_create_json_body(measurement, time, value):
    assert create_json_body(measurement, time, value) == [
        {"measurement": measurement, "time": time, "fields": {"value": value}}
    ]
