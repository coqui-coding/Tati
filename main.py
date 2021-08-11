# Weather app that detects changes from NHC page and sends email to subscribers

import requests
from bs4 import BeautifulSoup
import logging
import re

logging.basicConfig(level=logging.DEBUG)

nhc_site = 'https://www.nhc.noaa.gov/'


def add_space_to_camel_case(string):
    return re.sub(r"(?<=\w)([A-Z])", r" \1", string.strip())


if __name__ == '__main__':
    source = requests.get(nhc_site).text
    soup = BeautifulSoup(source, 'lxml')
    tables = soup.find_all('table')

    section = tables[7]
    sub_sections = section.find_all('tr')

    region = sub_sections[0].text.strip()
    logging.debug(f'region = {region}')

    outlook_tag = sub_sections[1].find('td', align='left')
    outlook_text = outlook_tag.a.text
    outlook_link = nhc_site + outlook_tag.a['href']
    outlook_last_update = outlook_tag.span.text

    logging.debug(f'outlook_text = {outlook_text}')
    logging.debug(f'outlook_link = {outlook_link}')
    logging.debug(f'outlook_last_update = {outlook_last_update}')
    logging.info('Parsed outlook info')

    discussion_tag = sub_sections[1].find('td', align='right')
    discussion_text = discussion_tag.a.text
    discussion_link = nhc_site + discussion_tag.a['href']
    discussion_last_update = discussion_tag.span.text

    logging.debug(f'discussion_text = {discussion_text}')
    logging.debug(f'discussion_link = {discussion_link}')
    logging.debug(f'discussion_last_update = {discussion_last_update}')
    logging.info('Parsed discussion info')

    storm_section = sub_sections[3]
    storm_header = storm_section.find('tr', align='left', valign='middle')

    logging.info('Scraped storm header info')

    storm_image_tag = storm_header.img
    storm_name_tag = storm_header.b
    storm_name = storm_name_tag.a['name']
    storm_fullname = storm_name_tag.text
    rss_image_tag = storm_header.find('img', alt='RSS Feed icon')
    rss_link = nhc_site + rss_image_tag.parent['href']

    logging.debug(f'storm_image_tag = {storm_image_tag}')
    logging.debug(f'storm_name_tag = {storm_name_tag}')
    logging.debug(f'storm_name = {storm_name}')
    logging.debug(f'storm_fullname = {storm_fullname}')
    logging.debug(f'rss_image_tag = {rss_image_tag}')
    logging.debug(f'rss_link = {rss_link}')
    logging.info('Parsed storm header info')

    storm_body = sub_sections[5]
    headline = storm_body.find('td', class_='std').text.strip()

    logging.info('Starting parsing storm info')

    amount_of_rows = len(storm_body.find_all('tr'))

    for row_number in range(1, amount_of_rows):
        row = storm_body.find_all('tr')[row_number]

        # Checks for table row tags inside of table row tags and deletes the amount of tags accordingly
        amount_of_rows -= int(((str(row).count('tr>') + str(row).count('<tr ')) / 2) - 1)

    # Starts on 1 to skip headline
    for row_number in range(1, amount_of_rows):
        logging.debug(f'On row: {row_number}')

        row = storm_body.find_all('tr')[row_number].find_all('td')

        for box in row:
            logging.debug(f'On box number: {row.index(box) + 1}')

            try:
                if box['class'] == ['reg']:
                    if box.a is None:
                        important_info = add_space_to_camel_case(box.text)
                    else:
                        important_info = add_space_to_camel_case(box.text)
                        link = nhc_site + box.a['href']
                        image_tag = box.img

                    logging.debug(f'important_info = {important_info}')

                elif box.a is not None and box['class'] == ['std']:
                    link = nhc_site + box.a['href']
                    link_text = add_space_to_camel_case(box.text)

                    logging.debug(f'link_text = {link_text}')

            except KeyError as error:
                logging.exception(f'KeyError exception handled: {error}')
