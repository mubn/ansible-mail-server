#!/usr/bin/env python3
"""SMTP submission + IMAP fetch roundtrip for a virtual mailbox."""

from __future__ import annotations

import imaplib
import os
import smtplib
import ssl
import sys
import time
import uuid
from email.message import EmailMessage


def env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"missing environment variable {name}")
    return value


def tls_context(verify: bool) -> ssl.SSLContext:
    if verify:
        return ssl.create_default_context()
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context


def main() -> None:
    host = env("MAIL_HOST")
    user = env("MAIL_USER")
    password = env("MAIL_PASSWORD")
    verify = env("MAIL_VERIFY_TLS").lower() in {"1", "true", "yes"}
    smtp_port = int(os.environ.get("MAIL_SMTP_PORT", "587"))
    imap_port = int(os.environ.get("MAIL_IMAP_PORT", "143"))
    timeout = int(os.environ.get("MAIL_TIMEOUT", "30"))

    token = uuid.uuid4().hex
    subject = f"verify-{token}"
    context = tls_context(verify)

    message = EmailMessage()
    message["From"] = user
    message["To"] = user
    message["Subject"] = subject
    message.set_content("Automated verification message.\n")

    with smtplib.SMTP(host, smtp_port, timeout=timeout) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.login(user, password)
        smtp.send_message(message)

    deadline = time.time() + timeout
    found = False
    with imaplib.IMAP4(host, imap_port, timeout=timeout) as imap:
        imap.starttls(ssl_context=context)
        imap.login(user, password)
        imap.select("INBOX")
        while time.time() < deadline:
            status, data = imap.search(None, "SUBJECT", subject)
            if status == "OK" and data and data[0]:
                found = True
                for mail_id in data[0].split():
                    imap.store(mail_id, "+FLAGS", "\\Deleted")
                imap.expunge()
                break
            time.sleep(2)
            imap.noop()
        imap.logout()

    if not found:
        raise SystemExit(f"sent {subject!r} but it did not appear in INBOX within {timeout}s")

    print(f"delivered and fetched {subject}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — surface the exact mail-stack error
        print(exc, file=sys.stderr)
        raise SystemExit(1)
