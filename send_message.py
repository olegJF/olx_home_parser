import sys
import os
import datetime

MAIL_SERVER = os.environ.get('MAIL_SERVER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')


project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'realty.settings'

import django
django.setup()

from django.core.mail import EmailMultiAlternatives
from scraping.models import RealEstate


qs = RealEstate.objects.filter(sent=False)
html_row = '<p><small>{}:{}</small></p><br/>'
if qs.exists() and qs.count() >= 5:
    html_content = ''
    for row in qs:
        html_content += f'<a href="{row.url}" target="_blank">'
        html_content += f'{row.title}</a><br/>'
        html_content += f'<p>Price: {row.price}</p>'
        if row.added_time:
            html_content += html_row.format(*divmod(row.added_time, 60))
        html_content += '<hr/><br/><br/>'
    qs.update(sent=True)
    subject = 'RealEstate'
    # from_email, to = EMAIL_HOST_USER, EMAIL_HOST_USER
    # text_content = 'This is an important message.'

    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    mail = smtplib.SMTP()
    mail.connect(MAIL_SERVER, 25)
    mail.ehlo()
    mail.starttls()
    mail.login(EMAIL_USER, EMAIL_PASSWORD)

    part = MIMEText(html_content, 'html')
    msg.attach(part)
    mail.sendmail(EMAIL_USER, [EMAIL_HOST_USER], msg.as_string())
    mail.quit()

    today = datetime.date.today()
    ten_days_ago = datetime.date.today() - datetime.timedelta(60)

    RealEstate.objects.filter(sent=True, created__lte=ten_days_ago).delete()
