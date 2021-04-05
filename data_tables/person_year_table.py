"""
This script collates and processes information from various sources to make a person-year table of legislators in
Romanian parliament, with an eye on the causes of a first party switch.
"""

import csv
import itertools
import operator
from data_tables.dicts.idealogical_switch_cost import ideological_pswitch_costs
from data_tables.dicts.corruption_dicts import leader_conv_one_year, leader_conv_multi_year, min_conv_full, \
    min_conv_old, min_conv_new, min_conv_none, media_announcement_dict
from data_tables.dicts.reference_dicts import party_name_changes, historical_regions_dict, govt_parties, \
    election_years, party_leader_changes, party_size, ethnic_parties, personality_parties
from local import root


def make_person_year_table(person_legislature_table_path, person_year_table_out_path, risk_set_table_out_path):
    """
    Starting from a person-legislature table (where each row is one 4-year legislative mandate of one person) create a
    person-year table, where each row represents the data from one legislator in one year.

    :param person_legislature_table_path: str, path to the person-legislature table
    :param person_year_table_out_path: str, path where we want the person-year table to live
    :param risk_set_table_out_path: str, path where we want the rist set table to live
    :return: None
    """

    with open(person_legislature_table_path, 'r') as in_f:
        pers_leg_table = list(csv.reader(in_f))
        header = pers_leg_table[0]
        pers_leg_table = pers_leg_table[1:]  # skip the header

    # get column indexes for the person-legislature table
    surnames_col_idx, given_names_col_idx = header.index("surnames"), header.index("given names")
    mandate_start_col_idx, mandate_end_col_idx = header.index("mandate start"), header.index("mandate end")
    pid_col_idx, seniority_col_idx = header.index("PersID"), header.index("seniority")
    leg_col_idx, chamb_col_idx = header.index("legislature"), header.index("chamber")
    const_col_idx, s_party_col_idx = header.index("constituency"), header.index("entry party code")
    p_switch_yr_col_idx, died_col_idx = header.index("first party switch year"), header.index("death status")
    dest_party_col_idx, frmr_switcher_col_idx = header.index("destination party code"), header.index("former switcher")
    rank_col_idx, rank_dates_col_ind = header.index("entry ppg rank"), header.index("entry ppg rank dates")

    # see how many legislatures each person was ultimately in, i.e. how long their political career was across elections
    career_lens = {pers_leg[pid_col_idx]: 0 for pers_leg in pers_leg_table}
    for pers_leg in pers_leg_table:
        career_lens[pers_leg[pid_col_idx]] += 1

    person_year_table_header = ["person_id", "surnames", "given names", "legis", "legis_clock", "year",
                                "multi_legis_parl", "senate", "constit",
                                "h_region", "senior", "senior_cat", "start_party", "p_size", "p_ethnic", "p_pers",
                                "p_govt", "pre_switch_rank", "p_switch1", "destination_party", "idlgcl_switch_cost",
                                "former_switcher", "elect_year", "lead_change", "leave_early", "lead_conv_one_year",
                                "lead_conv_multi_year", "min_conv_full", "min_conv_old", "min_conv_new",
                                "min_conv_none",  "ann_year_only", "ann_to_next_elect", "ann_perm_mark"]

    pers_yr_table = []

    for pers_leg in pers_leg_table:

        # ignore those who died in office: only ~60 mandates out of ~4000 died in office, and of these only 3 switched
        # parties before dying; so not loosing too much information if we throw out data on these dead, and gain model
        # simplicity since we don't need to do multiple-outcome survival models
        if pers_leg[died_col_idx] == "no death in office":

            # look only at post-2000 legislatures (TODO fill in data for previous legislatures too)
            if pers_leg[leg_col_idx] in {"2000-2004", "2004-2008", "2008-2012", "2012-2016", "2016-2020"}:

                # get names
                surnames, given_names = pers_leg[surnames_col_idx], pers_leg[given_names_col_idx]

                # see whether this is, ultimately, a multi-legislature parliamentarian
                multi_legis_parl = 1 if career_lens[pers_leg[0]] > 1 else 0

                # get the number of years that the parliamentarian served in a particular legislature
                # NB: since elections are typically in Nov/Dec, mandates usually start in December. Ignore that first
                # year since politics don't really start until January of the next year, so a mandate from 2004-2008 is
                # really 2005-2008, which is still 4 years (inclusive), up to the elections in Nov/Dec 2008.
                if int(pers_leg[mandate_start_col_idx].split('-')[0]) in {2000, 2004, 2008, 2012, 2016} \
                        and int(pers_leg[mandate_start_col_idx].split('-')[1]) == 12:
                    # NB: mandate info has form = "YR-MO-DAY"
                    first_year_in_leg = int(pers_leg[mandate_start_col_idx].split('-')[0]) + 1
                else:
                    first_year_in_leg = int(pers_leg[mandate_start_col_idx].split('-')[0])

                last_year_in_leg = int(pers_leg[mandate_end_col_idx].split('-')[0])
                last_month_in_leg = int(pers_leg[mandate_end_col_idx].split('-')[1])
                years_in_leg = list(range(first_year_in_leg, last_year_in_leg + 1))

                pid, senior, leg, = pers_leg[pid_col_idx], pers_leg[seniority_col_idx], pers_leg[leg_col_idx]
                senate = 1 if pers_leg[chamb_col_idx] == "SENATOR" else 0
                const, former_switcher = pers_leg[const_col_idx], pers_leg[frmr_switcher_col_idx]
                s_party, p_switch_yr = pers_leg[s_party_col_idx], pers_leg[p_switch_yr_col_idx]

                # novice = first legislature; journeyman = send; master = third or more
                seniority_cat_dict = {1: "novice", 2: "journeyman"}
                seniority_cat = "master"
                if int(senior) in seniority_cat_dict:
                    seniority_cat = seniority_cat_dict[int(senior)]

                if s_party in party_name_changes:
                    s_party = party_name_changes[s_party]

                h_reg = historical_regions_dict[const]
                s_party_size = party_size[leg][s_party]
                s_party_ethnic = 1 if s_party in ethnic_parties else 0
                s_personality_party = 1 if s_party in personality_parties else 0

                for idx, yr in enumerate(years_in_leg):
                    legis_clock = idx + 1
                    govt = govt_parties[yr][s_party]
                    party_switch = 1 if p_switch_yr and int(yr) == int(p_switch_yr) else 0
                    elec_yr = 1 if int(yr) in election_years else 0
                    leader_change = 1 if yr in party_leader_changes and s_party in party_leader_changes[yr] else 0
                    leave_early = 1 if yr == last_year_in_leg and last_month_in_leg <= 5 else 0

                    dest_party = pers_leg[dest_party_col_idx] if party_switch else ""

                    # since the PP DD and UNPR fused around May 2015, any PP DD -> UNPR transfers in 2015 should not
                    # be counted as party switches
                    if s_party == "PP DD" and dest_party == "UPPR" and int(yr) == 2015:
                        party_switch, p_switch_yr, dest_party = 0, '', ''
                    # likewise for the merger between PDL and PNL in 2014; any PDL-PNL moves in 2014 aren't switches
                    if s_party == "PDL" and dest_party == "PNL" and int(yr) == 2014:
                        party_switch, p_switch_yr, dest_party = 0, '', ''
                    # the Conservative Party (PC) also merged with a breakaway wing of the PNL on 19 June 2015 to
                    # form ALDE; so any PC -> ALDE moves in 2015 are NOT switches
                    if s_party == "PC" and dest_party == "ALDE" and int(yr) == 2015:
                        party_switch, p_switch_yr, dest_party = 0, '', ''

                    # get the rank of ther person within the PPG, relative to the daterange of the rank
                    lower_date = int(pers_leg[rank_dates_col_ind].split("-")[0].split(".")[1])  # in MO.YR-MO.YR format
                    upper_date = int(pers_leg[rank_dates_col_ind].split("-")[1].split(".")[1])
                    pre_switch_rank = pers_leg[rank_col_idx] if lower_date <= yr <= upper_date else "membru"

                    idlgcl_switch_cost = ideological_switch_cost(s_party, dest_party, yr) if dest_party else ""

                    # leader conviction columns
                    lead_conv_one_yr = 0
                    if yr in leader_conv_one_year and s_party in leader_conv_one_year[yr]:
                        lead_conv_one_yr = 1

                    lead_conv_multi_yr = 0
                    if yr in leader_conv_multi_year and s_party in leader_conv_multi_year[yr]:
                        lead_conv_multi_yr = 1

                    # ministerial conviction columns
                    min_conv_f = 0
                    if yr in min_conv_full and s_party in min_conv_full[yr]:
                        min_conv_f = min_conv_full[yr][s_party]

                    min_conv_o = 0
                    if yr in min_conv_old and s_party in min_conv_old[yr]:
                        min_conv_o = min_conv_old[yr][s_party]

                    min_conv_n = 0
                    if yr in min_conv_new and s_party in min_conv_new[yr]:
                        min_conv_n = min_conv_new[yr][s_party]

                    min_conv_no = 0
                    if yr in min_conv_none and s_party in min_conv_none[yr]:
                        min_conv_no = min_conv_none[yr][s_party]

                    person_year = [pid, surnames, given_names, leg, legis_clock, yr, multi_legis_parl, senate, const,
                                   h_reg, senior, seniority_cat, s_party, s_party_size, s_party_ethnic,
                                   s_personality_party, govt, pre_switch_rank, party_switch, dest_party,
                                   idlgcl_switch_cost, former_switcher,  elec_yr, leader_change, leave_early,
                                   lead_conv_one_yr, lead_conv_multi_yr, min_conv_f, min_conv_o, min_conv_n,
                                   min_conv_no]

                    pers_yr_table.append(person_year)

    # add the media announcement
    pers_yr_table = media_announcement_corruption(pers_yr_table, person_year_table_header)

    with open(person_year_table_out_path, 'w') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(person_year_table_header)
        [writer.writerow(p_yr) for p_yr in pers_yr_table]

    first_switch_risk_set(pers_yr_table, risk_set_table_out_path, person_year_table_header)
    first_switch_risk_set(pers_yr_table, risk_set_table_out_path, person_year_table_header, multi_year_only=True)


def ideological_switch_cost(entry_party_code, destination_party_code, year):
    """
    Looks up the party switch edge (e.g. "PC-ALDE" means "from PC to ALDE") in the edge list and returns the associated
    edge weight, i.e. cost of switching. Transform the edge value into a categorical and set a default for no switching.

    :param entry_party_code: str
    :param destination_party_code: str
    :param year: str or int
    :return string, "low", "medium", or "high"
    """

    edge = entry_party_code + "-" + destination_party_code
    cost_map = {0: 'low', 1: 'medium', 2: 'high'}
    if entry_party_code != "PNL" and destination_party_code != "PNL":
        switch_cost = ideological_pswitch_costs["any period"][edge]
    else:  # edge includes PNL
        if int(year) <= 2014:
            switch_cost = ideological_pswitch_costs["pre-2014"][edge]
        else:  # after 2014 (exclusive)
            switch_cost = ideological_pswitch_costs["post-2014"][edge]
    return cost_map[switch_cost]


def media_announcement_corruption(person_year_table, header):
    """
    Adds three indicator columns:
    (a) "1" if one heard about a media piece reporting on one's putative corruption in a given calendar year
    (b) "1" if one heard about a media piece reporting on one's putative corruption in a given calendar year and all
        subsequent calendar years until the end of one's mandate
    (c) "1" if one heard about a media piece reporting on one's putative corruption in a given calendar year and all
        subsequent calendar years until the end of one's political career, i.e. when they drop out of the dataset

    :param person_year_table: table of person years, as a list of lists
    :param header: list, the table header for the person_year_table
    :return a person-year table with three extra columns relating to media reporting
    """

    surnames_col_idx, given_names_col_idx = header.index("surnames"), header.index("given names")
    leg_col_idx, yr_col_idx = header.index("legis"), header.index("year")

    table_with_media_reporting_columns = []

    for pers_year in person_year_table:
        leg, yr = pers_year[leg_col_idx], int(pers_year[yr_col_idx])
        fullname = pers_year[surnames_col_idx] + " " + pers_year[given_names_col_idx]
        new_cols = [0, 0, 0]  # in this order: a, b, c (see docstring for meaning of letters)
        if fullname in media_announcement_dict:
            announcement_year = int(media_announcement_dict[fullname].split(".")[-1])

            # for all years after the announcement, inclusive
            if announcement_year <= yr:
                new_cols[2] = 1

            # for all years after the announcement (inclusive) until the final legislature year (inclusive)
            if announcement_year <= yr <= int(leg.split("-")[1]):  # leg in form of "2012-2016"
                new_cols[1] = 1

            # only for the calendar year of the announcement
            if announcement_year == yr:
                new_cols[0] = 1

        table_with_media_reporting_columns.append(pers_year + new_cols)
    return table_with_media_reporting_columns


def first_switch_risk_set(person_year_table, risk_set_table_out_path, header, multi_year_only=False):
    """
    To facilitate survival analysis where we only care about time to first party switch, create an accurate risk set
    where person years are included only up to (and including) the year in which the first party switch occurs. After
    that point, that person is out of the risk set, since they are no longer at risk of a first departure

    NB: I leave recurring party switches out of this since that's a qualitatively different dynamic.

    :param person_year_table: table of person years, as a list of lists
    :param risk_set_table_out_path: str, path where we want the risk set table to live
    :param header: list, the table header for the person_year_table
    :param multi_year_only: bool, switch to only keep people that we observe for more than one year
    :return: None
    """

    # get header column indexes
    pid_col_idx, yr_col_idx = header.index("person_id"), header.index("year")
    leg_col_idx, pswitch1_indicator_col_idx = header.index("legis"), header.index("p_switch1")

    if multi_year_only:
        risk_set_table_out_path = risk_set_table_out_path[:-4] + "_multi_year_only.csv"

    # sort by person-ID and year, group by person ID
    person_year_table.sort(key=operator.itemgetter(pid_col_idx, yr_col_idx))
    people = [person for key, [*person] in itertools.groupby(person_year_table, key=operator.itemgetter(pid_col_idx))]

    first_switch_risk_set_table = []
    for person in people:
        if multi_year_only and len(person) < 2:
            continue

        # now group the person by legislature
        pers_legs = [p_leg for key, [*p_leg] in itertools.groupby(person, key=operator.itemgetter(leg_col_idx))]

        for p_leg in pers_legs:
            # find the year, if any, in which the person switched parties
            party_switch_year = ''
            for pers_yr in p_leg:
                if int(pers_yr[pswitch1_indicator_col_idx]) == 1:
                    party_switch_year = int(pers_yr[yr_col_idx])
            # if there was a party switch, only include pre-switch years (switch year inclusive)
            for pers_yr in p_leg:
                if party_switch_year:
                    if int(pers_yr[yr_col_idx]) <= party_switch_year:
                        first_switch_risk_set_table.append(pers_yr)
                else:
                    first_switch_risk_set_table.append(pers_yr)

    with open(risk_set_table_out_path, 'w') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)
        [writer.writerow(p_yr) for p_yr in first_switch_risk_set_table]


if __name__ == "__main__":
    trunk = "data/parliamentarians/"
    person_legislature_path = root + trunk + 'parliamentarians_person_legislature_table.csv'
    person_year_path = root + trunk + "parliamentarians_person_year_table.csv"
    risk_set_path = root + trunk + "parliamentarians_first_party_switch_risk_set.csv"
    make_person_year_table(person_legislature_path, person_year_path, risk_set_path)
