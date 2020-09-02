"""
Tools for scraping records of parliamentarians from the website of the Romanian parliament.
"""

import requests
from bs4 import BeautifulSoup
import time
import csv
from local import root


def scrape_parliamentarians(outdir):
    """
    Scrape profiles of all deputies and senators in RO parliament from 1990 to August 2020. This code generates
    person-legislatures (i.e. one row for each legislature) and with each person legislature associates the following
    data:

    legislature; surname; given name; unique person ID (across legislatures); date mandate began in this
    legislature; parliamentary party group (8 potential slots, since can change groups maximum eight times in
    four-year legislature); date interval in parl. party group (eight slots, one for each parl group).

    Ultimately writes out one big .csv table with data on all parliamentarian-legislatures

    :param outdir: directory in which we dump zip archives
    :return: None
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

    parliamentarians = []

    # iterate over all the urls, request that htmls, and extract the relevant the data
    url_base = 'http://www.cdep.ro'
    for parl_leg_link in person_leg_profile_links:
        full_url = url_base + parl_leg_link
        try:
            time.sleep(1)
            print(full_url)
            html = requests.get(full_url, headers=header)
            parliamentarians.append(extract_parliamentarian_info(html))
        except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
            print(e, ' | ', full_url)
            # give it a minute
            time.sleep(60)
            # save recalcitrant url to file of failed requests, and move on
            with open('recalcitrant_profile_sites.txt', 'a') as out_f:
                out_f.write(full_url), out_f.write('\n')

    # build the output table
    parl_leg_table = []
    header = ["PersID", "LegID", "legislature", "chamber", "surnames", "given names", "mandate start", "mandate end",
              "entry party", "first party switch month", "first party switch year"]

    # bang all the person-legislatures together
    for idx, parl in enumerate(parliamentarians):

        row = ['', str(idx), parl["legislature"], parl["chamber"], parl["surnames"], parl["given names"],
               parl["mandate start"], parl["mandate end"], parl["entry party"], parl["first party switch month"],
               parl["first party switch year"]]

        parl_leg_table.append(row)

    # assign person-level ID's
    unique_full_names = {row[4] + ' ' + row[5] for row in parl_leg_table}
    unique_person_ids = {ufn: str(idx) for idx, ufn in enumerate(unique_full_names)}
    for parl_leg in parl_leg_table:
        parl_full_name = parl_leg[4] + ' ' + parl_leg[5]
        if parl_full_name in unique_person_ids:
            parl_leg[0] = unique_person_ids[parl_full_name]

    # write output table to disk
    with open(outdir + 'parliamentarians_party_switch_table.csv', 'w') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)
        for parl_leg in parl_leg_table:
            writer.writerow(parl_leg)


def extract_parliamentarian_info(html):
    """
    Get the parliamentarian's legislature, chamber, name, mandate boundaries (i.e start and end), the name of the
    party with which they entered parliament, and the date of the the first time they switched parties (if this
    occurred).

    :param html: str, html of parliamentarian profile site
    :return: dict with desired data per parliamentarian-legislature
    """

    # now extract desired info from html
    # div class="boxDep clearfix" ; in here you can find the grup parlamentar

    soup = BeautifulSoup(html.text, 'html.parser')

    chamber = soup.find('div', class_="boxDep clearfix").h3.text
    mandate = get_mandate(soup)
    mandate_start, mandate_end = mandate[0], mandate[1]

    # get names
    names = soup.find('div', class_="boxTitle").text.replace('-', ' ').split()
    surnames, given_names = ' '.join([n for n in names if n.isupper()]), ' '.join([n for n in names if not n.isupper()])
    surnames, given_names = ad_hoc_name_corrector(surnames, given_names)

    # get legislature; all the filters there are to extract just the year from the text below
    # Prima pagina > Legislatura 1990-1992 / Camera Deputatilor > Viorica Edelhauser
    leg = soup.find('td', class_="cale-right").text.split('>')[1].split('/')[0].replace('Legislatura', ''). strip()

    party_name_and_first_departure = get_party_name_and_first_switch(soup, surnames, given_names, leg)
    entry_party, first_party_switch = party_name_and_first_departure[0], party_name_and_first_departure[1]

    return {"legislature": leg, "chamber": chamber, "surnames": surnames, "given names": given_names,
            "mandate start": mandate_start, "mandate end": mandate_end, "entry party": entry_party,
            "first party switch month": first_party_switch["month"],
            "first party switch year": first_party_switch["year"]}


def get_mandate(soup):
    """
    Returns the beginning and end of a parliamentarian's mandate. Mandates differ in length because some
    join parliament after elections (since they replace a retiree) while some retire before the end of their term.

    :param soup: a BeautifulSoup object
    :return: a tuple of two strings, first is mandate start, second is mandate end, each in format YEAR-MONTH-DAY
    """

    ro_months = {"ianuarie": '01', "februarie": '02', "martie": '03', "aprilie": "04", "mai": '05', "iunie": '06',
                 "iulie": '07', "august": '08', "septembrie": "09", "octombrie": "10", "noiembrie": '11',
                 "decembrie": '12'}

    mandate_start, mandate_end = "default", "default"

    mandate_info = soup.find('div', class_="boxDep clearfix").contents[2].text
    if "validarii:" in mandate_info:
        start_date = ' '.join(mandate_info.split("validarii:")[1].split(' - ')[0].split())
        day, month, year = start_date.split()[0], start_date.split()[1], start_date.split()[2][:4]
        month = ro_months[month]
        mandate_start = '-'.join([year, month, day])
    if "încetarii" in mandate_info:
        end_date = ' '.join(mandate_info.split("încetarii")[1].split(' - ')[0].split())
        day, month, year = end_date.split()[1], end_date.split()[2], end_date.split()[3][:4]
        month = ro_months[month]
        mandate_end = '-'.join([year, month, day])
    return mandate_start, mandate_end


def ad_hoc_name_corrector(surnames, given_names):
    """
    Catches a bunch of ad-hoc given name mistakes, mostly to do with higher functions (e.g. treasurement of the
    lower house of parliament).

    :param surnames:str, all letters uppercase
    :param given_names: str
    :return: corrected surnames and given names
    """
    if "BĂNICIOIU" in given_names:
        surnames, given_names = "BĂNICIOIU", "Nicolae"
    if "ZISOPOL" in given_names:
        surnames, given_names = "ZISOPOL", "Dragoş Gabriel"
    if "LEOREANU" in given_names:
        surnames, given_names = "LEOREANU", "Laurenţiu Dan"
    if "PIRTEA" in given_names:
        surnames, given_names = "PIRTEA", "Marilen Gabriel"
    if "BUICAN" in given_names:
        surnames, given_names = "BUICAN", "Cristian"
    if "CIOLACU" in given_names:
        surnames, given_names = "CIOLACU", "Ion Marcel"
    if "Carmen Ileana (Moldovan)" in given_names:
        given_names = "Carmen Ileana (Moldovan)"
    if "BUDĂI" in given_names:
        surnames, given_names = "BUDĂI", "Marius Constantin"
    if "Iulian IANCU" in given_names:
        surnames, given_names = "IANCU", "Iulian"
    if "Lia Olguţa VASILESCU" in given_names:
        surnames, given_names = "VASILESCU", "Lia Olguţa"
    if "Florin IORDACHE" in given_names:
        surnames, given_names = "IORDACHE", "Florin"
    if "Dénes" in given_names:
        given_names = "Dénes"
    if "RODEANU" in given_names:
        surnames, given_names = "RODEANU", "Bogdan Ionel"
    return surnames, given_names


def get_party_name_and_first_switch(soup, surnames, given_names, legislature):

    party_codes = {"FSN": "Frontul Salvării Naţionale", "PSD": "Partidul Social Democrat",
                   "PNL": "Partidul Naţional Liberal", "PDSR": "Partidul Democraţiei Sociale din România",
                   "PNTCD": "Naţional Ţărănesc Creştin Democrat", "PD": "Partidul Democrat",
                   "PDL": "Partidul Democrat Liberal", "UDMR": "Uniunea Democrată Maghiară din România",
                   "PP DD": "Partidul Poporului - Dan Diaconescu", "MER": "Mişcarea Ecologistă din România",
                   "PC": "Partidul Conservator", "PRM": "Partidul România Mare", "PER": "Partidul Ecologist Român",
                   "PUR SL": "Partidul Social Umanist din România (social liberal)", "USR": "Uniunea Salvaţi România",
                   "PNL CD": "Partidul Naţional Liberal Convenţia Democrată", "PSM": "Partidul Socialist al Muncii",
                   "FDSN": "Frontul Democrat al Salvarii Nationale", "PUNR": "Partidul Unităţi Naţionale a Românilor",
                   "PMP": "Partidul Mişcarea Populară", "ALDE": "Alianţa Liberalior şi Democraţilor",
                   "PDAR": "Partidul Democrat Agrar din România", "PAC": "Partidul Alianţei Civice",
                   "PL'93": "Partidul Liberal 1993", "GDC": "Gruparea Democratică de Centru",
                   "PTLDR": "Partidul Tineretului Liber Democrat din România", "ULB": 'Uniunea Liberală "Brătianu"',
                   "AUR": "Alianţa pentru Unitatea Românilor", "PRNR": "Partidul Reconstrucţiei Naţionale din România",
                   "PLS": "Partidul Liber Schimbist", "FER": "Federaţia Ecologistă Română",
                   "PAR": "Partidul Alternativa României", "UNPR": "Uniunea Națională pentru Progresul României"}

    short_month_codes = {'ian': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mai': '05', 'iun': '06', 'iul': '07',
                         'aug': '08', 'sep': '09', 'oct': '10', 'noi': '11', 'dec': '12'}

    # get the name of the party with which they entered parliament, and the date of the first party switch

    entry_party = ''
    first_switch_date = {"month": '', "year": ''}

    info_fields = soup.find_all('div', class_="boxDep clearfix")
    for i in info_fields:

        if "minoritatilor nationale" in i.contents[0].text:
            entry_party = 'minorities'

        if "Formatiunea politica" in i.contents[0].text:
            for j in i.contents:
                if 'Tag' in str(type(j)) and ':' not in j.text:

                    party_group_text = j.text.replace('\xa0', '').replace('\r', '').replace('\n', '').replace('-', ' ')
                    split_by_departures = party_group_text.split('până în')

                    # sometimes parties simply change names -- ignore these
                    if len(split_by_departures) > 1 and 'se transforma' not in split_by_departures[1]:
                        departure_date = split_by_departures[1].strip()

                        departure_month = departure_date.split()[0].replace('.', '').strip()
                        departure_month = short_month_codes[departure_month]

                        departure_year = departure_date.split()[1][:4]

                        first_switch_date = {'month': departure_month, 'year': departure_year}

                    # now get the party name
                    for p_code in party_codes:
                        if p_code in split_by_departures[0]:
                            entry_party = party_codes[p_code]

                    # covers for bugs related to "PD" also being found in other party names
                    if entry_party == 'Partidul Democrat' and 'PDSR' in split_by_departures[0]:
                        entry_party = "Partidul Democraţiei Sociale din România"
                    if entry_party == 'Partidul Democrat' and 'PDAR' in split_by_departures[0]:
                        entry_party = "Partidul Democrat Agrar din România"

                    print(split_by_departures)

    # covers for some bugs related to party name changes,
    # namely that "FDSN" went to "PDSR" in 1993 and "PDSR" to "PSD" in 2001
    if entry_party == 'Frontul Democrat al Salvarii Nationale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date = {"month": '', "year": ''}
    if entry_party == 'Partidul Democraţiei Sociale din România':
        if first_switch_date and first_switch_date['year'] == '2001':
            first_switch_date = {"month": '', "year": ''}
    if entry_party == 'Frontul Salvării Naţionale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date = {"month": '', "year": ''}

    # run the data past the ad-hoc name and switch corrector
    entry_party, first_switch_date = ad_hoc_names_switch(surnames, given_names, legislature,
                                                         entry_party, first_switch_date)
    print(entry_party, first_switch_date)
    return entry_party, first_switch_date


def ad_hoc_names_switch(surnames, given_names, legislature, entry_party, first_switch_date):
    """
    In some legislatures some parliamentarians have unusually formatted profiles. This function corrects the imput
    for them.

    :param surnames: str
    :param given_names: str
    :param legislature: str
    :param entry_party: str
    :param first_switch_date: dict of form {"month": '', "year": ''}
    :return: correct entry party and first switch date
    """

    if surnames == "IORGOVAN" and given_names == "Antonie" and legislature == '1990-1992':
        entry_party, first_switch_date = "independent", {"month": '', "year": ''}
    if surnames == "CAJAL" and given_names == "Nicolae" and legislature == '1990-1992':
        entry_party, first_switch_date = "independent", {"month": '', "year": ''}
    if surnames == "BONDARIU" and given_names == "Ionel" and legislature == '1992-1996':
        entry_party, first_switch_date = "PDSR", {"month": "12", "year": "1995"}
    if surnames == "BOLD" and given_names == "Ion" and legislature == '1992-1996':
        entry_party, first_switch_date = "PNTCD", {"month": "12", "year": "1994"}
    if surnames == "DRĂGHIEA" and given_names == "Nicolae" and legislature == '1992-1996':
        entry_party, first_switch_date = "PDSR", {"month": "02", "year": "1995"}
    if surnames == "PASCU" and given_names == "Horia Radu" and legislature == '1992-1996':
        entry_party, first_switch_date = "PL'93", {"month": "09", "year": "1993"}
    if surnames == "CERVENI" and given_names == "Niculae" and legislature == '1992-1996':
        entry_party, first_switch_date = "PL'93", {"month": "09", "year": "1993"}
    if surnames == "TĂNASIE" and given_names == "Petru" and legislature == '1992-1996':
        entry_party, first_switch_date = "PDSR", {"month": "02", "year": "1996"}
    if surnames == "HRISTU" and given_names == "Ion" and legislature == '1992-1996':
        entry_party, first_switch_date = "PRM", {"month": "04", "year": "1993"}
    if surnames == "VINTILESCU" and given_names == "Teodor" and legislature == '1992-1996':
        entry_party, first_switch_date = "PL'93", {"month": "02", "year": "1994"}
    if surnames == "RĂBAN" and given_names == "Grigore" and legislature == '1992-1996':
        entry_party, first_switch_date = "PSM", {"month": "02", "year": "1995"}
    if surnames == "MÂNDROVICEANU" and given_names == "Vasile" and legislature == '1992-1996':
        entry_party, first_switch_date = "PL'93", {"month": "03", "year": "1995"}
    if surnames == "JECAN" and given_names == "Aurel" and legislature == '1992-1996':
        entry_party, first_switch_date = "PUNR", {"month": "09", "year": "1996"}
    if surnames == "Ursu" and given_names == "Doru Viorel" and legislature == '1992-1996':
        entry_party, first_switch_date = "PD", {"month": "03", "year": "1995"}
    if surnames == "ŢURLEA" and given_names == "Petre" and legislature == '1992-1996':
        entry_party, first_switch_date = "PDSR", {"month": "09", "year": "1993"}
    if surnames == "COŞEA" and given_names == "Dumitru Gheorghe Micea" and legislature == '2004-2008':
        entry_party, first_switch_date = "PNL", {"month": "02", "year": "2008"}

    return entry_party, first_switch_date


if __name__ == "__main__":
    scrape_parliamentarians(root + 'data/parliamentarians/')
