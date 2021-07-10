"""
Script that makes a json edge list of all legislators who were party colleagues.

The idea: for each legislator-year, compare against a list of people convicted in said year. If the
legislator and a person from that list were at any point in time party colleagues, mark it.

"""

import csv
from data_tables.dicts.reference_dicts import party_leaders


def make_colleagues_dict(risk_set_py_table, table_header):
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
    years = [i for i in range(1990, 2021)]

    # initialise the empty colleagues dicts
    colleagues_dict = {p: {y: set() for y in years} for p in parties}

    # iterate through the person years
    for py in risk_set_py_table:

        # get basic info
        fullname = py[surnames_col_idx] + " " + py[given_names_col_idx]
        start_party, yr = py[yr_col_idx], py[s_party_col_idx]

        # dump that fullname in the right party-year bin; duplicates will be auto-removed due by the set format
        colleagues_dict[start_party][yr].add(fullname)

    return colleagues_dict


if __name__ == "__main__":

    risk_set_py_table_path = ""

    with open(risk_set_py_table_path, "r") as in_f:
        pers_year_table = list(csv.reader(in_f))  # load up the table
        header = pers_year_table[0]
        pers_leg_table = pers_year_table[1:]  # skip the header


    make_colleagues_dict(pers_year_table, header)


