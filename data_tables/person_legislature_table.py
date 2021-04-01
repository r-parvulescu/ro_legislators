"""
Extract relevant information from the htmls of parliamentarian-legislature profile-page htmls and dump it all
in one big csv table, that we then write to disk.
"""

from bs4 import BeautifulSoup
from zipfile import ZipFile
import tempfile
import os
import csv
import re
import operator
import itertools
import helpers
from data_tables.dicts.destination_ind_dict import destination_ind_dict

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


def make_parliamentarians_legislature_table(zip_archive_path, outdir):
    """
    This code generates a table of person-legislatures (i.e. one row for each legislature) and with each person
    legislature associates the following data:

    legislature; surname; given name; unique person ID (across legislatures); date mandate began in this
    legislature; parliamentary party group (8 potential slots, since can change groups maximum eight times in
    four-year legislature); date interval in parl. party group (eight slots, one for each parl group).

    Ultimately writes out one big .csv table with data on all parliamentarian-legislatures

    :param zip_archive_path = path to zip archive where the htmls from the profile sites are stored
    :param outdir: directory in which we dump the parliamentarian-legislature table
    :return: None
    """

    header = ["PersID", "PersLegID", "legislature", "chamber", "constituency", "surnames", "given names",
              "mandate start", "mandate end", "death status", "entry party name", "entry party code",
              "entry ppg rank", "entry ppg rank dates", "destination party code", "first party switch month",
              "first party switch year", "seniority", "former switcher "]

    parliamentarians = []

    # work in memory: unzip data files into tempdir, extract data, temp directory gone after use
    with tempfile.TemporaryDirectory() as tmpdirname:

        with ZipFile(zip_archive_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        # iterate over htmls, extracting relevant date ;  NB: they are html.text from requests, not request object
        for rootdir, subdirs, files in os.walk(tmpdirname):
            for file in files:
                file_path = rootdir + os.sep + file
                with open(file_path, 'r') as in_f:
                    parliamentarians.append(extract_parliamentarian_info(in_f))

    # build the output table
    parl_leg_table = []
    # bang all the person-legislatures together
    for idx, parl in enumerate(parliamentarians):
        row = [0, idx, parl["legislature"], parl["chamber"], parl["constituency"], parl["surnames"],
               parl["given names"], parl["mandate start"], parl["mandate end"], parl["deceased in office"],
               parl["entry party name"], parl["entry party code"], parl["entry ppg rank"], parl["entry ppg rank dates"],
               parl["destination party code"], parl["first party switch month"], parl["first party switch year"]]

        parl_leg_table.append(row)

    # deduplicate the table; e.g. SILAGHI Ovidiu Ioan for 2012-2016 appears twice in the data, for whatever reason
    parl_leg_table = helpers.deduplicate_list_of_lists(parl_leg_table)

    assign_unique_person_ids(parl_leg_table)
    parl_leg_table = seniority(parl_leg_table)
    parl_leg_table = former_switcher(parl_leg_table, header)

    # write output table to disk
    with open(outdir + 'parliamentarians_person_legislature_table.csv', 'w') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)
        for parl_leg in parl_leg_table:
            writer.writerow(parl_leg)


def extract_parliamentarian_info(html_text):
    """
    Get the parliamentarian's legislature, chamber, name, mandate boundaries (i.e start and end), the name of the
    party with which they entered parliament, and the date of the the first time they switched parties (if this
    occurred).

    :param html_text: str, html.text of parliamentarian profile site
    :return: dict with desired data per parliamentarian-legislature
    """
    soup = BeautifulSoup(html_text, 'html.parser')

    surnames, given_names = get_names(soup)
    legislature = get_legislature(soup)
    chamber = get_chamber(soup)
    constituency = get_constituency(soup)
    mandate_start, mandate_end = get_mandate(soup)
    deceased_in_office = get_deceased_in_office(soup)
    entry_party, entry_party_code, first_party_switch, dest_party_code = get_party_and_first_switch(soup)
    ppg1_rank, ppg1_dates = get_rank_in_first_ppg(soup, mandate_start, mandate_end, surnames, given_names)

    return {"legislature": legislature, "chamber": chamber, "constituency": constituency, "surnames": surnames,
            "given names": given_names, "mandate start": mandate_start, "mandate end": mandate_end,
            "deceased in office": deceased_in_office,
            "entry party name": entry_party, "entry party code": entry_party_code,
            "entry ppg rank": ppg1_rank, "entry ppg rank dates": ppg1_dates,
            "destination party code": dest_party_code,
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
    Catches a bunch of ad-hoc given name mistakes, mostly to do with higher functions (e.g. treasurer of the
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
    leg = leg.replace("prezent", "2020")
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


def get_constituency(soup):
    """
    Identifies the constituency (county, really) which the parliamentarian represents.

    :param soup: a BeautifulSoup object
    :return: str, the name of the constituency
    """

    # due to the gradual introduction of Ilfov county in the 1990s the numbering of counties differs in 1990-1992,
    # 1992-1996 & 1996-2000, and 2000 onward
    const_dict_1990 = {1: "ALBA", 2: "ARAD", 3: "ARGEŞ", 4: "BACĂU", 5: "BIHOR", 6: "BISTRIŢA-NĂSĂUD", 7: "BOTOŞANI",
                       8: "BRAŞOV", 9: "BRĂILA", 10: "BUZĂU", 11: "CARAŞ-SEVERIN", 12: "CĂLĂRAŞI", 13: "CLUJ",
                       14: "CONSTANŢA", 15: "COVASNA", 16: "DÂMBOVIŢA", 17: "DOLJ", 18: "GALAŢI", 19: "GIURGIU",
                       20: "GORJ", 21: "HARGHITA", 22: "HUNEDOARA", 23: "IALOMIŢA", 24: "IAŞI",
                       25: "MARAMUREŞ", 26: "MEHEDINŢI", 27: "MUREŞ", 28: "NEAMŢ", 29: "OLT", 30: "PRAHOVA",
                       31: "SATU MARE", 32: "SĂLAJ", 33: "SIBIU", 34: "SUCEAVA", 35: "TELEORMAN", 36: "TIMIŞ",
                       37: "TULCEA", 38: "VASLUI", 39: "VÂLCEA", 40: "VRANCEA", 41: "BUCUREŞTI"}

    const_dict_1992_96 = {1: "ALBA", 2: "ARAD", 3: "ARGEŞ", 4: "BACĂU", 5: "BIHOR", 6: "BISTRIŢA-NĂSĂUD", 7: "BOTOŞANI",
                          8: "BRAŞOV", 9: "BRĂILA", 10: "BUZĂU", 11: "CARAŞ-SEVERIN", 12: "CĂLĂRAŞI", 13: "CLUJ",
                          14: "CONSTANŢA", 15: "COVASNA", 16: "DÂMBOVIŢA", 17: "DOLJ", 18: "GALAŢI", 19: "GIURGIU",
                          20: "GORJ", 21: "HARGHITA", 22: "HUNEDOARA", 23: "IALOMIŢA", 24: "IAŞI",
                          25: "MARAMUREŞ", 26: "MEHEDINŢI", 27: "MUREŞ", 28: "NEAMŢ", 29: "OLT", 30: "PRAHOVA",
                          31: "SATU MARE", 32: "SĂLAJ", 33: "SIBIU", 34: "SUCEAVA", 35: "TELEORMAN", 36: "TIMIŞ",
                          37: "TULCEA", 38: "VASLUI", 39: "VÂLCEA", 40: "VRANCEA", 41: "BUCUREŞTI", 42: "ILFOV"}

    # Ilfov county was created in 1997, so the numbers after "Iaşi" incremented by one thereafter
    const_dict_2000 = {1: "ALBA", 2: "ARAD", 3: "ARGEŞ", 4: "BACĂU", 5: "BIHOR", 6: "BISTRIŢA-NĂSĂUD", 7: "BOTOŞANI",
                       8: "BRAŞOV", 9: "BRĂILA", 10: "BUZĂU", 11: "CARAŞ-SEVERIN", 12: "CĂLĂRAŞI", 13: "CLUJ",
                       14: "CONSTANŢA", 15: "COVASNA", 16: "DÂMBOVIŢA", 17: "DOLJ", 18: "GALAŢI", 19: "GIURGIU",
                       20: "GORJ", 21: "HARGHITA", 22: "HUNEDOARA", 23: "IALOMIŢA", 24: "IAŞI", 25: "ILFOV",
                       26: "MARAMUREŞ", 27: "MEHEDINŢI", 28: "MUREŞ", 29: "NEAMŢ", 30: "OLT", 31: "PRAHOVA",
                       32: "SATU MARE", 33: "SĂLAJ", 34: "SIBIU", 35: "SUCEAVA", 36: "TELEORMAN", 37: "TIMIŞ",
                       38: "TULCEA", 39: "VASLUI", 40: "VÂLCEA", 41: "VRANCEA", 42: "BUCUREŞTI", 43: "DIASPORA"}

    constituency_text = soup.find('p').text
    if "la nivel" in constituency_text:
        # these are national minority representatives in the lower house, who are voted for one, national constituency
        return "MINORITĂŢI"
    else:
        # the constituency code is the first occurence in the string of the form "nr.DIGITS", where the digits range
        # from 1 to 43. Codes uniquely map to constituency names
        constituency_code = int(re.search("(?<=nr\.)[0-9]+", constituency_text)[0])
        # error out if getting nonsensical codes
        if not 1 <= constituency_code <= 43:
            print(constituency_text)
            raise ValueError("NONSENSICAL CODE ERROR")
        legislature = get_legislature(soup)
        if legislature == "1990-1992":
            return const_dict_1990[constituency_code]
        elif legislature in {"1992-1996", "1996-2000"}:
            return const_dict_1992_96[constituency_code]
        else:
            return const_dict_2000[constituency_code]


def get_deceased_in_office(soup):
    """
    Identifies whether a parliamentarian died in office.

    :param soup: a BeautifulSoup object
    :return: str, "deceased in office" or "no death in office"
    """

    mandate_text = soup.find('p').text
    if "decedat" in mandate_text:
        return "deceased in office"
    else:
        return "no death in office"


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

    legislature = get_legislature(soup)
    leg_start, leg_end = int(legislature.split('-')[0]), legislature.split('-')[1]

    # by default mandates end in December of election year and begin in January of subsequent year; set day to November
    # 30th and December 1st; exceptions are first two post-communist legislatures
    if legislature == "1990-1992":  # first exception is; these are default values, i.e. when
        mandate_start, mandate_end = "1990-06-01", "1992-08-01"
    elif legislature == "1992-1996":  # the second exception is
        mandate_start, mandate_end = "1992-10-01", "1996-01-01"
    else:
        mandate_start, mandate_end = str(leg_start) + "-12-01", leg_end + "-11-30"

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


def get_party_and_first_switch(soup):
    """
    Identifies the party on whose ticket a legislator was elected, and if that legislator switches parties, it also
    identifies the month and year of that switch and receiving party.

    NB: this only considers the first party switch, NOT multiple switches.

    :param soup: a BeautifulSoup object
    :return: a 4-tuple of strings: entry party name, entry party code, first switch date, and destination party code
    """

    dest_party_name, dest_party_code = "", ""

    # get the name of the party with which they entered parliament, and the date of the first party switch
    entry_party_name, entry_party_code = '', ''
    first_switch_date = {"month": '', "year": ''}

    info_fields = soup.find_all('div', class_="boxDep clearfix")
    for i in info_fields:

        if "minoritatilor nationale" in i.contents[0].text:
            entry_party_name, entry_party_code = 'minorities', 'MIN'

        if "Formatiunea politica" in i.contents[0].text:
            for j in i.contents:
                if 'Tag' in str(type(j)) and ':' not in j.text:
                    party_group_text = j.text.replace('\xa0', '').replace('\r', '').replace('\n', '').replace('-', ' ')
                    split_by_departures = party_group_text.split('până în')

                    # sometimes parties simply change names -- ignore these; the form of the text string from which
                    # we extract the date is "  iun. 2001PSD Partidul Social Democrat  din  iun. 2001"
                    if len(split_by_departures) > 1 and 'se transforma' not in split_by_departures[1]:
                        departure_date = split_by_departures[1].strip()

                        departure_month = departure_date.split()[0].replace('.', '').strip()
                        departure_month = short_month_codes[departure_month]

                        departure_year = departure_date.split()[1][:4]

                        first_switch_date = {'month': departure_month, 'year': departure_year}

                        dest_party_name, dest_party_code = destination_party_name(split_by_departures)

                    # get the start party name
                    for p_code in party_codes:
                        if p_code in split_by_departures[0]:
                            entry_party_name, entry_party_code = party_codes[p_code], p_code

                    # covers for bugs related to "PD" also being found in other party names
                    if entry_party_name == 'Partidul Democrat' and 'PDSR' in split_by_departures[0]:
                        entry_party_name, entry_party_code = "Partidul Democraţiei Sociale din România", "PDSR"
                    if entry_party_name == 'Partidul Democrat' and 'PDAR' in split_by_departures[0]:
                        entry_party_name, entry_party_code = "Partidul Democrat Agrar din România", "PDAR"

    # cover for bugs related to party name changes

    # "FDSN" rebranded as "PDSR" in 1993 and
    if entry_party_name == 'Frontul Democrat al Salvarii Nationale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date, dest_party_code = {"month": '', "year": ''}, ""

    # FSN became PD in 1993
    if entry_party_name == 'Frontul Salvării Naţionale':
        if first_switch_date and first_switch_date['year'] == '1993':
            first_switch_date, dest_party_code = {"month": '', "year": ''}, ""

    # "PDSR" rebranded as to "PSD" in 2001
    if entry_party_name == 'Partidul Democraţiei Sociale din România':
        if first_switch_date and first_switch_date['year'] == '2001':
            first_switch_date, dest_party_code = {"month": '', "year": ''}, ""

    # run the data past the ad-hoc party name and switch corrector
    surnames, given_names = get_names(soup)
    legislature = get_legislature(soup)
    corrected_switch_data = adhoc_party_and_switches(surnames, given_names, legislature, entry_party_name,
                                                     entry_party_code, dest_party_code, first_switch_date)
    entry_party_name, entry_party_code, first_switch_date, dest_party_code = corrected_switch_data

    entry_party_code, dest_party_code = party_code_standardiser(entry_party_code, dest_party_code)

    # if the origin and destination party are the same, blank out the destination party and switching
    # NB: this plows over cases where a legislator left their party only to return; this is interesting but rare
    #      behaviour (max 32 people) so I just treat it as "did not switch," which is true, if a bit simplistic
    if dest_party_code:
        if entry_party_code == dest_party_code:
            first_switch_date,  dest_party_code = {"month": '', "year": ''}, ""

    return entry_party_name, entry_party_code, first_switch_date, dest_party_code


def destination_party_name(split_by_departures):
    """
    This script extracts the name of the destination party, when a parliamentarian has switched parties. Often, for
    both political and book-keeping reasons, a parliamentarian is marked as switching from their starting party to
    "independent" and only then go on to join another party. In this case I assume that the destination party is the
    first party AFTER the "independent" stint, therefore assuming that (regardless of duration) the party-switcher was
    never REALLY independent, but that that status was a political and/or bookkeeping illusion. In this format the only
    geniune independents are those that remain in that category and never end up joining another party.

    NB: two ways of marking independents is the word "independent" or "Fără adeziune la formaţiunea politică pentru
        care a candidat la alegeri", meaning "not affiliated with the party for whom they ran at the last election."

    :param split_by_departures: list, a string split by the month of the switch/departure date. For example,
                                ['PNL Partidul Naţional Liberal  ', '  dec. 2006independent  din  dec. 2006  ',
                                '  feb. 2008PDL Partidul Democrat Liberal  din  feb. 2008']
    :return: tuple, the destination party fullname and its code/acronym. In the example above it would be ("Partidul
             Democrat Liberal", "PDL")
    """

    entry_party_name, entry_party_code = "", ""

    # if the second entry "independent"
    if "independent" in split_by_departures[1] or "adeziune" in split_by_departures[1]:

        # if that parliamentarian never joined another party then they remained a genuine independent legislator
        if len(split_by_departures) == 2:
            entry_party_name, entry_party_code = "independent", "IND"

        # else, there's a party after their stint as independent: that's the destination party
        # the format is "feb. 2010PDL Partidul Democrat Liberal  din  feb. 2010"
        else:
            for p_code in party_codes:
                if p_code in split_by_departures[2]:
                    entry_party_name, entry_party_code = party_codes[p_code], p_code
                    # covers for bugs related to "PD" also being found in other party names (viz. "PDSR" and "PDAR")
                    if entry_party_name == 'Partidul Democrat' and 'PDSR' in split_by_departures[2]:
                        entry_party_name, entry_party_code = "Partidul Democraţiei Sociale din România", "PDSR"
                    if entry_party_name == 'Partidul Democrat' and 'PDAR' in split_by_departures[2]:
                        entry_party_name, entry_party_code = "Partidul Democrat Agrar din România", "PDAR"

    else:  # else, we're dealing with straight switches that didn't go through some "independent" phase
        for p_code in party_codes:
            if p_code in split_by_departures[1]:
                entry_party_name, entry_party_code = party_codes[p_code], p_code
                # covers for bugs related to "PD" also being found in other party names (viz. "PDSR" and "PDAR")
                if entry_party_name == 'Partidul Democrat' and 'PDSR' in split_by_departures[1]:
                    entry_party_name, entry_party_code = "Partidul Democraţiei Sociale din România", "PDSR"
                if entry_party_name == 'Partidul Democrat' and 'PDAR' in split_by_departures[1]:
                    entry_party_name, entry_party_code = "Partidul Democrat Agrar din România", "PDAR"

    return entry_party_name, entry_party_code


def adhoc_party_and_switches(surnames, given_names, legislature, entry_party_name, entry_party_code,
                             destination_party_code, first_switch_date):
    """
    In some legislatures some parliamentarians have unusually formatted profiles regarding party names and switches.
    This function catches and corrects that unusualness.

    :param surnames: str
    :param given_names: str
    :param legislature: str
    :param entry_party_name: str
    :param entry_party_code: str
    :param destination_party_code: str
    :param first_switch_date: dict of form {"month": '', "year": ''}
    :return: correct entry party, first switch date, and destination party code
    """

    if surnames == "IORGOVAN" and given_names == "Antonie" and legislature == '1990-1992':
        entry_party_name, entry_party_code, first_switch_date = "independent", "IND", {"month": '', "year": ''}

    if surnames == "CAJAL" and given_names == "Nicolae" and legislature == '1990-1992':
        entry_party_name, entry_party_code, first_switch_date = "independent", "IND", {"month": '', "year": ''}

    if surnames == "BONDARIU" and given_names == "Ionel" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democraţiei Sociale din România", "PDSR", \
                                                                {"month": "12", "year": "1995"}

    if surnames == "BOLD" and given_names == "Ion" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Naţional Ţărănesc Creştin Democrat", \
                                                                "PNŢCD", {"month": "12", "year": "1994"}

    if surnames == "DRĂGHIEA" and given_names == "Nicolae" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democraţiei Sociale din România", "PDSR", \
                                                                {"month": "02", "year": "1995"}

    if surnames == "PASCU" and given_names == "Horia Radu" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Liberal 1993", "PL'93", \
                                                                {"month": "09", "year": "1993"}

    if surnames == "CERVENI" and given_names == "Niculae" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Liberal 1993", "PL'93", \
                                                                {"month": "09", "year": "1993"}

    if surnames == "TĂNASIE" and given_names == "Petru" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democraţiei Sociale din România", "PDSR", \
                                                                {"month": "02", "year": "1996"}

    if surnames == "HRISTU" and given_names == "Ion" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul România Mare", "PRM", \
                                                                {"month": "04", "year": "1993"}

    if surnames == "VINTILESCU" and given_names == "Teodor" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Liberal 1993", "PL'93", \
                                                                {"month": "02", "year": "1994"}

    if surnames == "RĂBAN" and given_names == "Grigore" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Socialist al Muncii", "PSM", \
                                                                {"month": "02", "year": "1995"}

    if surnames == "MÂNDROVICEANU" and given_names == "Vasile" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Liberal 1993", "PL'93", \
                                                                {"month": "03", "year": "1995"}

    if surnames == "JECAN" and given_names == "Aurel" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Unităţi Naţionale a Românilor", "PUNR", \
                                                                {"month": "09", "year": "1996"}

    if surnames == "URSU" and given_names == "Doru Viorel" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democrat", "PD", \
                                                                {"month": "03", "year": "1995"}

    if surnames == "ŢURLEA" and given_names == "Petre" and legislature == '1992-1996':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democraţiei Sociale din România", "PDSR", \
                                                                {"month": "09", "year": "1993"}

    if surnames == "COŞEA" and given_names == "Dumitru Gheorghe Mircea" and legislature == '2004-2008':
        entry_party_name, entry_party_code, first_switch_date = "Partidul Naţional Liberal", "PNL", \
                                                                {"month": "02", "year": "2008"}

    if surnames == "TODIRAŞCU" and given_names == "Valeriu" and legislature == "2012-2016":
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democrat Liberal", "PDL", \
                                                                {"month": "02", "year": "2015"}

    if surnames == "CERNEA" and given_names == "Remus Florinel" and legislature == "2012-2016":
        entry_party_name, entry_party_code, first_switch_date = "Partidul Social Democrat", "PSD", \
                                                                {"month": "05", "year": "2013"}

    if surnames == "SILAGHI" and given_names == "Ovidiu Ioan" and legislature == "2012-2016":
        entry_party_name, entry_party_code, first_switch_date = "Partidul Naţional Liberal", "PNL", \
                                                                {"month": "07", "year": "2014"}

    if surnames == "OPREA" and given_names == "Dumitru" and legislature == "2012-2016":
        entry_party_name, entry_party_code, first_switch_date = "Partidul Democrat Liberal", "PDL", \
                                                                {"month": "02", "year": "2015"}

    # correct "independent" party destinations that are actually transfers to other caucauses
    if legislature in destination_ind_dict:
        fullname = surnames + " " + given_names
        if fullname in destination_ind_dict[legislature]:
            destination_party_code = destination_ind_dict[legislature][fullname]

    return entry_party_name, entry_party_code, first_switch_date, destination_party_code


def party_code_standardiser(entry_party_code, dest_party_code):
    """
    Since some parties have rebranded, it's easier to just use the same name for all times, despite this being
    anachornistic in some cases. The full party name is faithful to the period.
    """
    if entry_party_code == "PD":
        entry_party_code = "PDL"
    if dest_party_code == "PD":
        dest_party_code = "PDL"
    if entry_party_code == "PUR SL":
        entry_party_code = "PC"
    if dest_party_code == "PUR SL":
        dest_party_code = "PC"
    if entry_party_code == "PDSR":
        entry_party_code = "PSD"
    if dest_party_code == "PDSR":
        dest_party_code = "PSD"

    return entry_party_code, dest_party_code


def get_rank_in_first_ppg(soup, mandate_start, mandate_end, surnames, given_names):
    """
    Returns the rank that a legislator held within their first parliamentary party group, and the span of time in which
    they held this rank. The ranks are "membru", "secretar", "vicelider" and "lider", in increasing order.

    :param soup: a BeautifulSoup object
    :param mandate_start: str, the beginning of a mandate, comes in YR-MO-DAY format
    :param mandate_end: str, the end of a mandate, comes in YR-MO-DAY format
    :param surnames: str
    :param given_names: str
    :return: a 2-tuple of string (rank, date range the rank was held)
    """

    # TODO: this ignores if there are second rank-holdings in the same first-party stint. So E.g. Ovidiu Gant in
    #       2012-2016 was vicelider twice without changing parties (but vicelider was interrupted). This code counts
    #       only the first occurence. NEED TO FIX THIS

    # mandate boundaries come in YR-MO-DAY format, but we need MO.YR
    m_start = mandate_start.split("-")[1] + "." + mandate_start.split("-")[0]
    m_end = mandate_end.split("-")[1] + "." + mandate_end.split("-")[0]

    # the default rank is a simple member, and the default date range is start and end of mandate
    # NB: somewhat deceptive default since the rank is only first rank of first party, but mandate may include mutiple
    #     rank and party changes
    rank, date_range = "membru", m_start + "-" + m_end

    # turns out that a couple of legislators from 1990-1996 was never registered in any caucus; return default values
    if (surnames == "MOLDOVAN" and given_names == "Constantin") \
            or (surnames == "MOŢIU" and given_names == "Adrian Ovidiu") \
            or (surnames == "CEONTEA" and given_names == "Radu") \
            or (surnames == "CAZIMIR" and given_names == "Ştefan"):
        return rank, date_range

    # where information lives in the html
    info_fields = soup.find_all('div', class_="boxDep clearfix")
    for i in info_fields:
        # drill down to the field containing PPG info
        if "Grupul parlamentar" in i.contents[0].text:
            ppg1_info = i.find_all('tr')[0]  # focus only on first PPG, hence 0 index
            ppg1_text = ppg1_info.text.replace('\xa0', '').replace('\r', '').replace('\n', '').replace('-', ' ')  # tidy

            high_ranks = {"Secretar", "Vicelider", "Lider"}

            for hr in high_ranks:
                if hr in ppg1_text:  # isolate higher ranks

                    # since date range information is after the rank name, split the string on the rank

                    # if the last entry is empty, then the person had high rank for all of their time in said party,
                    if not ppg1_text.split(hr)[-1]:
                        date_range = m_start + "-" + m_end

                    else:  # else their rank for only a portion of their time in the first party
                        # case 1: they had the rank from one date until another
                        if "din" in ppg1_text.split(hr)[-1] and "până" in ppg1_text.split(hr)[-1]:
                            date_range = ppg1_text.split(hr)[-1].replace("din", '').replace("până în", "-").replace(" ", "")
                        # case 2: held the rank from a certain date until the end of their stay in the first party
                        elif "din" in ppg1_text.split(hr)[-1]:
                            date_range = ppg1_text.split(hr)[-1].replace("din", '').replace(" ", "") + "-" + m_end
                        #  case 3: held the rank from the start of their time in the first party until a certain date
                        else:
                            date_range = m_start + "-" + ppg1_text.split(hr)[-1].replace("până în", '').replace(" ", "")

                    # replace the short month code (e.g. "aug") with its number correspondent (e.g. "08")
                    for smc in short_month_codes:
                        if smc in date_range:
                            date_range = date_range.replace(smc, short_month_codes[smc])

                    # the base data don't always put a period between month and year, so you can get"052016"; fix this
                    # for the start period
                    date_range = date_range[:2] + "." + date_range[2:] if "." not in date_range[:3] else date_range
                    # for the end period
                    date_range = date_range[:-4] + "." + date_range[-4:] if date_range[-5] != "." else date_range

                    rank = hr.lower()  # set the rank

                    # ensure that missing period issue is solved: format MO.YR-MO.YR must have two periods
                    if date_range.count(".") != 2:
                        raise ValueError("INCORRENT DATE RANGE FORMAT")

    return rank, date_range


def assign_unique_person_ids(parl_leg_table):
    """
    Goes through a table of parliamentarian-legislatures and assigns each person (and their associated mandates)
    one unique ID.

    NB: there are two "POP Virigil" in the 1996-2000 legislature with nothing to distinguish them as far as these
    data are concerned (same party, neither switches, same mandates) so I leave these two merged. Nothing can be done.

    :param parl_leg_table: table (as list of lists) of parliamentarian-legislature, where each parl-leg is a row
    :return: None
    """

    # assign person-level ID's
    unique_full_names = {row[5] + ' ' + row[6] for row in parl_leg_table}  # row[5] == surname, row[6] == given name
    unique_person_ids = {ufn: idx for idx, ufn in enumerate(unique_full_names)}
    for parl_leg in parl_leg_table:

        parl_full_name = parl_leg[5] + ' ' + parl_leg[6]
        if parl_full_name in unique_person_ids:

            # some people have identical full names, but different legislatures; handle
            if parl_full_name == 'POPESCU Virgil' and parl_leg[2] == "1990-1992":  # parl_leg[2] = legislature
                parl_leg[0] = 2802
            elif parl_full_name == 'POPESCU Corneliu' and parl_leg[2] == "2004-2008":
                parl_leg[0] = 2803
            else:  # everyone else with unique full names
                parl_leg[0] = unique_person_ids[parl_full_name]

        else:
            print(parl_full_name, " NOT IN FULLNAME SET, ERROR, CHECK")


def seniority(parl_leg_table):
    """
    Add a column at the end of the parliamentarian-legislature table which indicates seniority. A seniority of "1" means
    that this is the first legislature that said parliamentarian served in, "2" means the second legislature, etc.

    :param parl_leg_table: a table (as list of lists) where rows are parliamentarian-legislatures (i.e. info on one
                           parliamentarian in one legislature)
    :return: a parl_leg table where the last column indicates seniorty
    """

    # sort person-legislatures by unique ID and legislature, then group people by unique ID
    parl_leg_table.sort(key=operator.itemgetter(0, 2))  # row[0] == person ID, row[2] == legislature
    people = [person for key, [*person] in itertools.groupby(parl_leg_table, key=operator.itemgetter(0))]

    table_with_seniority_column = []
    for person in people:
        for idx, pers_leg in enumerate(person):
            # add the seniority column at the end; 1-indexed
            table_with_seniority_column.append(pers_leg + [idx + 1])
    return table_with_seniority_column


def former_switcher(parl_leg_table, header):
    """
    For legislators that have served more than one term, add a column indicating if they switched parties in a previous
    mandate. In particular, "1" means that they switched in the mandate immediately before this one, "2" that they
    switched parties during two mandates (notwithstanding how close they are to the current) and "0" means that they
    never switched parties.

    :param parl_leg_table: a table (as list of lists) where rows are parliamentarian-legislatures (i.e. info on one
                           parliamentarian in one legislature)
    :param header: list, header of the parl_leg_table
    :return: a parl_leg table where the last column indicates whether and how a legislator is a former switcher
    """

    table_with_former_switcher_column = []
    pid_col_idx, leg_col_idx = header.index("PersID"), header.index("legislature")
    dest_party_code_col_idx = header.index("destination party code")

    # make a set of strings of PersID-Legislature of each parliamentarian-legislature that features a switch
    pers_legs_with_switch = {str(row[pid_col_idx]) + "." + row[leg_col_idx] for row in parl_leg_table
                             if row[dest_party_code_col_idx]}

    legs = ["1990-1992", "1992-1996", "1996-2000", "2000-2004", "2004-2008", "2008-2012", "2012-2016", "2016-2020"]

    for parl_leg in parl_leg_table:  # for each parliamentarian-legislature
        pid, current_leg = str(parl_leg[pid_col_idx]), parl_leg[leg_col_idx]
        if current_leg == "1990-1992":  # skip first post-revolutionary legislature, nothing before it
            continue
        prior_leg = legs[legs.index(current_leg) - 1]
        prior_switcher = 1 if pid + "." + prior_leg in pers_legs_with_switch else 0
        table_with_former_switcher_column.append(parl_leg + [prior_switcher])
    return table_with_former_switcher_column
