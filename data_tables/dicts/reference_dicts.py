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

# ALL INFO FROM WIKIPEDIA
# I look at post-2008 espeically since I study the 2008, 2012, and 2020 legislatures
# NB: Alina Gorghiu was co-leader with Vasile Blaga for most of her time as president of the PNL. Since their mandates
#     overlap almost entirely the fact that there were two of them doesn't really matter
# NB: Daniel Constantin was co-president of ALDE after Tariceanu's PNL breakaway faction fused with the PC to make ALDE,
#     but Constantin left in 2017, with Tariceanu remaining sole leader. I therefore consider 2017 a leadership turnover
#     year for ALDE.
# NB: the UNPR effectively went on ice from 2016 to 2018, until it was revamped by Oprea, who had founded it in the
#     first place
# NB: PP DD was absorbed into UNPR in June of 2015
# NB: on the 17th of August 2020 USR and the extraparliamentary party PLUS officially fused, with PLUS president D
#     Dacian Ciolos becoming co-president alongside Barna. I have not counted this as a change in leadership because
#     it did not involve Barna leaving, and it involved an extraparliamentary party.
party_leaders = {"UDMR": {"Marko Bela": "1993-02.2011", "Kelemen Hunor": "02.2011-prezent"},
                 "PDL": {"Emil Boc": "01.01.2005-30.06.2012", "Vasile Blaga": "30.06.2012-17.12.2014"},
                 "PNL": {"Călin Popescu Tăriceanu": "02.10.2004-20.03.2009", "Crin Antonescu": "20.03.2009-31.05.2014",
                         "Klaus Iohannis": "28.06.2014-18.12.2014", "Alina Gorghiu": "18.12.2014-12.12.2016",
                         "Raluca Turcan (acting)": "13.12.2016-17.06.2017", "Ludovic Orban": "17.06.2017-prezent"},
                 "PSD": {"Adrian Năstase": "16.01.2001-21.01.2005", "Mircea Geonă": "21.01.2005-21.02.2010",
                         "Victor Ponta": "21.02.2010-12.07.2015", "Liviu Dragnea": "22.07.2015-27.05.2019",
                         "Viorica Dăncilă (acting)": "27.05.2019-26.11.2019", "Marcel Ciolacu": "29.11.2019-prezent"},
                 "PC": {"Dan Voiculescu": "18.12.1991-02.2010", "Daniel Constantin": "02.2010-19.06.2015"},
                 "ALDE": {"Daniel Constantin": "19.06.2015-04.2017", "Călin Popescu Tăriceanu": "04.2017-19.10.2020"},
                 "PRO": {"Victor Ponta": "03.09.2017-prezent"},
                 "UNPR": {"Marian Sârbu": "05.2010-28.05.2012", "Gabriel Oprea": ("28.05-2012-03.2016",
                                                                                  "06.2018-prezent")},
                 "PP DD": {"Simona Man": "29.05.2012-29.06.2015"},
                 "PRM": {"Vadim Tudor": ("20.06.1991-2005", "2005-2015"), "Corneliu Ciontu": "2005"},
                 "USR": {"Nicuşor Dan": "27.12.2015-1.07.2017", "Dan Barna": "28.10.2017-prezent"},
                 "PMP": {"Eugen Tomac": ("23.06.2013-08.06.2014", "30.01.2015-27.03.2016", "16.06.2018-09.12.2020"),
                         "Elena Udrea": "08.06.2014-30.01.2015", "Traian Băsescu": "27.03.2016-16.06.2018"}}

# NB: I marked Boc as being head of PDL 2005-2012, even though one could argue that the actual boss was Basescu
# NB: on the books Daniel Constantin became the leader of the PC in 2010, but Dan Voiculescu was the big boss until he
#     went to jail (Constantin actually had a personal 200,000 unto Voiculescu), so I count Voiculescu's jailing as the
#     real leadership turnover
# NB: Dan Diaconescu was never officially the head of PP-DD, but again, he was the real leader, so I count his jailing
#     as the real leadership turnover
# NB: Gabriel Oprea was the founder and real shaker of the UNPR so I don't count the turnover from Marian Sârbu to Oprea
#     as a real leadership turnover
# NB: the real PMP boss has always been Traian Basescu: Eugen Tomac and Elena Udrea were always captains; consequently,
#     I mark no leadership turnover in the PMP
# NB: PP DD is marked as a leadership change in 2015 because Dan Diaconescu was sent to jail. Likewise the leadership
#     change in PC in 2014 is for Voiculescu being sent to jail, and in UNPR in 2016 it's for Oprea resigning in order
#     to stand trial in a corruption case.
party_leader_changes = {2001: {"PNL", "PDL"}, 2002: {"PNL"}, 2003: {}, 2004: {"PNL"}, 2005: {"PSD", "PDL", "PRM"},
                        2006: {},
                        2007: {}, 2008: {},
                        2009: {"PNL"}, 2010: {"PSD"}, 2011: {"UDMR"}, 2012: {"PDL"}, 2013: {},
                        2014: {"PNL", "PC"},
                        2015: {"PSD", "PP DD"}, 2016: {"PNL", "UNPR"},
                        2017: {"PNL", "USR", "ALDE"}, 2018: {}, 2019: {"PSD"}, 2020: {}}

# as a robustness check, I don't use my more in-depth knowledge above and simply count formal leadership changes
party_leader_change_by_the_books = {2001: {"PNL", "PDL"}, 2002: {"PNL"}, 2003: {}, 2004: {"PNL"},
                                    2005: {"PSD", "PDL", "PRM"}, 2006: {},
                                    2007: {}, 2008: {},
                                    2009: {"PNL"}, 2010: {"PSD", "PC"}, 2011: {"UDMR"}, 2012: {"PDL", "UNPR"}, 2013: {},
                                    2014: {"PNL", "PMP"},
                                    2015: {"PSD", "PMP"}, 2016: {"PNL", "UNPR", "PMP"},
                                    2017: {"PNL", "USR", "ALDE"}, 2018: {"PMP"}, 2019: {"PSD"}, 2020: {}}

# often legislators give up their seats in the run-up to legislative and/or local elections, to better contest these.
# Local elections take place several months before legislative ones, in the same year, so if you were to resign to prep
# for local elections you would do this around the beginning of summer legislative recess, which usually begins in June.
# In other words, all people leaving the legislature before up to May of election year are probably doing so for
# non-standard reasons
leave_early_cutoff = {"2004-05", "2008-05", "2012-05", "2016-05", "2020-05"}

# for each constituency, typically counties, we record the party affiliation of the head of the county council (i.e.
# the county-level executive) and of the mayor of the county seat. Together these show the political orientation of the
# county, which is useful for seeing if legislators switch parties when doing so might make them an opporition figure
# vis-a-vis the local executive majority, which often controls the pork.
# NB: since local elections occur several months before legislative, and since changes of majorities are impossible
#     among the mayors (and after 2016 of county presidents) and otherwise extremely rare among the county councils,
#     I treat the electoral political affiliations at county and sub-county level as fixed between legislative votes.
#     Local leaders DO change colours, but this tends to happen around election time.
# NB: for legislators representing the extra-territorial diaspora or the nation-wide ethnic constituencies for reserved
#     minority seats I simply mark the CC Pres and CS Mayor as "IND", i.e. independent. A bit of a fudge, but there you
#     go.
# NB: for Sibiu county and city I treat the FDGR as PNL becausse they are practically always in coalition and have close
#     ideological and personnel ties
# NB: for Timişoara in 2008 I treat the mayor as PNL since it was an alliance largely dominated by the PNL (plus FDGR
#     and PNŢCD) which took the mayorality
# NB: for Bucharest I count the general mayor as county president AND mayor, ignoring the mayors of the buroughs. I
#     also take "independent" at face value in Bucharest, though usually this means "coalition against PSD"
# NB: Because the county seat for Ilfov is Bucharest, I use the mayor of Bucharest as the mayor of
# NB: the elections were won by a grand coalition that soon fell apart. Nonetheless individual offices were won by
#     politicians with specific, non-coalition affiliation. It is these affiliations which I use for that period.
# NB: practically all PDL mayors (notably Emil Boc from Cluj) went to the PNL in 2014 when those parties fused.
# NB: tough call on the mayor of Deva's actual affiliation (PC or PNL) in 2012, I went with PNL since we ran under their
#     banner the next time around.
# NB: Cătălin Cherecheş of Baia Mara switched parties A LOT before and after 2012; I mark him as PNL for 2012 and
#     in 2016 as UNPR-ish while actually being in jail (lol). I mark that win for an independent.
# NB: In 2016 Mircia Muntean won the Deva mayorship on the back of a PSD splinter group that later chose to abolish
#     itself. I count him as an independent.
# NB: Mircia Gutau is the long-standing mayor of Ramnicu Valcea and he keeps flipping parties to win, In 2016 I mark him
#     as independent.
county_polit_dict = {"2008-2012": {"ALBA": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "ARAD": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "BIHOR": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "BRAŞOV": {"CC Pres": "PNL", "CS Mayor": "PDL"},
                                   "BISTRIŢA-NĂSĂUD": {"CC Pres": "PDL", "CS Mayor": "PSD"},
                                   "CARAŞ-SEVERIN": {"CC Pres": "PDL", "CS Mayor": "IND"},
                                   "CLUJ": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "COVASNA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HARGHITA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HUNEDOARA": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "MARAMUREŞ": {"CC Pres": "PDL", "CS Mayor": "PNL"},
                                   "MUREŞ": {"CC Pres": "UDMR", "CS Mayor": "PDL"},
                                   "SATU MARE": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "SĂLAJ": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "SIBIU": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "SUCEAVA": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "TIMIŞ": {"CC Pres": "PDL", "CS Mayor": "PNL"},
                                   "BACĂU": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "BOTOŞANI": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "GALAŢI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "IAŞI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "NEAMŢ": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "VASLUI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "VRANCEA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ARGEŞ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BRĂILA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BUCUREŞTI": {"CC Pres": "IND", "CS Mayor": "IND"},
                                   "BUZĂU": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "CĂLĂRAŞI": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "CONSTANŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "DÂMBOVIŢA": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "DOLJ": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "GIURGIU": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "GORJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "IALOMIŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ILFOV": {"CC Pres": "PDL", "CS Mayor": "IND"},
                                   "MEHEDINŢI": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "OLT": {"CC Pres": "PDL", "CS Mayor": "PSD"},
                                   "PRAHOVA": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "TELEORMAN": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "TULCEA": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "VÂLCEA": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "MINORITĂŢI": {"CC Pres": "IND", "CS Mayor": "IND"},
                                   "DIASPORA": {"CC Pres": "IND", "CS Mayor": "IND"}
                                   },
                     "2012-2016": {"ALBA": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "ARAD": {"CC Pres": "PDL", "CS Mayor": "PDL"},
                                   "BIHOR": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "BRAŞOV": {"CC Pres": "PNL", "CS Mayor": "PDL"},
                                   "BISTRIŢA-NĂSĂUD": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "CARAŞ-SEVERIN": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "CLUJ": {"CC Pres": "PNL", "CS Mayor": "PDL"},
                                   "COVASNA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HARGHITA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HUNEDOARA": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "MARAMUREŞ": {"CC Pres": "PC", "CS Mayor": "PNL"},
                                   "MUREŞ": {"CC Pres": "PNL", "CS Mayor": "PDL"},
                                   "SATU MARE": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "SĂLAJ": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "SIBIU": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "SUCEAVA": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "TIMIŞ": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "BACĂU": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "BOTOŞANI": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "GALAŢI": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "IAŞI": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "NEAMŢ": {"CC Pres": "UNPR", "CS Mayor": "PDL"},
                                   "VASLUI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "VRANCEA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ARGEŞ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BRĂILA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BUCUREŞTI": {"CC Pres": "IND", "CS Mayor": "IND"},
                                   "BUZĂU": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "CĂLĂRAŞI": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "CONSTANŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "DÂMBOVIŢA": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "DOLJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "GIURGIU": {"CC Pres": "PNL", "CS Mayor": "IND"},
                                   "GORJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "IALOMIŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ILFOV": {"CC Pres": "PNL", "CS Mayor": "IND"},
                                   "MEHEDINŢI": {"CC Pres": "PSD", "CS Mayor": "PDL"},
                                   "OLT": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "PRAHOVA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "TELEORMAN": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "TULCEA": {"CC Pres": "PNL", "CS Mayor": "PDL"},
                                   "VÂLCEA": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "MINORITĂŢI": {"CC Pres": "IND", "CS Mayor": "IND"},
                                   "DIASPORA": {"CC Pres": "IND", "CS Mayor": "IND"}
                                   },
                     "2016-2020": {"ALBA": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "ARAD": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "BIHOR": {"CC Pres": "UDMR", "CS Mayor": "PNL"},
                                   "BRAŞOV": {"CC Pres": "", "CS Mayor": "IND"},
                                   "BISTRIŢA-NĂSĂUD": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "CARAŞ-SEVERIN": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "CLUJ": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "COVASNA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HARGHITA": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "HUNEDOARA": {"CC Pres": "PSD", "CS Mayor": "IND"},
                                   "MARAMUREŞ": {"CC Pres": "PSD", "CS Mayor": "IND"},
                                   "MUREŞ": {"CC Pres": "UDMR", "CS Mayor": "PNL"},
                                   "SATU MARE": {"CC Pres": "UDMR", "CS Mayor": "UDMR"},
                                   "SĂLAJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "SIBIU": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "SUCEAVA": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "TIMIŞ": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "BACĂU": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BOTOŞANI": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "GALAŢI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "IAŞI": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "NEAMŢ": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "VASLUI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "VRANCEA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ARGEŞ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BRĂILA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BUCUREŞTI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "BUZĂU": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "CĂLĂRAŞI": {"CC Pres": "PNL", "CS Mayor": "PNL"},
                                   "CONSTANŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "DÂMBOVIŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "DOLJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "GIURGIU": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "GORJ": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "IALOMIŢA": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "ILFOV": {"CC Pres": "PNL", "CS Mayor": "PSD"},
                                   "MEHEDINŢI": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "OLT": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "PRAHOVA": {"CC Pres": "PSD", "CS Mayor": "PNL"},
                                   "TELEORMAN": {"CC Pres": "PSD", "CS Mayor": "PSD"},
                                   "TULCEA": {"CC Pres": "PSD", "CS Mayor": "IND"},
                                   "VÂLCEA": {"CC Pres": "PSD", "CS Mayor": "IND"},
                                   "MINORITĂŢI": {"CC Pres": "IND", "CS Mayor": "IND"},
                                   "DIASPORA": {"CC Pres": "IND", "CS Mayor": "IND"}
                                   }
                     }
