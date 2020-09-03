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
    for idx, parl_leg_link in enumerate(person_leg_profile_links):
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
    # bang all the person-legislatures together
    for idx, parl in enumerate(parliamentarians):
        row = ['', str(idx), parl["legislature"], parl["chamber"], parl["surnames"], parl["given names"],
               parl["mandate start"], parl["mandate end"], parl["entry party"], parl["first party switch month"],
               parl["first party switch year"]]

        parl_leg_table.append(row)

    assign_unique_person_ids(parl_leg_table)

    # write output table to disk
    header = ["PersID", "PersLegID", "legislature", "chamber", "surnames", "given names", "mandate start",
              "mandate end", "entry party", "first party switch month", "first party switch year"]
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

    soup = BeautifulSoup(html.text, 'html.parser')

    surnames, given_names = get_names(soup)
    legislature = get_legislature(soup)
    chamber = get_chamber(soup)
    mandate_start, mandate_end = get_mandate(soup)
    entry_party, first_party_switch = get_party_name_and_first_switch(soup)

    return {"legislature": legislature, "chamber": chamber, "surnames": surnames, "given names": given_names,
            "mandate start": mandate_start, "mandate end": mandate_end, "entry party": entry_party,
            "first party switch month": first_party_switch["month"],
            "first party switch year": first_party_switch["year"]}


def get_names(soup):
    """
    Get the surnames and given names of the parliamentarian-legislature.

    :param soup: a BeautifulSoup object
    :return: a tuple of strings, first string is surnames (all uppercase) second string is given names
    """
    names = soup.find('div', class_="boxTitle").text.replace('-', ' ').split()
    surnames, given_names = ' '.join([n for n in names if n.isupper()]), ' '.join([n for n in names if not n.isupper()])
    surnames, given_names = ad_hoc_name_corrector(surnames, given_names)
    return surnames, given_names


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


def get_legislature(soup):
    """
    Return the legislature, e.g. 2004-2008
    :param soup: a BeautifulSoup object
    :return: a string in format START YEAR- END YEAR, e.g. 1992-1996
    """

    # get legislature; all the filters there are to extract just the year from the text below
    # Prima pagina > Legislatura 1990-1992 / Camera Deputatilor > Viorica Edelhauser
    leg = soup.find('td', class_="cale-right").text.split('>')[1].split('/')[0].replace('Legislatura', '').strip()
    return leg


def get_chamber(soup):
    """
    Identifies which chamber of parliament (lower house = Camera Deputaţilor ; upper house = Senat) the
    parlaimentarian-legislature was in.

    :param soup: a BeautifulSoup object
    :return: str, "DEPUTAT" or "SENATOR"
    """

    # chamber text always includes "DEPUTAT" or "SENATOR" but sometimes other info too, such as whether the
    # parliamentarian was speaker or secretary of the chamber. Code below excludes all that other info
    chamber_text = soup.find('div', class_="boxDep clearfix").h3.text
    if "DEPUTAT" in chamber_text:
        chamber = "DEPUTAT"
    elif "SENATOR" in chamber_text:
        chamber = "SENATOR"
    else:  # if neither deputy nor senator, some error that I have to inspect later
        chamber = None
    return chamber


def get_mandate(soup):
    """
    Returns the beginning and end of a parliamentarian's mandate. Mandates differ in length because some
    join parliament after elections (since they replace a retiree) while some retire before the end of their term.

    :param soup: a BeautifulSoup object
    :
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

    # one ad-hoc problem with SILAGHI Ovidiu Ioan, who for some reason is registered twice in the same year
    surnames, given_names = get_names(soup)
    legislature = get_legislature(soup)
    if surnames == "SILAGHI" and given_names == "Ovidiu Ioan" and legislature == "2012-2016":
        mandate_start, mandate_end = "default", "default"

    return mandate_start, mandate_end


def get_party_name_and_first_switch(soup):
    party_codes = {"FSN": "Frontul Salvării Naţionale", "PSD": "Partidul Social Democrat",
                   "PNL": "Partidul Naţional Liberal", "PDSR": "Partidul Democraţiei Sociale din România",
                   "PNTCD": "Partidul Naţional Ţărănesc Creştin Democrat", "PD": "Partidul Democrat",
                   "PDL": "Partidul Democrat Liberal", "UDMR": "Uniunea Democrată Maghiară din România",
                   "PP DD": "Partidul Poporului - Dan Diaconescu", "MER": "Mişcarea Ecologistă din România",
                   "PC": "Partidul Conservator", "PRM": "Partidul România Mare", "PER": "Partidul Ecologist Român",
                   "PUR SL": "Partidul Social Umanist din România (social liberal)", "USR": "Uniunea Salvaţi România",
                   "PNL CD": "Partidul Naţional Liberal - Convenţia Democrată", "PSM": "Partidul Socialist al Muncii",
                   "FDSN": "Frontul Democrat al Salvarii Nationale", "PUNR": "Partidul Unităţi Naţionale a Românilor",
                   "PMP": "Partidul Mişcarea Populară", "ALDE": "Alianţa Liberalior şi Democraţilor",
                   "PDAR": "Partidul Democrat Agrar din România", "PAC": "Partidul Alianţei Civice",
                   "PL'93": "Partidul Liberal 1993", "GDC": "Gruparea Democratică de Centru",
                   "PTLDR": "Partidul Tineretului Liber Democrat din România", "ULB": 'Uniunea Liberală "Brătianu"',
                   "AUR": "Alianţa pentru Unitatea Românilor", "PRNR": "Partidul Reconstrucţiei Naţionale din România",
                   "PLS": "Partidul Liber Schimbist", "FER": "Federaţia Ecologistă Română",
                   "PAR": "Partidul Alternativa României", "UNPR": "Uniunea Națională pentru Progresul României",
                   "FC": "Forţa Civică"}

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

    # covers for bugs related to party name changes

    # "FDSN" rebranded as "PDSR" in 1993 and
    if entry_party == 'Frontul Democrat al Salvarii Nationale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date = {"month": '', "year": ''}

    # "PDSR" rebranded as to "PSD" in 2001
    if entry_party == 'Partidul Democraţiei Sociale din România':
        if first_switch_date and first_switch_date['year'] == '2001':
            first_switch_date = {"month": '', "year": ''}

    # FSN became PD in 1993
    if entry_party == 'Frontul Salvării Naţionale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date = {"month": '', "year": ''}

    # run the data past the ad-hoc party name and switch corrector
    surnames, given_names = get_names(soup)
    legislature = get_legislature(soup)
    entry_party, first_switch_date = ad_hoc_party_names_and_switches(surnames, given_names, legislature,
                                                                     entry_party, first_switch_date)
    print(entry_party, first_switch_date)
    return entry_party, first_switch_date


def ad_hoc_party_names_and_switches(surnames, given_names, legislature, entry_party, first_switch_date):
    """
    In some legislatures some parliamentarians have unusually formatted profiles regarding party names and switches.
    This function catches and corrects that unusualness.

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
        entry_party, first_switch_date = "Partidul Democraţiei Sociale din România", {"month": "12", "year": "1995"}

    if surnames == "BOLD" and given_names == "Ion" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Naţional Ţărănesc Creştin Democrat", {"month": "12", "year": "1994"}

    if surnames == "DRĂGHIEA" and given_names == "Nicolae" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Democraţiei Sociale din România", {"month": "02", "year": "1995"}

    if surnames == "PASCU" and given_names == "Horia Radu" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Liberal 1993", {"month": "09", "year": "1993"}

    if surnames == "CERVENI" and given_names == "Niculae" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Liberal 1993", {"month": "09", "year": "1993"}

    if surnames == "TĂNASIE" and given_names == "Petru" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Democraţiei Sociale din România", {"month": "02", "year": "1996"}

    if surnames == "HRISTU" and given_names == "Ion" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul România Mare", {"month": "04", "year": "1993"}

    if surnames == "VINTILESCU" and given_names == "Teodor" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Liberal 1993", {"month": "02", "year": "1994"}

    if surnames == "RĂBAN" and given_names == "Grigore" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Socialist al Muncii", {"month": "02", "year": "1995"}

    if surnames == "MÂNDROVICEANU" and given_names == "Vasile" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Liberal 1993", {"month": "03", "year": "1995"}

    if surnames == "JECAN" and given_names == "Aurel" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Unităţi Naţionale a Românilor", {"month": "09", "year": "1996"}

    if surnames == "URSU" and given_names == "Doru Viorel" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Democrat", {"month": "03", "year": "1995"}

    if surnames == "ŢURLEA" and given_names == "Petre" and legislature == '1992-1996':
        entry_party, first_switch_date = "Partidul Democraţiei Sociale din România", {"month": "09", "year": "1993"}

    if surnames == "COŞEA" and given_names == "Dumitru Gheorghe Mircea" and legislature == '2004-2008':
        entry_party, first_switch_date = "Partidul Naţional Liberal", {"month": "02", "year": "2008"}

    if surnames == "TODIRAŞCU" and given_names == "Valeriu" and legislature == "2012-2016":
        entry_party, first_switch_date = "Partidul Democrat Liberal", {"month": "02", "year": "2015"}

    if surnames == "CERNEA" and given_names == "Remus Florinel" and legislature == "2012-2016":
        entry_party, first_switch_date = "Partidul Social Democrat", {"month": "05", "year": "2013"}

    if surnames == "SILAGHI" and given_names == "Ovidiu Ioan" and legislature == "2012-2016":
        entry_party, first_switch_date = "Partidul Naţional Liberal", {"month": "07", "year": "2014"}

    return entry_party, first_switch_date


def assign_unique_person_ids(parl_leg_table):
    """
    Goes through a table of parliamentarian-legislatures and assigns each person (and their associated mandates)
    one unique ID.

    NB: there are two "POPO Virigil" in the 1996-2000 legislature with nothing to distinguish them as far as these
    data are concerned (same party, neither switches, same mandates) so I leave these two merged. Nothing can be done.

    :param parl_leg_table: table (as list of lists) of parliamentarian-legislature, where each parl-leg is a row
    :return: None
    """

    # assign person-level ID's
    unique_full_names = {row[4] + ' ' + row[5] for row in parl_leg_table}
    unique_person_ids = {ufn: str(idx) for idx, ufn in enumerate(unique_full_names)}
    for parl_leg in parl_leg_table:

        parl_full_name = parl_leg[4] + ' ' + parl_leg[5]

        if parl_full_name in unique_person_ids:

            # some people have identical full names, but different legislatures; handle
            if parl_full_name == 'POPESCU Virgil' and parl_leg[2] == "1990-1992":  # parl_leg[2] = legislature
                parl_leg[0] = max(unique_person_ids) + 1
            elif parl_full_name == 'POPESCU Corneliu' and parl_leg[2] == "2004-2008":
                parl_leg[0] = max(unique_person_ids) + 2
            else:  # everyone else with unique full names
                parl_leg[0] = unique_person_ids[parl_full_name]

        else:
            print(parl_full_name, " NOT IN FULLNAME SET, ERROR, CHECK")


if __name__ == "__main__":
    scrape_parliamentarians(root + 'data/parliamentarians/')
