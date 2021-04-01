"""
Scraping records of parliamentarians' careers from the website of the Romanian parliament, saving the htmls to
disk for processing.
"""

import requests
from bs4 import BeautifulSoup
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import time
from local import root


def scrape_parliamentarians(outdir):
    """
    Scrape profiles of all deputies and senators in RO parliament from 1990 to August 2020 and dump the htmls into
    zip archive.
    """

    # make header to pass to requests, tell site who I am
    header = {'User-Agent': 'Mozilla/5.0 (Linux Mint 18, 32-bit)'}

    # get all links to parliamentarian profile pages
    with open('links_parliamentarians_html.txt', 'r') as in_f:
        text = in_f.read()
        soup = BeautifulSoup(text, 'html.parser')

    # get all htmls which lead to person-leg profiles
    person_leg_profile_links = set()
    for link in soup.find_all('a'):
        person_leg_profile_links.add(link.get('href'))

    # make zip archive
    in_memory_file = BytesIO()
    zip_archive = ZipFile(in_memory_file, mode='w')

    # iterate over all the urls, request that htmls, dump the htmls in the zip archive
    url_base = 'http://www.cdep.ro'
    for idx, parl_leg_link in enumerate(person_leg_profile_links):
        full_url = url_base + parl_leg_link
        try:
            time.sleep(1)
            print(idx, " | ", full_url)
            html = requests.get(full_url, headers=header)
            file_path = full_url.replace("http://www.cdep.ro/pls/parlam/", '') + '_.html'
            zip_archive.writestr(file_path, html.text, compress_type=ZIP_DEFLATED)
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            print(e, ' | ', full_url)
            # give it a minute
            time.sleep(60)
            # save recalcitrant url to file of failed requests, and move on
            with open('recalcitrant_profile_sites.txt', 'a') as out_f:
                out_f.write(full_url), out_f.write('\n')

    zip_archive.close()

    in_memory_file.seek(0)
    with open(outdir + '/parliamentarian_legislature_profile_site_htmls.zip', 'wb') as f:
        shutil.copyfileobj(in_memory_file, f)


if __name__ == "__main__":
    out_directory = root + 'data/parliamentarians/'
    scrape_parliamentarians(out_directory)
