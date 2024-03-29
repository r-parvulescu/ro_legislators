"""
This script collates and processes information from various sources to make a person-year table of legislators in
Romanian parliament, with an eye on the causes of a first party switch.
"""

import csv
import itertools
import operator
from data_tables.dicts.idealogical_switch_cost import ideological_pswitch_costs
from data_tables.dicts.govt_member import govt_parties
from data_tables.dicts.party_leaders import party_leader_changes
from data_tables.dicts.county_politics import county_polit_dict
from data_tables.dicts.corruption_dicts import leader_conv_one_year, leader_conv_multi_year, \
    first_conviction_appeal_possible, final_guilty_verdict, legis_guilty_count
from data_tables.dicts.reference_dicts import party_name_changes, historical_regions_dict, election_years, ppg_size, \
    ethnic_parties, personality_parties
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

    # see how many legislatures each person was ultimately in, i.e. how long their political career was across elections
    career_lens = {pers_leg[pid_col_idx]: 0 for pers_leg in pers_leg_table}
    for pers_leg in pers_leg_table:
        career_lens[pers_leg[pid_col_idx]] += 1

    person_year_table_header = ["person_id", "surnames", "given names", "legis", "legis_clock", "year",
                                "multi_legis_parl", "senate", "constit", "h_region", "senior", "senior_cat",
                                "start_party", "p_size", "p_ethnic", "p_pers", "p_govt", "local_party_overlap",
                                "pre_switch_rank", "rank_change", "p_switch1", "destination_party",
                                "idlgcl_switch_cost",
                                "former_switcher", "elect_year", "lead_change", "leave_early", "lead_conv_one_year",
                                "lead_conv_multi_year", "min_conv_full", "min_conv_old", "min_conv_new",
                                "min_conv_none", "other_legis_conv_full", "pconv_same_yr", "pconv_to_elec",
                                "pconv_perm_mark", "ann_year_only", "ann_to_next_elect", "ann_perm_mark"]

    pers_yr_table = []

    for pers_leg in pers_leg_table:

        # ignore those who died in office: only ~60 mandates out of ~4000 died in office, and of these only 3 switched
        # parties before dying; so not loosing too much information if we throw out data on these dead, and gain model
        # simplicity since we don't need to do multiple-outcome survival models
        if pers_leg[died_col_idx] == "no death in office":

            leg = pers_leg[leg_col_idx]

            # look only at post-2000 legislatures (TODO fill in data for previous legislatures too)
            if leg in {"2000-2004", "2004-2008", "2008-2012", "2012-2016", "2016-2020"}:

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

                seniority_cat = get_seniority_cat(senior)

                if s_party in party_name_changes and \
                        leg in {"2000-2004", "2004-2008", "2008-2012", "2012-2016", "2016-2020"}:
                    s_party = party_name_changes[s_party]

                h_reg = historical_regions_dict[const]
                s_party_ethnic = 1 if s_party in ethnic_parties else 0
                s_personality_party = 1 if s_party in personality_parties else 0

                for idx, yr in enumerate(years_in_leg):
                    legis_clock = idx + 1
                    s_ppg_size = get_ppg_size(s_party, senate, yr, leg, pool_chambers=True) if yr > 2008 else ""
                    govt = govt_parties[yr][s_party]
                    local_party_overlap = get_local_govt_parties(leg, const, s_party)
                    party_switch = 1 if p_switch_yr and int(yr) == int(p_switch_yr) else 0
                    elec_yr = 1 if int(yr) in election_years else 0
                    leader_change = 1 if yr in party_leader_changes and s_party in party_leader_changes[yr] else 0
                    leave_early = 1 if yr == last_year_in_leg and last_month_in_leg <= 5 else 0
                    dest_party = pers_leg[dest_party_col_idx] if party_switch else ""

                    # catch and clean potential issues arising from ppg changes, like party group fusions
                    party_switch, p_switch_yr, dest_party = ad_hoc_ppg_changes(s_party, dest_party, yr,
                                                                               party_switch, p_switch_yr)
                    pre_switch_rank = get_pre_switch_rank(header, pers_leg, yr)

                    idlgcl_switch_cost = ideological_switch_cost(s_party, dest_party, yr) if dest_party else ""

                    cnvct_data = get_convictions_data(yr, s_party)

                    lead_conv_one_yr = cnvct_data["lead_conv_one_year"]
                    lead_conv_multi_yr = cnvct_data["lead_conv_multi_year"]
                    mconv_full, mconv_old = cnvct_data["min_conv_full"], cnvct_data["min_conv_old"]
                    mconv_new, mconv_none = cnvct_data["min_conv_new"], cnvct_data["min_conv_none"]
                    others_legs_conv_full = cnvct_data["legis_conv_full"]
                    pconv_appeal_same_yr = self_convicted_appeal(surnames, given_names, yr, leg, "same year")
                    pconv_appeal_to_elec = self_convicted_appeal(surnames, given_names, yr, leg, "until next election")
                    pconv_appeal_pmark = self_convicted_appeal(surnames, given_names, yr, leg, "permanent mark")

                    person_year = [pid, surnames, given_names, leg, legis_clock, yr, multi_legis_parl, senate, const,
                                   h_reg, senior, seniority_cat, s_party, s_ppg_size, s_party_ethnic,
                                   s_personality_party, govt, local_party_overlap, pre_switch_rank, party_switch,
                                   dest_party, idlgcl_switch_cost, former_switcher, elec_yr, leader_change,
                                   leave_early, lead_conv_one_yr, lead_conv_multi_yr, mconv_full, mconv_old, mconv_new,
                                   mconv_none, others_legs_conv_full, pconv_appeal_same_yr, pconv_appeal_to_elec,
                                   pconv_appeal_pmark]

                    pers_yr_table.append(person_year)

    # add rank change column
    pers_yr_table = rank_change(pers_yr_table, person_year_table_header)

    with open(person_year_table_out_path, 'w') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(person_year_table_header)
        [writer.writerow(p_yr) for p_yr in pers_yr_table]

    first_switch_risk_set(pers_yr_table, risk_set_table_out_path, person_year_table_header)
    first_switch_risk_set(pers_yr_table, risk_set_table_out_path, person_year_table_header, multi_year_only=True)


def get_seniority_cat(senior):
    """Map a seniority category number to a string."""
    # novice = first legislature; journeyman = send; master = third or more
    seniority_cat_dict = {1: "novice", 2: "journeyman"}
    seniority_cat = "master"  # implicit category "3"
    if int(senior) in seniority_cat_dict:
        seniority_cat = seniority_cat_dict[int(senior)]
    return seniority_cat


def ad_hoc_ppg_changes(s_party, dest_party, yr, party_switch, p_switch_yr):
    """Catches and corrects possible errors arising from party changes, fusions, etc."""
    # since the PP DD and UNPR fused around May 2015, any PP DD -> UNPR transfers in 2015 should not
    # be counted as party switches
    if s_party == "PP DD" and dest_party == "UPPR" and int(yr) == 2015:
        party_switch, p_switch_yr, dest_party = 0, '', ''
    # likewise for the merger between PDL and PNL in 2015; any PDL-PNL moves in 2015 aren't switches
    if s_party == "PDL" and dest_party == "PNL" and int(yr) == 2015:
        party_switch, p_switch_yr, dest_party = 0, '', ''
    # the Conservative Party (PC) also merged with a breakaway wing of the PNL on 19 June 2015 to
    # form ALDE; so any PC -> ALDE moves in 2015 are NOT switches
    if s_party == "PC" and dest_party == "ALDE" and int(yr) == 2015:
        party_switch, p_switch_yr, dest_party = 0, '', ''
    return party_switch, p_switch_yr, dest_party


def get_pre_switch_rank(header, pers_leg, yr):
    """
    Get the PPG rank (e.g. secretary) of the legislator BEFORE they switched parties.
    NB: if they never switched parties, this is just the rank.
    """
    rank_col_idx, rank_dates_col_ind = header.index("entry ppg rank"), header.index("entry ppg rank dates")
    # get the rank of the person within the PPG, relative to the daterange of the rank
    lower_date = int(pers_leg[rank_dates_col_ind].split("-")[0].split(".")[1])  # in MO.YR-MO.YR format
    upper_date = int(pers_leg[rank_dates_col_ind].split("-")[1].split(".")[1])
    pre_switch_rank = pers_leg[rank_col_idx] if lower_date <= yr <= upper_date else "membru"
    return pre_switch_rank


def get_ppg_size(s_party, senator, yr, legis, pool_chambers=True):
    """
    Get the size of a legislator's PPG, counted at the start of a calendar year.

    NB: only has data from 2009 to 2020 (inclusive)

    :param s_party: str, e.g. "PSD"
    :param senator: int, 1 if a senator 0 if a member of the lower house, the chamber of deputies
    :param yr: str or int, e.g. 2013
    :param legis: str, e.g. "2008-2012"
    :param pool_chambers: bool, whether to pool the PPG sizes of the Senate and Chamber of Deputies; True by default
    :return: int, the size of the PPG at the beginning of that calendar year
    """

    # NB: certain parties ran in electoral alliances and then caucused together, for at least part of a legislature.
    #     The dict below shows which small parties were in which caucuses, and when.
    small_party_caucus_switch = {"PC": {"2008-2012": {"ppg switch date": "02.2011",
                                                      "pre switch ppg": "PSD",
                                                      "post switch ppg": "PNL"}},
                                 "UNPR": {"2012-2016": {"ppg switch date": "02.2016",
                                                        "pre switch ppg": "PSD",
                                                        "post switch ppg": "UNPR"}}
                                 }
    if s_party in small_party_caucus_switch:
        if legis in small_party_caucus_switch[s_party]:
            # NB: by convention, I take all years before (INCLUDING the switch year) as pre switch ppg years
            switch_year = int(small_party_caucus_switch[s_party][legis]["ppg switch date"].split(".")[-1])
            if yr <= switch_year:
                s_party = small_party_caucus_switch[s_party][legis]["pre switch ppg"]
            else:
                s_party = small_party_caucus_switch[s_party][legis]["post switch ppg"]

    ppg_size_senat = ppg_size[yr]["SENAT"][s_party] if s_party != "MIN" else 0
    ppg_size_cdep = ppg_size[yr]["CDEP"][s_party]

    if pool_chambers:
        return ppg_size_senat + ppg_size_cdep
    else:
        return ppg_size_senat if senator else ppg_size_cdep


def get_local_govt_parties(legislature, constituency, own_party):
    """
    It may matter for a legislator's switch decision what the political alignment of the local government in their
    constituency is, because (a) legislative politicians may have local ambitions, and especially (b) local executives
    tend to control much of the pork that a legislators would want to send, guide, apply, etc.

    In Romanian both the county council (whose majority is represented by the council president) and the mayor of the
    city that is the county seat (always the largest in the county) are important figures in local politics with
    significant discretionary budget and political powers. Therefore, if in any given year the legislator's party is
    the same as that of BOTH the county council president AND the county seat mayor, we give a value of "full overlap."
    If only one of the two figures align with the legislator's party then it's a "partial overlap" and if none align
    then there is "no overlap."

    :param legislature: str, e.g. "2008-2012"
    :param constituency: str, e.g. "CLUJ"
    :param own_party: the party code of the legislator in this year, e.g. PDL
    :return str: full overlap, partial overlap, no overlap
    """

    # for now I only have data on local politics for these three legislatures
    if legislature not in {"2008-2012", "2012-2016", "2016-2020"}:
        return ""

    cc_pres_party = county_polit_dict[legislature][constituency]["CC Pres"]
    cs_mayor_party = county_polit_dict[legislature][constituency]["CS Mayor"]

    if own_party == cc_pres_party and own_party == cs_mayor_party:
        return "full overlap"
    elif own_party == cc_pres_party or own_party == cs_mayor_party:
        return "partial overlap"
    else:
        return "no overlap"

    # TODO do this also with a different measure, namely whether local party figures are in the governing coalition,
    #  regardless of whether or not they're one's own party


def get_convictions_data(yr, s_party):
    """Get convictions data by checking external conviction dictionaries. Return a dict of information on convictions"""

    conviction_dict = {"lead_conv_one_year": 0, "lead_conv_multi_year": 0,
                       "min_conv_full": 0, "min_conv_old": 0, "min_conv_new": 0, "min_conv_none": 0,
                       "legis_conv_full": 0}

    if yr in leader_conv_one_year and s_party in leader_conv_one_year[yr]:
        conviction_dict["lead_conv_one_year"] = 1

    if yr in leader_conv_multi_year and s_party in leader_conv_multi_year[yr]:
        conviction_dict["lead_conv_multi_year"] = 1

    if yr in legis_guilty_count and s_party in legis_guilty_count[yr]:
        conviction_dict["legis_conv_full"] = legis_guilty_count[yr][s_party]

    return conviction_dict


def self_convicted_appeal(surnames, given_names, yr, legis, condition):
    """
    Check the dictionary that records which legislators were convicted when (with possibility of appeal) and return 1
    for different conditions of oneself having been convicted with possibility of appeal. If no conditions are met,
    return 0.

    NB: we need to be careful throughout not to count people who received a final conviction, i.e. one not subject to
        appeal

    :param surnames: str
    :param given_names: str
    :param yr: str or int, e.g. 2014, "2015"
    :param legis: str, e.g. "2000-2004"
    :param condition: str, either "same year", "until next election" or "permanent mark"
    :return: int, a 1 or 0
    """
    fullname = surnames + " " + given_names
    last_legis_year = int(legis.split("-")[1])
    if fullname in first_conviction_appeal_possible:
        first_conv_date = first_conviction_appeal_possible[fullname].split(".")  # comes in "DAY.MO.YR" format
        first_conv_month, first_conv_year = first_conv_date[1], int(first_conv_date[2])

        # ignore everyone who got their final conviction in this year or earlier; again, date in DAY.MO.YR format
        if fullname in final_guilty_verdict and int(final_guilty_verdict[fullname].split(".")[-1]) <= int(yr):
            return 0

        if condition == "same year" and int(yr) == first_conv_year:
            return 1

        if condition == "until next election" and first_conv_year <= int(yr) <= last_legis_year:
            return 1
        if condition == "permanent mark" and first_conv_year <= int(yr):
            return 1
    return 0


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


def rank_change(person_year_table, header):
    """
    Sees how one's rank within the first parliamentary party group has changed between years.

    NB: by combining person-years in the first year (who by definition cannot have been demoted) with those in the
        who do not move even when they can, this thing committs a pretty big fudge. I do  it to get a rough sense.

    :param person_year_table:
    :param header:
    :return:
    """
    # intialise the new table
    py_table_with_rank_change = []

    # initialise the dictionary of position rankings
    rank_dict = {"lider": 3, "vicelider": 2, "secretar": 1, "membru": 0}

    # get column indexes
    pid_col_idx, rank_col_idx = header.index("person_id"), header.index("pre_switch_rank")
    leg_col_idx, yr_col_idx = header.index("legis"), header.index("year")

    # sort table by pid and year
    person_year_table.sort(key=operator.itemgetter(pid_col_idx, yr_col_idx))

    # group table by person
    people = [person for key, [*person] in itertools.groupby(person_year_table, key=operator.itemgetter(pid_col_idx))]

    for person in people:
        # then group by legislature
        pers_legs = [p_leg for key, [*p_leg] in itertools.groupby(person, key=operator.itemgetter(leg_col_idx))]

        for p_leg in pers_legs:
            for idx, pers_yr in enumerate(p_leg):
                if idx > 0:
                    current_rank, previous_rank = pers_yr[rank_col_idx], p_leg[idx - 1][rank_col_idx]
                    if rank_dict[current_rank] > rank_dict[previous_rank]:
                        delta_rank = "increase"
                    elif rank_dict[current_rank] == rank_dict[previous_rank]:
                        delta_rank = "no change"
                    else:  # rank_dict[current_rank] < rank_dict[previous_rank]:
                        delta_rank = "decrease"
                else:  # first year of legislature, no rank change was possible
                    delta_rank = "no change"
                py_table_with_rank_change.append(pers_yr[:rank_col_idx + 1] + [delta_rank] + pers_yr[rank_col_idx + 1:])
    return py_table_with_rank_change


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
