"""
Script that makes a json edge list of all legislators who were party colleagues.

The idea: for each legislator-year, compare against a list of people convicted in said year. If the
legislator and a person from that list were at any point in time party colleagues, mark it.

"""

import csv
from local import root
from data_tables.dicts.party_leaders import party_leaders


def colleagues_party_bins(risk_set_py_table, table_header):
    """
    Make a dict, where first level keys are parties, second level keys are years, and values are sets of full names of
    legislators. All people in that set were party colleagues in a given year.

    NB: I use the risk-set person-year table (i.e. the one that excludes years AFTER a legislator switched parties
        for the first time within a legislature) in order to constrain the function to just careers before switching.
        Post-switch careers are handled separately.

    :param risk_set_py_table: table as list of lists, contains person years, where a legislator's years are absent
                              if they occur AFTER a first party switch (no header in this table)
    :param table_header, list, the header of the risk_set_py_table
    :return the colleagues_dict

    """

    surnames_col_idx, given_names_col_idx = table_header.index("surnames"), table_header.index("given names")
    yr_col_idx, s_party_col_idx = table_header.index("year"), table_header.index("start_party")

    parties = party_leaders.keys()
    years = [str(i) for i in range(1990, 2021)]

    # initialise the empty colleagues dicts
    party_year_colleagues = {p: {y: set() for y in years} for p in parties}

    # iterate through the person years
    for py in risk_set_py_table:

        # get basic info
        fullname = py[surnames_col_idx] + " " + py[given_names_col_idx]
        start_party, yr = str(py[s_party_col_idx]), py[yr_col_idx]

        # dump that fullname in the right party-year bin; duplicates will be auto-removed due by the set format
        party_year_colleagues[start_party][yr].add(fullname)

    return party_year_colleagues


def colleagues_person_bins(risk_set_py_table, table_header):
    """
    Make a dict, where key is fullname of legislator and value is a set of strings, where each string is the
    fullname of a party colleague and a year in which they were colleagues.

    """

    # get colleagues binned by party and year
    coll_pbin = colleagues_party_bins(risk_set_py_table, table_header)

    # initialise the empty dict of the form {person: set(all of their colleagues, in person-year format)}
    colleague_dict = {}

    for party in coll_pbin:  # loop through all parties
        for year in coll_pbin[party]:  # through all years

            colleagues_that_year = coll_pbin[party][year]

            for person in coll_pbin[party][year]:  # loop through all legislators

                if person not in colleague_dict:  # if the person is not in the person dict, add them
                    colleague_dict.update({person: set()})

                # add colleagues to that person's lifetime colleague set
                for cllg in colleagues_that_year:
                    colleague_dict[person].add(str(cllg) + " - " + str(year))

    return colleague_dict


if __name__ == "__main__":

    trunk = "data/parliamentarians/"
    risk_set_py_table_path = root + trunk + "parliamentarians_first_party_switch_risk_set.csv"

    with open(risk_set_py_table_path, "r") as in_f:
        pers_year_table = list(csv.reader(in_f))  # load up the table
        header = pers_year_table[0]
        pers_year_table = pers_year_table[1:]  # skip the header

    #colls = colleagues_person_bins(pers_year_table, header)



