# Weather app that detects changes from NHC page and sends email to subscribers
__version__ = '21.08.11'

import requests
from bs4 import BeautifulSoup

nhc_site = 'https://www.nhc.noaa.gov/'

if __name__ == '__main__':
    source = requests.get(nhc_site).text
    soup = BeautifulSoup(source, 'lxml')
    tables = soup.find_all('table')

    section = tables[7]
    sub_sections = section.find_all('tr')

    region = sub_sections[0].text

    outlook_tag = sub_sections[1].find('td', align='left')
    outlook_text = outlook_tag.a.text
    outlook_link = nhc_site + outlook_tag.a['href']
    outlook_last_update = outlook_tag.span.text

    discussion_tag = sub_sections[1].find('td', align='right')
    discussion_text = discussion_tag.a.text
    discussion_link = nhc_site + discussion_tag.a['href']
    discussion_last_update = discussion_tag.span.text

    storm_section = sub_sections[3]
    storm_header = storm_section.find('tr', align='left', valign='middle')

    storm_image_tag = storm_header.img
    storm_name_tag = storm_header.b
    storm_name = storm_name_tag.a['name']
    storm_fullname = storm_name_tag.text
    rss_image_tag = storm_header.find('img', alt='RSS Feed icon')
    rss_link = nhc_site + rss_image_tag.parent['href']

    storm_body = sub_sections[5]
    headline = storm_body.find('td', class_='std').text.strip()

    # TODO: Detect number of rows
    for row in range(1, 4):
        for box in storm_body.find_all('tr')[row].find_all('td'):
            try:
                if box['class'] == ['reg']:
                    if box.a is None:
                        important_info = box.text
                    else:
                        important_info = box.text
                        link = nhc_site + box.a['href']
                        image_tag = box.img

                elif box.a is not None and box['class'] == ['std']:
                    link = nhc_site + box.a['href']
                    link_text = box.text

            except KeyError as error:
                print(f'KeyError exception handled: {error}')
