#!/usr/bin/env python3
# Copyright (C) Ryax Technologies
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail(object):
    def __init__(self, host, port, password, from_email):
        self.from_email = from_email
        self.password = password
        self.host = host
        self.port = port

    def configure(self):
        print(f"Logging to {self.host}:{self.port}")
        if "gmail" in self.host:
            raise Exception("Gmail host in not supported in this module")
        else:
            session = smtplib.SMTP_SSL(self.host, self.port)
            session.ehlo()
            session.login(self.from_email, self.password)
            self.session = session

    def send_message(self, subject, to, body):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.from_email
        message["To"] = to
        message["Subject"] = subject

        # Add body to email
        mime_text = MIMEText(body, "plain")
        message.attach(mime_text)

        # Send e-mail
        print("Sending e-mail...")
        self.session.sendmail(self.from_email, to, message.as_string())
        print("Done.")
        self.session.quit()


def handle(req):
    mail = Mail(
        host=req["host"],
        port=req["port"],
        password=req["password"],
        from_email=req["from"],
    )
    mail.configure()
    mail.send_message(req["subject"], req["to"], req["message"])
