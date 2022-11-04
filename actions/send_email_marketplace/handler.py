#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
How to configure:
Change the hardcoded parameters on the constructor:
    self.from_email = "yourmail@ryax.tech"
    self.password = "yoursecret"

This only works form zoho smtp if the account has 2FA disabled.
"""


class Mail(object):
    def __init__(self):
        print("Preparing to send e-mail message...")
        self.from_email = "pedro.velho@ryax.tech"
        self.password = "fd1ohroysbrn"
        self.host = "smtp.zoho.com"
        self.port = 465
        self.from_email_alternate = "ryaxanalytics@ryax.tech"

    def configure(self):
        print("Establishing SMTP connection...")
        print(f"Logging to {self.host}:{self.port}")
        if "gmail" in self.host:
            raise Exception("Gmail host in not supported in this module")
        else:
            session = smtplib.SMTP_SSL(self.host, self.port)
            session.ehlo()
            session.login(self.from_email, self.password)
            self.session = session

    def add_attachment(self, message: MIMEMultipart, attachment: str):
        print("Add the attachment file...")
        # Add attachment
        with open(attachment, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            content = file.read()
            part.set_payload(content)
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment)}",
        )
        message.attach(part)

    def send_message(self, subject, to, body, attachment):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.from_email_alternate
        message["To"] = to
        message["Subject"] = subject

        # Add body to email
        mime_text = MIMEText(body, "html")
        message.attach(mime_text)
        self.add_attachment(message, attachment)

        # Send e-mail
        print("Sending e-mail...")
        self.session.sendmail(self.from_email_alternate, to, message.as_string())
        print("Done.")
        self.session.quit()


def get_template_from_file():
    with open("./template.html", "r") as body_msg:
        return body_msg.read()


def handle(req):
    mail = Mail()
    mail.configure()
    mail.send_message(
        "Ryax e-mail publisher",
        req["email_to"],
        get_template_from_file(),
        req["file_to_attach"],
    )
