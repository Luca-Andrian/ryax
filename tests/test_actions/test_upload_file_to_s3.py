import boto3
import mock
import pytest
from freezegun import freeze_time

from actions.upload_file_to_s3.ryax_handler import connect_to_bucket, create_bucket_key
from actions.upload_file_to_s3.ryax_handler import handle as upload_to_s3_handler


@mock.patch(
    "actions.upload_file_to_s3.ryax_handler.create_bucket_key",
    mock.MagicMock(),
)
@mock.patch(
    "actions.upload_file_to_s3.ryax_handler.connect_to_bucket",
    mock.MagicMock(),
)
@pytest.mark.parametrize(
    "inputs_mock",
    [
        {
            "key_id": "foo",
            "secret_key_id": "bar",
            "bucket_name": "alpha",
            "file_to_upload": "beta.txt",
            "timestamp_bool": "timestamp",
        },
        {
            "key_id": "foo",
            "secret_key_id": "bar",
            "bucket_name": "alpha",
            "file_to_upload": "beta.txt",
            "timestamp_bool": "no-timestamp",
        },
    ],
)
def test_upload_to_s3(inputs_mock):
    s3 = boto3.resource("s3")
    s3.Bucket = mock.MagicMock()
    s3.Bucket.upload_file = mock.MagicMock()
    assert upload_to_s3_handler(inputs_mock) == {}


@pytest.mark.parametrize("name,access,secret", [("name", "access", "secret")])
def test_connect_to_bucket(name, access, secret):
    boto3.resource = mock.MagicMock()
    boto3.resource.Bucket = mock.MagicMock()
    connect_to_bucket(name, access, secret)
    boto3.resource.assert_called_with(
        "s3", aws_access_key_id=access, aws_secret_access_key=secret
    )


@pytest.mark.parametrize(
    "filename,timestamp, expected_result",
    [("foo.txt", False, "foo.txt"), ("foo.txt", True, "foo_2010-02-02T00:00:00.txt")],
)
def test_create_bucket_key(filename, timestamp, expected_result):
    with freeze_time("2010-02-02"):
        assert create_bucket_key(filename, timestamp) == expected_result
