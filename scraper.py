import os, sys
import requests
import re
from bs4 import BeautifulSoup as BS
import codecs
from datetime import datetime
from random import randint


project_dir = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'realty.settings'

import django
django.setup()

from django.db import IntegrityError
from scraping.models import RealEstate

TIME_PATTERN = r'.+(?P<_time>\d{2}:\d{2})'
session = requests.Session()
headers = [
    {'User-Agent':
         'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent':
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
base_url = 'https://www.olx.ua/nedvizhimost/kvartiry-komnaty/prodazha-kvartir-komnat/kiev/?search%5Bfilter_float_number_of_rooms%3Afrom%5D=3&search%5Bfilter_float_number_of_rooms%3Ato%5D=3&search%5Bdistrict_id%5D=15'
domain = 'https://www.olx.ua/'
data = []
urls = []
# urls.append(base_url)
req = session.get(base_url, headers=headers[randint(0, 2)])
today = datetime.today()
today_str = datetime.strftime(today, '%d-%m-%Y')
if req.status_code == 200:
    bsObj = BS(req.text, "html.parser")
    table = bsObj.find('table', attrs={'id': 'offers_table'})
    tr_list = bsObj.find_all('tr', attrs={'class': 'wrap'})
    for tr in tr_list:
        td = tr.find('td', attrs={'class': 'offer'})
        if 'promoted' in td['class']:
            continue
        title_cell = td.find('td', attrs={'class': 'title-cell'})
        title = title_cell.find('h3')
        href = title.a['href']
        price = "No price"
        last_price = 0
        td_price = td.find('td', attrs={'class': 'td-price'})
        if td_price:
            price = td_price.text.replace('\n', ' ').replace('\t', ' ')
            last_price = int(''.join(c for c in price if c.isdigit()))
        bottom_cell = td.find('td', attrs={'class': 'bottom-cell'})
        added_time = None
        f_text = bottom_cell.text.replace('\n', ' ').replace('\t', ' ')
        _m = re.findall(TIME_PATTERN, f_text)
        if _m:
            _time = _m[0]
            hour, minute = _time.split(":")
            added_time = int(hour) * 60 + int(minute)
        history_data = {today_str: price}
        data.append({'url': href,
                     'title': title.text,
                     'price': price,
                     'added_time': added_time,
                     'last_price': last_price,
                     'history_data': history_data
                     })
        urls.append(href)
qs = RealEstate.objects.filter(url__in=urls)
used = {q.url: q for q in qs}
for d in data:
    if d['url'] in used:
        instance = used[d['url']]
        if instance.last_price != d['last_price']:
            _data = instance.history_data
            _data[today_str] = d['price']
            instance.history_data = _data
            instance.sent = False
            instance.save()
    else:
        m = RealEstate(**d)
        m.save()
    # try:
    #     m.save()
    # except IntegrityError:
    #     pass
# handle = codecs.open('data.html', "w", 'utf-8')
# handle.write(str(data))
# handle.close()
