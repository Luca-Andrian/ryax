import mock
import pytest

from actions.send_email.ryax_handler import Mail, MIMEMultipart, handle


@mock.patch.object(Mail, "__init__")
@mock.patch.object(Mail, "configure")
@mock.patch.object(Mail, "send_message")
def test_handle(send_message_mock, configure_mock, mail_init_mock):
    json_req = {
        "host": "host",
        "port": 111,
        "password": "password",
        "from": "from@email.com",
        "to": "to@email.com",
        "subject": "subject",
        "message": """message""",
    }
    mail_init_mock.return_value = None
    configure_mock.return_value = None
    send_message_mock.return_value = None
    handle(json_req)
    mail_init_mock.assert_called_once_with(
        host="host",
        port=111,
        password="password",
        from_email="from@email.com",
    )
    configure_mock.assert_called_once()
    send_message_mock.assert_called_once_with("subject", "to@email.com", "message")


@mock.patch("smtplib.SMTP_SSL")
def test_configure(smtp_ssl_mock):
    mail = Mail("host", 111, "password", "from@email.com")
    session_mock = mock.MagicMock()
    session_mock.ehlo = mock.MagicMock()
    session_mock.login = mock.MagicMock()
    smtp_ssl_mock.return_value = session_mock
    mail.configure()
    smtp_ssl_mock.assert_called_once_with("host", 111)
    session_mock.ehlo.assert_called_once()
    session_mock.login.assert_called_once_with("from@email.com", "password")


def test_configure_when_gmail():
    mail = Mail("host.gmail", 111, "password", "from@email.com")
    with pytest.raises(Exception):
        mail.configure()


@mock.patch.object(MIMEMultipart, "attach")
def test_send_message(multipart_attach):
    session = mock.MagicMock()
    session.sendmail = mock.MagicMock()
    session.quit = mock.MagicMock()
    mail = Mail("host", 111, "password", "from@email.com")
    mail.session = session
    mail.send_message("subject", "to@email.com", """message""")
    multipart_attach.assert_called_once_with(mock.ANY)
    session.sendmail.assert_called_once_with("from@email.com", "to@email.com", mock.ANY)
    session.quit.assert_called_once()
