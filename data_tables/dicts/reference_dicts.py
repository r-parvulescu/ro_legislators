"""Reference dictionaries for baseline information."""

ethnic_parties = {"MIN", "UDMR"}

personality_parties = {"PMP", "PP DD", "ALDE", "PC"}

# hard to say if PRM post-2000 was "Vadim's party" in the same sense that ALDE was Tăriceanu's party: my feeling is
# "no", PRM was less tied to its founder, but this is debatable
personality_parties_names = {"Partidul Mişcarea Populară", "Partidul Poporului - Dan Diaconescu",
                             "Alianţa Liberalior şi Democraţilor", "Partidul Conservator"}

# NB: I map PNTCD and FC to PDL because they were tiny and jointly on the list with PDL for only one post-2000
# legislature, then went back into the unknown. unlike UNPR and PC, who were there for longer and actually mattered as
# independent PPGs
party_name_dict = {"Partidul Democraţiei Sociale din România": "Partidul Social Democrat",
                   "Partidul Democrat": "Partidul Democrat Liberal",
                   "Partidul Social Umanist din România (social liberal)": "Partidul Conservator",
                   "Partidul Naţional Ţărănesc Creştin Democrat": "Partidul Democrat Liberal",
                   "Forţa Civică": "Partidul Democrat Liberal",
                   "minorities": "Grupul Minorităţilor Naţionale"}

# "PD" rebranded to "PDL" in 2007, "PUR SL" changed its name to "PC" in 2005
# NB: these apply only post-2000!
party_name_changes = {"PD": "PDL", "PUR SL": "PC", "PDSR": "PSD", "PNTCD": "PDL", "FC": "PDL"}

election_years = {1990, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020}

leg_chamb_size = {"2000-2004": {"SENATOR": 140, "DEPUTAT": 345},
                  "2004-2008": {"SENATOR": 137, "DEPUTAT": 332},
                  "2008-2012": {"SENATOR": 137, "DEPUTAT": 334},
                  "2012-2016": {"SENATOR": 176, "DEPUTAT": 412},
                  "2016-2020": {"SENATOR": 136, "DEPUTAT": 329}}

# NB: the information for party sizes after elections and government coalition partners come from Wikipedia
# NB: I count Forţa Civică and PNTCD in 2012 elections as part of PD-L, but I count UNPR separately

# party size cutoffs for senate: small <=15, 16 <= midling <= 30, 31 <= large
party_size_after_election_senate = {2000: {"UDMR": 12, "PSD": 61, "PNL": 13, "PDL": 13, "PRM": 37, "PC": 4},
                                    2004: {"UDMR": 10, "PSD": 46, "PNL": 28, "PDL": 21, "PRM": 21, "PC": 11},
                                    2008: {"UDMR": 9, "PSD": 48, "PNL": 28, "PDL": 51, "PC": 1},
                                    2012: {"UDMR": 9, "PSD": 58, "PNL": 51, "PDL": 24, "UNPR": 5, "PC": 8, "PP DD": 21},
                                    2016: {"UDMR": 9, "PSD": 67, "PNL": 30, "PMP": 8, "USR": 13, "ALDE": 9}}

# party size cutoffs for CDEP: small <=31, 32 <= midling <= 60, 61 <= large
party_size_after_election_cdep = {2000: {"UDMR": 27, "PSD": 155, "PNL": 30, "PDL": 31, "PRM": 84, "PC": 6},
                                  2004: {"UDMR": 22, "PSD": 113, "PNL": 64, "PDL": 48, "PRM": 48, "PC": 19},
                                  2008: {"UDMR": 22, "PSD": 110, "PNL": 65, "PDL": 115, "PC": 4},
                                  2012: {"UDMR": 18, "PSD": 149, "PNL": 101, "PDL": 56, "UNPR": 10, "PC": 13,
                                         "PP DD": 47},
                                  2016: {"UDMR": 21, "PSD": 154, "PNL": 69, "PMP": 18, "USR": 30, "ALDE": 20}}

# I do not distinguish parliamentary party size by chamber because there is little inter-chamber variance, and that
# because the electoral system for the two chambers is identical, except senators represent roughly double the number
# of people that deputies do. NB: the Minorities group is only in the lower house and always has 15-18 people.
party_size_cat = {"2000-2004": {"UDMR": "small", "PSD": "large", "PNL": "small", "PDL": "small",
                                "PRM": "large", "PC": "small", "MIN": "small"},
                  "2004-2008": {"UDMR": "small", "PSD": "large", "PNL": "midling", "PDL": "midling",
                                "PRM": "midling", "PC": "small", "MIN": "small"},
                  "2008-2012": {"UDMR": "small", "PSD": "large", "PNL": "midling", "PDL": "large",
                                "PC": "small", "MIN": "small"},
                  "2012-2016": {"UDMR": "small", "PSD": "large", "PNL": "large", "PDL": "midling",
                                "PC": "small", "UNPR": "small", "PP DD": "midling", "MIN": "small"},
                  "2016-2020": {"UDMR": "small", "PSD": "large", "PNL": "midling", "PMP": "small",
                                "ALDE": "small", "USR": "small", "MIN": "small"}
                  }

# here I write down the yearly PPG size AT THE BEGINNING OF THE YEAR. Note that a size of zero means that the PPG
# has stopped existing, or hasn't yet been founded
ppg_size = {2009: {"SENAT": {"PSD": 48, "PNL": 28, "PDL": 51, "UDMR": 9, "UNPR": 0},
                   "CDEP": {"PSD": 110, "PNL": 65, "PDL": 115, "UDMR": 22, "UNPR": 0, "MIN": 16}},
            2010: {"SENAT": {"PSD": 44, "PNL": 25, "PDL": 50, "UDMR": 9, "UNPR": 6},
                   "CDEP": {"PSD": 103, "PNL": 54, "PDL": 115, "UDMR": 22, "UNPR": 7, "MIN": 16}},
            2011: {"SENAT": {"PSD": 44, "PNL": 22, "PDL": 48, "UDMR": 9, "UNPR": 11},
                   "CDEP": {"PSD": 91, "PNL": 53, "PDL": 124, "UDMR": 21, "UNPR": 21, "MIN": 16}},
            2012: {"SENAT": {"PSD": 39, "PNL": 25, "PDL": 45, "UDMR": 8, "UNPR": 14},
                   "CDEP": {"PSD": 87, "PNL": 59, "PDL": 121, "UDMR": 20, "UNPR": 25, "MIN": 15}},

            2013: {"SENAT": {"PSD": 58, "PNL": 51, "PDL": 24, "UDMR": 9, "PP DD": 21, "PC": 8},
                   "CDEP": {"PSD": 149, "PNL": 101, "PDL": 56, "UDMR": 18, "PP DD": 47, "MIN": 18, "PC": 13}},
            2014: {"SENAT": {"PSD": 68, "PNL": 51, "PDL": 23, "UDMR": 8, "PP DD": 8, "PC": 9},
                   "CDEP": {"PSD": 157, "PNL": 101, "PDL": 46, "UDMR": 18, "PP DD": 25, "MIN": 18, "PC": 18}},
            2015: {"SENAT": {"PSD": 74, "PNL": 40, "PDL": 20, "UDMR": 8, "PP DD": 0, "PC": 16},
                   "CDEP": {"PSD": 173, "PNL": 73, "PDL": 33, "UDMR": 18, "PP DD": 11, "MIN": 17, "PC": 35}},
            2016: {"SENAT": {"PSD": 76, "PNL": 59, "PDL": 0, "UDMR": 8, "PP DD": 0, "PC": 14},
                   "CDEP": {"PSD": 164, "PNL": 118, "PDL": 0, "UDMR": 17, "PP DD": 0, "MIN": 17, "PC": 26}},

            2017: {"SENAT": {"PSD": 67, "PNL": 30, "UDMR": 9, "ALDE": 9, "PMP": 8, "USR": 13},
                   "CDEP": {"PSD": 154, "PNL": 69, "UDMR": 21, "ALDE": 20, "PMP": 18, "USR": 30,
                            "PRO": "", "MIN": 17}},
            2018: {"SENAT": {"PSD": 67, "PNL": 29, "UDMR": 9, "ALDE": 9, "PMP": 8, "USR": 13},
                   "CDEP": {"PSD": 152, "PNL": 67, "UDMR": 21, "ALDE": 16, "PMP": 16, "USR": 29,
                            "PRO": "", "MIN": 17}},
            2019: {"SENAT": {"PSD": 69, "PNL": 25, "UDMR": 8, "ALDE": 13, "PMP": 0, "USR": 13},
                   "CDEP": {"PSD": 145, "PNL": 67, "UDMR": 21, "ALDE": 21, "PMP": 12, "USR": 28,
                            "PRO": "", "MIN": 17}},
            2020: {"SENAT": {"PSD": 69, "PNL": 27, "UDMR": 8, "ALDE": 0, "PMP": 0, "USR": 13},
                   "CDEP": {"PSD": 127, "PNL": 71, "UDMR": 21, "ALDE": 23, "PMP": 13, "USR": 28,
                            "PRO": 28, "MIN": 17}},
            }

# since this paper focuses strictly on strategic party switches, we want to avoid "forced" switches caused by
# the dissolution of PPGs, either because they no longer have the minimum number of members or because they merged
# with another party. The latter situation is already handled upstream to some extent but I'll include all cases here
# for completeness
# NB: PSDR and PSM in the lower house merged in September of 1996
# NB: for the 2004-2008 legislature the PNL and PD sat together as the D.A. alliance group only in the senate, until
#     they broke up in 2007. Since they were voted by their separate partis and then simply became party-based PPGs
#     (not the alliance) I do not count it as a PPG break-up
ppg_end_dates = {"1990-1992": {"SENAT": {}, "CDEP": {}},
                 "1992-1996": {"SENAT": {"OCL": "01.09.1993"}, "CDEP": {"PSDR": "02.09.1996",
                                                                        "PSM": "10.09.1996",
                                                                        "PAC": "29.06.1993"}},
                 "1996-2000": {"SENAT": {}, "CDEP": {"PSDR": "25.03.1999"}},
                 "2000-2004": {"SENAT": {}, "CDEP": {}},
                 "2004-2008": {"SENAT": {}, "CDEP": {}},
                 "2008-2012": {"SENAT": {}, "CDEP": {}},
                 "2012-2016": {"SENAT": {"PDL": "02.02.2015", "PP DD": "03.02.2014", "UNPR": "28.06.2016"},
                               "CDEP": {"PP DD": "22.12.2015", "PDL": "02.02.2015"}},
                 "2016-2020": {"SENAT": {"ALDE": "11.09.2019", "PMP": "04.06.2018"}, "CDEP": {"ALDE": "10.02.2020"}}}

# often legislators give up their seats in the run-up to legislative and/or local elections, to better contest these.
# Local elections take place several months before legislative ones, in the same year, so if you were to resign to prep
# for local elections you would do this around the beginning of summer legislative recess, which usually begins in June.
# In other words, all people leaving the legislature before up to May of election year are probably doing so for
# non-standard reasons
leave_early_cutoff = {"2004-05", "2008-05", "2012-05", "2016-05", "2020-05"}

# 1 = former Hapsburg possessions, i.e. Ardeal, Banat, Bucovina, Crişana, Maramureş; 2 = Moldova,
# 3 = Old Kingdom/Wallachia, i.e. Dobrogea, Muntenia, Oltenia; 4 = MINORTIES, 5 = DISAPORA
historical_regions_dict = {"ALBA": 1, "ARAD": 1, "BIHOR": 1, "BRAŞOV": 1, "BISTRIŢA-NĂSĂUD": 1, "CARAŞ-SEVERIN": 1,
                           "CLUJ": 1, "COVASNA": 1, "HARGHITA": 1, "HUNEDOARA": 1, "MARAMUREŞ": 1, "MUREŞ": 1,
                           "SATU MARE": 1, "SĂLAJ": 1, "SIBIU": 1, "SUCEAVA": 1, "TIMIŞ": 1,

                           "BACĂU": 2, "BOTOŞANI": 2, "GALAŢI": 2, "IAŞI": 2, "NEAMŢ": 2, "VASLUI": 2, "VRANCEA": 2,

                           "ARGEŞ": 3, "BRĂILA": 3, "BUCUREŞTI": 3, "BUZĂU": 3, "CĂLĂRAŞI": 3, "CONSTANŢA": 3,
                           "DÂMBOVIŢA": 3, "DOLJ": 3, "GIURGIU": 3, "GORJ": 3, "IALOMIŢA": 3, "ILFOV": 3,
                           "MEHEDINŢI": 3, "OLT": 3, "PRAHOVA": 3, "TELEORMAN": 3, "TULCEA": 3, "VÂLCEA": 3,

                           "MINORITĂŢI": 4,

                           "DIASPORA": 5
                           }
