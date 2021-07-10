"""Dictionaries pertaining to party leaders."""

# ALL INFO FROM WIKIPEDIA
# GENERAL NOTE: these are leadership changes of the party writ large, not just the parliamentary party group
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
party_leaders = {"PAR": {"Victor Surdu": "29.01.1990-28.06,1997", "Mihai Berca": "28.06.1997-14.03.1998"},
                 "PAC": {"Nicolae Manolescu": "01.01.1991-01.01.1998"}, "PSM": {"Ilie Verdeţ": "16.11.1990-20.03.2001"},
                 "PER": {"Adrian Manolache": "16.01.1990-20.04.1990", "Otto Ernest Weber": "20.04.1990-21.06.2001"},
                 "PSDR": {"Sergiu Cunescu": "16.01.1990-01.01.1999", "Alexandru Athanasiu": "01.01.1999-16.01.2001"},
                 "PNTŢCD": {"Corneliu Coposu": "06.01.1990-11.11.1995", "Ion Diaconescu": "11.11.1995-30.12.2000"},
                 "PUNR": {"Gheorghe Funar": "17.10.1992-22.03.1997", "Valeriu Tabără": "22.03.1997-11.05.2002",
                          "Mircea Chelaru": "11.05.2002-19.01.2006"},
                 "UDMR": {"Marko Bela": "1993-02.2011", "Kelemen Hunor": "02.2011-prezent"},
                 "PDL": {"Petre Roman": "28.05.1993-19.05.2001", "Traian Băsescu": "19.05.2001-18.12.2004",
                         "Emil Boc": "18.12.2004-30.06.2012", "Vasile Blaga": "30.06.2012-17.12.2014"},
                 "PNL": {"Mircea Ionescu-Quintus": "28.02.1993-18.02.2001", "Valeriu Stoica": "18.02.2001-24.08.2002",
                         "Theodor Stolojan": "24.08.2002-02.10.2004",
                         "Călin Popescu Tăriceanu": "02.10.2004-20.03.2009", "Crin Antonescu": "20.03.2009-31.05.2014",
                         "Klaus Iohannis": "28.06.2014-18.12.2014", "Alina Gorghiu": "18.12.2014-12.12.2016",
                         "Raluca Turcan (acting)": "13.12.2016-17.06.2017", "Ludovic Orban": "17.06.2017-prezent"},
                 "PSD": {"Oliviu Gherman": "10.07.1993-01.01.1997", "Ion Iliescu": "01.01.1997-20.12.2000",
                         "Adrian Năstase": "16.01.2001-21.01.2005", "Mircea Geonă": "21.01.2005-21.02.2010",
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
# NB: I count the PSD transfer of power from Iliescu to Năstase as having taken part in 2001
party_leader_changes = {1990: {"PER"}, 1991: {}, 1992: {}, 1993: {"UDMR"}, 1994: {}, 1995: {"PNTCD"}, 1996: {},
                        1997: {"PSD"}, 1998: {}, 1999: {"PSDR"}, 2000: {}, 2001: {"PNL", "PDL", "PSD"},
                        2002: {"PNL"}, 2003: {}, 2004: {"PNL"}, 2005: {"PSD", "PDL", "PRM"}, 2006: {}, 2007: {},
                        2008: {}, 2009: {"PNL"}, 2010: {"PSD"}, 2011: {"UDMR"}, 2012: {"PDL"}, 2013: {},
                        2014: {"PNL", "PC"},  2015: {"PSD", "PP DD"}, 2016: {"PNL", "UNPR"},
                        2017: {"PNL", "USR", "ALDE"}, 2018: {}, 2019: {"PSD"}, 2020: {}}

# as a robustness check, I don't use my more in-depth knowledge above and simply count formal leadership changes
party_leader_change_by_the_books = {2001: {"PNL", "PDL"}, 2002: {"PNL"}, 2003: {}, 2004: {"PNL"},
                                    2005: {"PSD", "PDL", "PRM"}, 2006: {},
                                    2007: {}, 2008: {},
                                    2009: {"PNL"}, 2010: {"PSD", "PC"}, 2011: {"UDMR"}, 2012: {"PDL", "UNPR"}, 2013: {},
                                    2014: {"PNL", "PMP"},
                                    2015: {"PSD", "PMP"}, 2016: {"PNL", "UNPR", "PMP"},
                                    2017: {"PNL", "USR", "ALDE"}, 2018: {"PMP"}, 2019: {"PSD"}, 2020: {}}
