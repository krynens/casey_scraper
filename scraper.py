import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

import scraperwiki
import requests
from datetime import datetime
from bs4 import BeautifulSoup

today = datetime.today()

url = 'https://eproperty.casey.vic.gov.au/T1PRProd/WebApps/eProperty/P1/PublicNotices/AllPublicNotices.aspx?f=P1.CSY.PUBNOTAL.ENQ'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')
soup.find('tr', class_='headerRow').decompose()
rows = soup.find_all('tr')

for row in rows:
    record = {}
    record['address'] = row.find_all('td')[2].text
    record['date_scraped'] = today.strftime("%Y-%m-%d")
    record['description'] = row.find_all('td')[1].text
    record['council_reference'] = row.find_all('td')[0].text
    record['info_url'] = 'https://eproperty.casey.vic.gov.au/T1PRProd/WebApps/eProperty/P1/PublicNotices/' + \
        str(row.find_all('td')[0]).split('"')[1]
    on_notice_to_raw = row.find_all('td')[3].text
    record['on_notice_to'] = datetime.strptime(on_notice_to_raw, "%d/%m/%Y").strftime("%Y-%m-%d")
    
    scraperwiki.sqlite.save(
        unique_keys=['council_reference'], data=record, table_name="data")
