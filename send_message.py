import sys
import os
import datetime

from realty.settings import EMAIL_HOST_USER

project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'realty.settings'

import django
django.setup()

from django.core.mail import EmailMultiAlternatives
from scraping.models import RealEstate


qs = RealEstate.objects.filter(sent=False)
html_row = '<p><small>{}:{}</small></p><br/>'
if qs.exists():
    html_content = ''
    for row in qs:
        html_content += f'<a href="{row.url}" target="_blank">'
        html_content += f'{row.title}</a><br/>'
        html_content += f'<p>Price: {row.price}</p>'
        html_content += html_row.format(*divmod(row.added_time, 60))
        html_content += '<hr/><br/><br/>'
    qs.update(sent=True)
    subject = 'RealEstate'
    from_email, to = EMAIL_HOST_USER, EMAIL_HOST_USER
    text_content = 'This is an important message.'

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

today = datetime.date.today()
ten_days_ago = datetime.date.today() - datetime.timedelta(10)

RealEstate.objects.filter(sent=True, created__lte=ten_days_ago).delete()
