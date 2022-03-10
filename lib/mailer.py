import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename

from django.template.loader import get_template
from lib.middleware import mailer

DOMAIN = "prions.ci"


def send_mail(server = mailer["server"], port = mailer["port"], **kwargs):
    action = kwargs.get("action")
    e_subject = kwargs.get("e_subject")
    e_sender = kwargs.get("e_sender", "info")
    e_receiver = kwargs.get("e_receiver")
    e_context = kwargs.get("e_context")

    text_content = get_template('notify/{}.txt'.format(action))
    html_content = get_template('notify/{}.html'.format(action))

    subject, from_email, to = e_subject, "{0}@{1}".format(e_sender, DOMAIN), e_receiver
    text_content = text_content.render(e_context)
    html_content = html_content.render(e_context)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text_content))
    # msg.attach(MIMEText(html_content, 'html'))

    if "e_attachments" in kwargs:
        e_attachments = kwargs.get("e_attachments")
        for f in e_attachments or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name = basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    try:
        smtp = smtplib.SMTP(server, port)
        smtp.sendmail(from_email, to, msg.as_string())
        smtp.close()
    except TimeoutError as e:
        print(e)
    except Exception as e:
        print(e)
