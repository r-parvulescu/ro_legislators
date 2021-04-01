"""
NB: not enough variance to see if timing of loss of parliamentary caucus group affects timing of party switch
    --> PUR-SL 2000-2004 always caucased with PSD, never had a PPG to lose
    --> PC (former PUR-SL) in 2008-2012 caucused first with PSD then with PNL, so didn't actually lose a caucus
    --> PC in 2012-2016 caucused on its own then merged with PNL splinter to form ALDE caucus in CDEP,
        always had its caucus in senate; either way, never lost a caucus
    --> PP-DD lost its caucuses in summer 2015: in Senat (July) and CDEP (August). Party leader Dan Diaconescu had
        been sent to jail several months prior, in March 2015
    --> PMP lost Senate caucus in June 2018, but kepy CDEP caucus
    --> ALDE lost both CDEP and Senat caucuses in September 2019

NB: the lists of gov't coaltion partners only include parties that were popularly elected. UNPR, for instance, was an
intra-parliamentary party for 2008-2012 formed by deputies leaving their original parties, so even though it was a
junionr partner in Ponta 1, it's not listed there as such. Conceptually, this is because we measure time to first
party defection, and since everyone in UNPR must have defected to join that party in the 2008-2012 legislature, can be
be no UNPR observations at all for that period.

NB: I end up ignoring confidence and supply agreements because it's very difficult to get hard information on this:
such agreements are usually informal, it's very rare that party leaders publicly agree to such things

NB: the information for party sizes after elections and government coalition partners come from Wikipedia

NB: whenever I refer to party I really mean "parliamentary party group"

NB: ideally would do this at level of half-year parliamentary "session", substantively because one can switch party
twice per session and
because PPG dynamics (dissolution, joining or leaving coalition) are more fine-grained than the year

"""

# NB: I map PNTCD and FC to PDL because they were tiny and jointly on the list with PDL for only one post-2000
# legislature, then went back into the unknown. unlike UNPR and PC, who were there for longer and actually mattered as
# independent PPGs
party_name_dict = {"Partidul Democraţiei Sociale din România": "Partidul Social Democrat",
                   "Partidul Democrat": "Partidul Democrat Liberal",
                   "Partidul Social Umanist din România (social liberal)": "Partidul Conservator",
                   "Partidul Naţional Ţărănesc Creştin Democrat": "Partidul Democrat Liberal",
                   "Forţa Civică": "Partidul Democrat Liberal",
                   "minorities": "Grupul Minorităţilor Naţionale"}

ethnic_parties = {"MIN", "UDMR"}

# hard to say if PRM post-2000 was "Vadim's party" in the same sense that ALDE was Tăriceanu's party: my feeling is
# "no", PRM was less tied to its founder, but this is debatable
personality_parties_names = {"Partidul Mişcarea Populară", "Partidul Poporului - Dan Diaconescu",
                             "Alianţa Liberalior şi Democraţilor", "Partidul Conservator"}

personality_parties = {"PMP", "PP DD", "ALDE", "PC"}

# NB: I cound Forţa Civică and PNŢCD in 2012 elections as part of PD-L, but I count UNPR separately
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
party_size = {"2000-2004": {"UDMR": "small", "PSD": "large", "PNL": "small", "PDL": "small",
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

gov_coalition_senior_partner = {"2000-2004": {"UDMR": '',
                                              "PSD": '28.12.2000-21.12.2004',
                                              "PNL": '',
                                              "PDL": '', "PRM": '', "PC": ''},
                                "2004-2008": {"UDMR": '', "PSD": '',
                                              "PNL": ('29.12.2004-05.04.2007', '05.04.2007-22.12.2008'),
                                              "PDL": '29.12.2004-05.04.2007',
                                              "PRM": '', "PC": ''},
                                "2008-2012": {"UDMR": '',
                                              "PSD": ('22.12.2008-23.12.2009', '07.05.2012-21.12.2012'),
                                              "PNL": '07.05.2012-21.12.2012',
                                              "PDL": ('22.12.2008-23.12.2009', '23.12.2009-06.02.2012',
                                                      '09.02.2012-07.05.2012'),
                                              "PC": ''},
                                "2012-2016": {"UDMR": '',
                                              "PSD": ('21.12.2012-05.03.2014', '05.03.2014-17.12.2014',
                                                      '17.12.2014-4.11.2015'),
                                              "PNL": '21.12.2012-05.03.2014',
                                              "PDL": '', "UNPR": '',
                                              "PC": '',
                                              "PP-DD": ''},
                                "2016-2020": {"UDMR": '',
                                              "PSD": ('04.01.2017-29.06.2017', '29.06.2017-29.01.2018',
                                                      '29.01.2018-04.11.2019'),
                                              "PNL": ('04.11.2019-14.04.2020', '14.04.2020-prezent'),
                                              "PMP": '', "USR": '', "ALDE": ''}}

gov_coalition_junior_partner = {"2000-2004": {"UDMR": '', "PSD": '', "PNL": '',
                                              "PDL": '', "PRM": '',
                                              "PC": '28.12.2000-21.12.2004'},
                                "2004-2008": {"UDMR": ('29.12.2004-05.04.2007', '05.04.2007-22.12.2008'),
                                              "PSD": '', "PNL": '',
                                              "PDL": '', "PRM": '',
                                              "PC": '29.12.2004-05.04.2007'},
                                "2008-2012": {"UDMR": ('23.12.2009-06.02.2012', '09.02.2012-07.05.2012'),
                                              "PSD": '', "PNL": '',
                                              "PDL": '',
                                              "PC": ('22.12.2008-23.12.2009', '07.05.2012-21.12.2012')},
                                "2012-2016": {"UDMR": '05.03.2014-17.12.2014',
                                              "PSD": '', "PNL": '',
                                              "PDL": '',
                                              "UNPR": ('21.12.2012-05.03.2014', '05.03.2014-17.12.2014',
                                                       '17.12.2014-4.11.2015'),
                                              "PC": ('21.12.2012-05.03.2014', '05.03.2014-17.12.2014',
                                                     '17.12.2014-4.11.2015'),
                                              "PP-DD": ''},
                                "2016-2020": {"UDMR": '', "PSD": '', "PNL": '',
                                              "PMP": '', "USR": '',
                                              "ALDE": ('04.01.2017-29.06.2017', '29.06.2017-29.01.2018',
                                                       '29.01.2018-04.11.2019')}}

# the minorities "party" is not really a party but a collection of representatives of organisations of different
# "national minorities" who caucus together for convenience but whose members typically vote in radically different
# ways, a situation that is acknowledged and accepted; they often support the government (whoever that may be) but you
# need to negotiate with every one of them for each thing. I therefore put them as perpetual "opposition", but it's an
# edge case
govt_parties = {2001: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "opposition",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2002: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "opposition",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2003: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "opposition",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2004: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "opposition",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2005: {"UDMR": "junior", "PSD": "opposition", "PNL": "senior", "PDL": "senior",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2006: {"UDMR": "junior", "PSD": "opposition", "PNL": "senior", "PDL": "senior",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2007: {"UDMR": "junior", "PSD": "opposition", "PNL": "senior", "PDL": "senior",
                       "PRM": "opposition", "PC": "junior", "MIN": "opposition"},
                2008: {"UDMR": "junior", "PSD": "opposition", "PNL": "senior", "PDL": "opposition",
                       "PRM": "opposition", "PC": "opposition", "MIN": "opposition"},
                2009: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "senior",
                       "PC": "junior", "MIN": "opposition"},
                2010: {"UDMR": "junior", "PSD": "opposition", "PNL": "opposition", "PDL": "senior",
                       "PC": "opposition", "MIN": "opposition"},
                2011: {"UDMR": "junior", "PSD": "opposition", "PNL": "opposition", "PDL": "senior",
                       "PC": "opposition", "MIN": "opposition"},
                2012: {"UDMR": "junior", "PSD": "senior", "PNL": "senior", "PDL": "senior",
                       "PC": "junior", "MIN": "opposition"},
                2013: {"UDMR": "opposition", "PSD": "senior", "PNL": "senior", "PDL": "opposition",
                       "PC": "junior", "UNPR": "junior", "PP DD": "opposition", "MIN": "opposition"},
                2014: {"UDMR": "junior", "PSD": "senior", "PNL": "senior", "PDL": "opposition",
                       "PC": "junior", "UNPR": "junior", "PP DD": "opposition", "MIN": "opposition"},
                2015: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PDL": "opposition",
                       "PC": "junior", "UNPR": "junior", "PP DD": "opposition", "MIN": "opposition"},
                2016: {"UDMR": "opposition", "PSD": "opposition", "PNL": "opposition", "PDL": "opposition",
                       "PC": "opposition", "UNPR": "opposition", "PP DD": "opposition", "MIN": "opposition"},
                2017: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PMP": "opposition",
                       "ALDE": "junior", "USR": "opposition", "MIN": "opposition"},
                2018: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PMP": "opposition",
                       "ALDE": "junior", "USR": "opposition", "MIN": "opposition"},
                2019: {"UDMR": "opposition", "PSD": "senior", "PNL": "opposition", "PMP": "opposition",
                       "ALDE": "junior", "USR": "opposition", "MIN": "opposition"},
                2020: {"UDMR": "opposition", "PSD": "opposition", "PNL": "senior", "PMP": "opposition",
                       "ALDE": "opposition", "USR": "opposition", "MIN": "opposition"},
                }

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

# "PD" rebranded to "PDL" in 2007, "PUR SL" changed its name to "PC" in 2005
party_name_changes = {"PD": "PDL", "PUR SL": "PC", "PDSR": "PSD", "PNTCD": "PDL", "FC": "PDL"}

election_years = {2004, 2008, 2012, 2016, 2020}

leg_chamb_size = {"2000-2004": {"SENATOR": 140, "DEPUTAT": 345},
                  "2004-2008": {"SENATOR": 137, "DEPUTAT": 332},
                  "2008-2012": {"SENATOR": 137, "DEPUTAT": 334},
                  "2012-2016": {"SENATOR": 176, "DEPUTAT": 412},
                  "2016-2020": {"SENATOR": 136, "DEPUTAT": 329}}

# TODO also get a list of parliamentarians convicted without possibility of appeal

# I marked Boc as being head of PDL 2005-2012, even though one could argue that the actual boss was Basescu

# on the books Daniel Constantin became the leader of the PC in 2010, but I don't buy it: Dan Voiculescu was the big
# boss until he went to jail, so I count THAT as the real leadership turnover

# Dan Diaconescu was never officially the head of PP-DD, but again, he was the real leader

# the PMP boss has always been Traian Basescu: Eugen Tomac and Elena Udrea were figureheads

# for all of its existence from 2015 to 2020 (when it fused with Ponta's PRO) ALDE only had one head, Tariceanu
party_leader_changes = {2001: {"PNL", "PDL"}, 2002: {"PNL"}, 2003: {}, 2004: {"PNL"}, 2005: {"PSD", "PDL"}, 2006: {},
                        2007: {}, 2008: {},
                        2009: {"PNL"}, 2010: {"PSD"}, 2011: {"UDMR"}, 2012: {"PDL"}, 2013: {}, 2014: {"PNL", "PC"},
                        2015: {"PSD", "PP DD"}, 2016: {"PNL", "UNPR"},
                        2017: {"PNL", "USR"}, 2018: {}, 2019: {"PSD"}, 2020: {}}

# often legislators give up their seats in the run-up to legislative and/or local elections, to better contest these.
# Local elections take place several months before legislative ones, in the same year, so if you were to resign to prep
# for local elections you would do this around the beginning of summer legislative recess, which usually begins in June.
# In other words, all people leaving the legislature before up to May of election year are probably doing so for
# non-standard reasons
leave_early_cutoff = {"2004-05", "2008-05", "2012-05", "2016-05", "2020-05"}