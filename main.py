# Weather app that detects changes from NHC page and sends email to subscribers
__version__ = '21.08.10'

import requests
from bs4 import BeautifulSoup

nhc_site = 'https://www.nhc.noaa.gov/'

if __name__ == '__main__':
    source = requests.get(nhc_site).text
    soup = BeautifulSoup(source, 'lxml')
    tables = soup.find_all('table')

    for table in tables:
        print(table)
