import mock

from actions.gcp_storage_writer.ryax_handler import handle


@mock.patch("google.cloud.storage.Client")
def test_handle(gcs_client_mock):
    req = {
        "gcp_sto_creds": "./gcp-storage-creds.json",
        "gcp_sto_bucket": "example_bucket_ryax",
        "file_to_upload": "file.txt",
        "dir_to_upload": "dirname",
    }
    client_mock = mock.MagicMock()
    bucket = mock.MagicMock()
    blob = mock.MagicMock()
    blob.upload_from_filename = mock.MagicMock()
    bucket.blob.return_value = blob
    client_mock.get_bucket.return_value = bucket
    gcs_client_mock.return_value = client_mock
    assert handle(req) == {}
    gcs_client_mock.assert_called_once()
    client_mock.get_bucket.assert_called_once_with("example_bucket_ryax")
    bucket.blob.assert_called_once_with("dirname/file.txt")
    blob.upload_from_filename.assert_called_once_with("file.txt")
