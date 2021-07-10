"""Dictionaries recording membership in government, typically in coalitions."""

# NB: the lists of gov't coaltion partners only include parties that were popularly elected. UNPR, for instance, was an
# intra-parliamentary party for 2008-2012 formed by deputies leaving their original parties, so even though it was a
# junior partner in Ponta 1, it's not listed there as such. Conceptually, this is because we measure time to first
# party defection, and since everyone in UNPR must have defected to join that party in the 2008-2012 legislature, there
# can be no UNPR observations at all for that period.
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

# NB: I end up ignoring confidence and supply agreements, where a party agrees to support a minority government from
# parliament without participating in government themselves, because it's very difficult to get hard information on
# this: such agreements are usually informal, it's very rare that Romanian party leaders publicly agree to such things
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