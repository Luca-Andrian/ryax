import os

import mock
import pytest

from actions.send_email_marketplace.handler import Mail, MIMEMultipart, handle


@pytest.fixture
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)


@mock.patch.object(Mail, "configure")
@mock.patch.object(Mail, "send_message")
@mock.patch("actions.send_email_marketplace.handler.get_template_from_file")
def test_handle(send_message_mock, configure_mock, get_template_from_file_mock):
    json_req = {
        "email_to": "pedro.velho@email.com",
        "file_to_attach": "../conftest.py",
    }
    configure_mock.return_value = None
    send_message_mock.return_value = None
    get_template_from_file_mock.return_value = "Test"
    handle(json_req)
    configure_mock.assert_called_once()
    send_message_mock.assert_called_once_with()


@mock.patch("smtplib.SMTP_SSL")
def test_configure(smtp_ssl_mock):
    mail = Mail()
    session_mock = mock.MagicMock()
    session_mock.ehlo = mock.MagicMock()
    session_mock.login = mock.MagicMock()
    smtp_ssl_mock.return_value = session_mock
    mail.configure()
    smtp_ssl_mock.assert_called_once_with("smtp.zoho.com", 465)
    session_mock.ehlo.assert_called_once()
    session_mock.login.assert_called_once_with("pedro.velho@ryax.tech", "fd1ohroysbrn")


@mock.patch.object(MIMEMultipart, "attach")
def test_send_message(multipart_attach):
    session = mock.MagicMock()
    session.sendmail = mock.MagicMock()
    session.quit = mock.MagicMock()
    mail = Mail()
    mail.session = session
    mock_attachment = "dumbfile.txt"
    with open(mock_attachment, "w") as dumb_file:
        dumb_file.write("test")
    mail.send_message(
        "Ryax e-mail publisher", "ryaxbot@free.fr", "Test", mock_attachment
    )
    session.sendmail.assert_called_once_with(
        "ryaxanalytics@ryax.tech", "ryaxbot@free.fr", mock.ANY
    )
    session.quit.assert_called_once()
