from datetime import datetime

import boto3
import mock
import pytest

from actions.download_file_from_bucket.ryax_handler import connect_to_bucket, handle


class TestDownloadFromS3:
    @pytest.fixture()
    def s3_bucket_object(self):
        class S3BucketObject:
            def __init__(self, key: str, date: str):
                self.key = key
                self.last_modified = date

        return S3BucketObject

    @pytest.mark.parametrize(
        "keys_dates,input_key,correct_key,match",
        [
            (
                [{"key": "key", "date": datetime.now()}],
                "key",
                "key",
                "Exact",
            ),
            (
                [{"key": "key", "date": datetime.now()}],
                "key",
                "key",
                "Earliest",
            ),
            (
                [{"key": "key", "date": datetime.now()}],
                "key",
                "key",
                "Latest",
            ),
            (
                [{"key": "key_foo", "date": datetime.now()}],
                "key",
                "key_foo",
                "Latest",
            ),
            (
                [{"key": "key_foo", "date": datetime.now()}],
                "key",
                "key_foo",
                "Latest",
            ),
            (
                [
                    {"key": "key", "date": datetime.now()},
                    {
                        "key": "key_foo",
                        "date": datetime.strptime("2018-06-29", "%Y-%m-%d"),
                    },
                ],
                "key",
                "key",
                "Latest",
            ),
            (
                [
                    {"key": "key", "date": datetime.now()},
                    {
                        "key": "key_foo",
                        "date": datetime.strptime("2018-06-29", "%Y-%m-%d"),
                    },
                ],
                "key",
                "key_foo",
                "Earliest",
            ),
            (
                [
                    {"key": "key_foo", "date": datetime.now()},
                    {
                        "key": "key_fo",
                        "date": datetime.strptime("2018-06-29", "%Y-%m-%d"),
                    },
                ],
                "key_fo",
                "key_fo",
                "Earliest",
            ),
            (
                [
                    {"key": "key_foo", "date": datetime.now()},
                    {
                        "key": "key_fo",
                        "date": datetime.strptime("2018-06-29", "%Y-%m-%d"),
                    },
                ],
                "key_fo",
                "key_fo",
                "Exact",
            ),
        ],
    )
    def test_download_file_from_s3(
        self, keys_dates, input_key, correct_key, match, s3_bucket_object
    ):
        handle_input_dict = {
            "key_id": "foo",
            "secret_key_id": "bar",
            "match": match,
            "bucket_name": "test",
            "key": input_key,
        }
        obj_filter_return_value = []
        for obj in keys_dates:
            obj_filter_return_value.append(
                s3_bucket_object(obj.get("key"), obj.get("date"))
            )

        with mock.patch(
            "actions.download_file_from_bucket.ryax_handler.connect_to_bucket"
        ) as get_bucket:
            get_bucket.return_value = mock.MagicMock()

            get_bucket.return_value.download_file = mock.MagicMock()
            get_bucket.return_value.objects.filter = mock.MagicMock(
                return_value=obj_filter_return_value
            )
            assert handle(handle_input_dict) == {"output_data": f"/tmp/{correct_key}"}

    @pytest.mark.parametrize(
        "keys_dates,input_key,match",
        [
            (
                [{"key": "key_doesnt_exist", "date": datetime.now()}],
                "key",
                "Exact",
            )
        ],
    )
    def test_download_file_from_s3_empty_output(
        self, keys_dates, input_key, match, s3_bucket_object
    ):
        handle_input_dict = {
            "key_id": "foo",
            "secret_key_id": "bar",
            "match": match,
            "bucket_name": "test",
            "key": input_key,
        }
        obj_filter_return_value = []
        for obj in keys_dates:
            obj_filter_return_value.append(
                s3_bucket_object(obj.get("key"), obj.get("date"))
            )

        with mock.patch(
            "actions.download_file_from_bucket.ryax_handler.connect_to_bucket"
        ) as get_bucket:
            get_bucket.return_value = mock.MagicMock()

            get_bucket.return_value.download_file = mock.MagicMock()
            get_bucket.return_value.objects.filter = mock.MagicMock(
                return_value=obj_filter_return_value
            )
            assert handle(handle_input_dict) == {}

    @pytest.mark.parametrize("name,access,secret", [("name", "access", "secret")])
    def test_connect_to_bucket(self, name, access, secret):
        boto3.resource = mock.MagicMock()
        boto3.resource.Bucket = mock.MagicMock()
        connect_to_bucket(name, access, secret)
        boto3.resource.assert_called_with(
            "s3", aws_access_key_id=access, aws_secret_access_key=secret
        )
