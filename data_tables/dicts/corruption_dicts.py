"""
These are dictionaries indicating which party leaders, ministers, and legislators were convicted (and when), or
alternatively when they were first mentioned in the media. were convicted when.

Different conviction signals can be interpreted in different ways by fellow legislators. Some possibilities are:

WHEN CURRENT PARTY LEADERS ARE CONVICTED

 (A) leader removal via conviction matters only in the year of conviction
        - the bad press doesn't stick

 (B) leader removal via conviction matters for all years after the conviction, until the next election
        - bad press sticks until an election

NB: bad press could also stick forever, but given my prior knowledge of the Romanian scene I nix this possibility: it
    looks like elections and some time in opposition genuinely wash out former bad reputation, to a large extent

I make some assumptions specific to Romanian party leaders. First, I assume that Dan Diaconescu and Dan Voiculescu
were the de facto leaders of their parties (PP DD and PC, respectively) and that the official party leaders were
puppets, i.e. not the real party leaders. Second, that the investigation of Gabriel Oprea by the DNA, which led to his
resignation from both the leadership of the UNPR (the party he founded) and his seat in parliament, can be treated as
a conviction for signalling purposes. To ensure robustness against these substantive judgement calls, I must:

 (C) initially include all of PP DD, PC, and UNPR, then remove them one at a time and see effects on the results.


WHEN CURRENT/FORMER MINISTERS AND/OR LEGISLATORS ARE CONVICTED

Only legislators who were PARTY COLLEAGUES with the convicted while the convicted was in office will be spooked
    - "if they could pin my current/former colleague, they might pin me."
    - NB: for ministers colleague-ship is assumed to mean "we were in the same party when the current/former
          minister was in ministerial office;" this tends to be a shorter period than mere party co-membership

But, it's unclear whether second (or more) convictions send additive messages: the first conviction may have already
driven home the point, so subsequent convictions will not contribute new information. Or not.
    i) additional convictions may target one and the same person
    ii) additional convictions may target different individuals

I assume that additional convictions of the same person do not add more information, so I ignore (i). More convictions
of different people may, however, be consequential. In practice this will not matter for ministers since, for any given
party, very few were convicted in any given year. It may, however, matter for legislators.

We will therefore need to check results against two variables: one that's a binary for "party colleagues convicted in
this year," and another for "category of party colleagues convicted in this year," with levels [zero, one, two+].

NB: things are probably more complicated because former colleagues (who are no longer either in parliament or politics)
    may be convicted, sending a signal to current office-holders. These possibilities introduce so many unknowns
    (e.g. how can we tell whether someone is genuinely retired from politics? How long before a former membership stops
    being relevant?) that I ignore them, and just go with the certain thing: having actually been in the same party,
    at the same time with the convicted.

NB: for building the colleagueship dictionary see party_colleagues.py

"""

# the only former party leader with a final conviction for corruption is Adrian Năstase (first conviction in 30.01.2012,
# upheld on appeal in 20.06.2012) and in a different case sentenced in 30.03.2012 which held on appeal on 06.01.2012; I
# count only the earliest conviction). The only current (unofficial) party leader to receive a conviction subject to
# appeal is Dan Voiculescu, on 26.09.2013 (upheld on appeal 08.08.2014);
# for a history of Năstase's cases which led to guilty verdicts (there were others that did not),  see:
# https://anticoruptie.hotnews.ro/ancheta-8314723-dosarul-trofeul-calitatii-adrian-nastase.htm  and
# https://anticoruptie.hotnews.ro/ancheta-7472284-dosarul-bunuri-din-china-zambaccian-adrian-nastase.htm
# for Voiculescu's case history see https://anticoruptie.hotnews.ro/ancheta-7475495-dosarul-dan-voiculescu.htm)
leader_former_convicted_current_with_appeal = {"Adrian Năstase": "03.01.2012",
                                               "Dan Voiculescu": "26.09.2013"}

# apply rule (A), matters only in that year### Now I look at either current par
leader_conv_one_year = {2014: ("PC"),
                        2015: ("PP DD"),
                        2016: ("UNPR"),
                        2019: ("PSD")}

# apply rule (B), matters for all subsequent years until the next legislative election
leader_conv_multi_year = {2014: ("PC"),
                          2015: ("PP DD", "PC"),
                          2016: ("UNPR", "PP DD", "PC"),
                          2019: ("PSD"),
                          2020: ("PSD")}

# By the time that they received their conviction, some former ministers had changed parties, so they were no longer
# in the party for which they served in government.

# NB: Dan Ioan Popescu was minister in th PSD government, and then deputy for PC before being convicted. I code him here
#     as having belonged to both groups, since his conviction could send messages to colleagues in both parties that
#     they're not safe
# NB: Monica Iacob Ridzi also went from PDL (during which she was minister), to PPDD, to UNPR (by 2014) before losing
#     her seat because she went to jail. Consequently, I mark her in all three parties, on account of she sent a
#     message to all.
# NB: Liviu Dragnea was part of PDL until 2001 when he was still in local politics. I do not mark this, since it was
#     both further ago in time than other cases, and because all of this preceded his first ministerial post by eight
#     years.
# NB: Sorin Frunzăverde was part of both PDL and PNL (though PDL at the time he was minister), so I mark his as both.
# NB: Gabriel Berca was in PDL (as minister) then in PNL. I mark him for both.
# NB: Elena Udrea was part of PDL (as minister) then PMP. I mark her as both.


# TODO put in minister fullnames as they appear in the table
convicted_ministers_names = {2011: {"PSD": "Dan Ioan Popescu",
                                    "PC": "Dan Ioan Popescu"},
                             2012: {"PSD": "Adrian Năstase"},
                             2013: {"PNL": "Decebal Traian Remeş"},
                             2014: {"PSD": "Adrian Năstase",
                                    "PNL": ("Alexandru Tudor Chiuariu", "Relu Fenechiu"),
                                    "PC": "Gheorghe Copos",
                                    "UDMR": "Zsolt Nagy"},
                             2015: {"PC": "Ioan Codrut Sereş",
                                    "PSD": "Miron Tudor Mitrea",
                                    "PDL": "Monica Iacob Ridzi",
                                    "UNPR": "Monica Iacob Ridzi",
                                    "UDMR": "Zsolt Nagy"},
                             2016: {"PNL": ("Corneliu Dobriţoiu", "Relu Fenechiu", "Sorin Frunzăverde"),
                                    "PDL": ("Gabriel Sandu", "Sorin Frunzăverde", "Stelian Fuia"),
                                    "PC": "Ioan Codruţ Sereş",
                                    "PSD": "Nicolae Liviu Dragnea"},
                             2017: {"PDL": "Gabriel Berca",
                                    "PNL": "Gabriel Berca"},
                             2018: {"PSD": ("Constantin Nită", "Dan Coman Şova"),
                                    "PDL": "Elena Gabriela Udrea",
                                    "PMP": "Elena Udrea"},
                             2019: {"PSD": "Nicolae Liviu Dragnea"}
                             }

# TODO make dict where we mark down the ministerial term, i.e. when they were actually minister

"""
The following dictionary shows, per person, the first date for which we could find media mentions (via Google searches)
that they might be investigated for corruption and/or had committed corruption. The purpose is to estimate, however
roughly, the date after which said legislator starts being personally worried about corruption investigations. 

There are several ways we could think about what type of signal is given by having your name and "corruption" mentioned 
in the press. First, we could say that it really only matters short term, say in the calendar year in which you hear
about it. Then again, we might say that it matters medium term, until the next legislative elections that test whether
or not this will affect one electorally. Long-term, one might say that having your name mentioned like that in marks you
for the rest of your political career. Finally, one could say that this signal is later superseded, augmented, 
diminished or somehow modulated by subsequent judicial events: actually being brought to court, having a first sentence
(but subject to appeal) or finally being convicted.

I discount the last three options because: 
  (a) my data probably oversample on those who do make it to court, and some never do because they retire beforehand, 
      charges are dropped under political pressure, etc. In other words, whether or not they make it to court or are 
      even indicted may be endogenous to the process described here.
  (b) a fortiori with having a first sentence passed: tons of intervening variables in the judicial process. I would say
      that this is a very important signal of its own
  (c) if someone IS successfully convicted for corruption then they will face a political interdict, which is lifted 
      after some years but in any case tends to dynamite political careers. So here there's nothing to study, since the
      action directly causes the effect.
      
Consequently I will ultimately make three variables from the date of investigation: whether one is affected in said 
calendar year, from that calendar year (inclusive) until the next election, or from that calendar year (inclusive) until
they drop out of the sample.

NB: three people in this database (Relu Fenechiu, Catalin Marian Radulescu, and Mircea Gheorghe Dragici) were
    investigated for more than one act of corruption. I collapse it and just use the first investigation, since this is
    the one that tips them off that the law is after them. 
"""

media_announcement_dict = {'BIVOLARU Gabriel': '1.1.1996',
                           'GHIVECIU Marian': '1.1.2008',
                           'MISCHIE Nicolae': '4.30.2004',
                           'COPOS Gheorghe': '1.19.2006',
                           'ROŞCA STĂNESCU Sorin Ştefan': '2.7.2006',
                           'MIHĂILESCU Petru Şerban': '3.15.2006',
                           'DUŢU Stelian': '4.5.2006',
                           'DUMITRU Ion': '3.16.2007',
                           'FENECHIU Relu': '5.15.2007',
                           'RUS Ioan Aurel': '12.6.2007',
                           'VOICULESCU Dan': '9.26.2008',
                           'ŞEREŞ Ioan Codruţ': '10.26.2008',
                           'POP Virgil': '11.18.2008',
                           'VOICU Cătălin': '12.11.2009',
                           'SOLOMON Antonie': '3.2.2010',
                           'PANDELE Sorin Andi': '6.16.2010',
                           'PĂSAT Dan': '8.10.2010',
                           'IFTIME Dragoş Adrian': '12.20.2010',
                           'OLOSZ Gergely': '4.12.2011',
                           'NOVAC Cornelia Brînduşa': '5.16.2011',
                           'BANIAS Mircea Marius': '5.23.2011',
                           'IACOB STRUGARU Stelică': '9.19.2011',
                           'CINDREA Ioan': '9.27.2011',
                           'KEREKES Károly': '9.27.2011',
                           'NEACŞU Marian': '11.22.2011',
                           'STANCIU Anghel': '12.30.2011',
                           'POPESCU Dumitru Dian': '7.3.2012',
                           'MĂGUREANU Cezar Mircea': '7.24.2012',
                           'BUCIUTA Ştefan': '8.6.2012',
                           'MOVILĂ Petru': '9.28.2012',
                           'TRĂŞCULESCU Alin Silviu': '11.11.2012',
                           'STAN Ion': '11.22.2012',
                           'DIACONU Mircea': '11.23.2012',
                           'COSTIN Gheorghe': '3.3.2013',
                           'MÁTÉ András Levente': '3.13.2013',
                           'NICULESCU MIZIL ŞTEFĂNESCU Oana': '3.14.2013',
                           'LONGHER Ghervazen': '3.16.2013',
                           'LAZĂR Sorin Constantin': '3.18.2013',
                           'CRĂCIUNESCU Grigore': '3.21.2013',
                           'CĂTĂNICIU Steluţa Gustica': '3.27.2013',
                           'OLTEAN Ioan': '9.12.2013',
                           'SILAGHI Ovidiu Ioan': '9.12.2013',
                           'BĂDĂLĂU Niculae': '10.28.2013',
                           'MERKA Adrian Miroslav': '11.11.2013',
                           'GROSARU Mircea': '11.11.2013',
                           'MIRCOVICI Niculae': '11.11.2013',
                           'COMAN Gheorghe': '12.19.2013',
                           'PÂSLARU Florin Costin': '1.7.2014',
                           'GLIGA Vasile Ghiorghe': '1.8.2014',
                           'RĂDULESCU Cătălin Marian': '2.17.2014',
                           'COSMA Vlad Alexandru': '2.19.2014',
                           'RUŞANU Dan Radu': '2.21.2014',
                           'DRĂGHICI Mircea Gheorghe': '3.4.2014',
                           'SECĂŞAN Iosif': '3.27.2014',
                           'ISĂILĂ Marius Ovidiu': '4.4.2014',
                           'POPESCU Florin Aurelian': '4.23.2014',
                           'POPOVICIU Alin Augustin Florin': '5.30.2014',
                           'SĂMĂRTINEAN Cornel Mircea': '5.30.2014',
                           'DRĂGHICI Sonia Maria': '6.10.2014',
                           'CORDOŞ Alexandru': '8.12.2014',
                           'DINIŢĂ Ion': '10.10.2014',
                           'URSĂRESCU Dorinel': '10.21.2014',
                           'CHIRU Gigi Christian': '10.30.2014',
                           'MARKÓ Attila Gabor': '11.21.2014',
                           'CULEŢU Dănuţ': '1.6.2015',
                           'GREBLĂ Toni': '1.22.2015',
                           'NICOLESCU Theodor Cătălin': '3.18.2015',
                           'ROŞCA Mircea': '4.14.2015',
                           'OCHI Ion': '4.21.2015',
                           'GHIŢĂ Sebastian Aurelian': '7.7.2015'}

# I now do the same for legislators and the date on which they received their first guilty verdict (subject, however,
# to appeal). Again, ultimately I will make three variables from this information.
# NB: Relu Fenechiu, Codruţ Şereş, Corneliu Dobriţoiu, George Copos, and Tudor Chiuariu were also ministers. Since I
#     count them with the ministers I discount them here, to avoid double counting.
#     Likewise Dan Voiculescu and Liviu Dragnea were counted with party leaders, so I ignore them here.
# NB: I do not know the exact date of first conviction for Gabriel Bivolaru, Ioan Aurel Rus, Sorin Andi Pandele so I put
#     January first as the default date
# NB: the month is missing for Viorel Gheorghiu, I put January as the default
first_conviction_appeal_possible = {'BIVOLARU Gabriel': '01.01.2002',
                                    'GHIVECIU Marian': '12.05.2015',
                                    'MISCHIE Nicolae': '12.07.2007',
                                    'MIHĂILESCU Petru Şerban': '20.12.2011',
                                    'RUS Ioan Aurel': '01.01.2012',
                                    'POP Virgil': '16.12.2011',
                                    'VOICU Cătălin': '01.06.2012',
                                    'SOLOMON Antonie': '11.07.2013',
                                    'PANDELE Sorin Andi': '01.01.2012',
                                    'PĂSAT Dan': '10.04.2013',
                                    'IFTIME Dragoş Adrian': '26.06.2013',
                                    'OLOSZ Gergely': '17.07.2013',
                                    'IACOB STRUGARU Stelică': '25.11.2014',
                                    'KEREKES Károly': '27.10.2014',
                                    'NEACŞU Marian': '24.02.2015',
                                    'STANCIU Anghel': '17.03.2015',
                                    'POPESCU Dumitru Dian': '28.11.2014',
                                    'MĂGUREANU Cezar Mircea': '01.10.2018',
                                    'BUCIUTA Ştefan': '06.06.2014',
                                    'TRĂŞCULESCU Alin Silviu': '20.03.2015',
                                    'COSTIN Gheorghe': '07.05.2015',
                                    'MÁTÉ András Levente': '01.07.2014',
                                    'NICULESCU MIZIL ŞTEFĂNESCU Oana': '07.10.2014',
                                    'LONGHER Ghervazen': '17.06.2014',
                                    'LAZĂR Sorin Constantin': '15.04.2014',
                                    'CRĂCIUNESCU Grigore': '16.06.2014',
                                    'MERKA Adrian Miroslav': '21.1.2015',
                                    'COMAN Gheorghe': '30.01.2014',
                                    'PÂSLARU Florin Costin': '23.03.2015',
                                    'GLIGA Vasile Ghiorghe': '12.02.2015',
                                    'RĂDULESCU Cătălin Marian': '31.03.2016',
                                    'COSMA Vlad Alexandru': '01.11.2016',
                                    'SECĂŞAN Iosif': '18.11.2014',
                                    'ISĂILĂ Marius Ovidiu': '12.4.2016',
                                    'POPESCU Florin Aurelian': '4.12.2015',
                                    'DRĂGHICI Sonia Maria': '03.23.2015',
                                    'DINIŢĂ Ion': '30.04.2020',
                                    'URSĂRESCU Dorinel': '27.05.2016',
                                    'CHIRU Gigi Christian': '13.03.2015',
                                    'NICOLESCU Theodor Cătălin': '14.02.2018',
                                    'ROŞCA Mircea': '28.10.2019',
                                    'OCHI Ion': '01.11.2017',
                                    'THUMA Hubert Petru Ştefan': "22.11.2013",
                                    'MUNTEAN Mircia': "08.07.2013",
                                    'DRĂGHICI Mircea Gheorghe': '15.10.2020',
                                    'GHEORGHIU Viorel': '11.01.2005'}

# this shows all the people who received a final, guilty verdict for a crime of corruption (i.e. no possibility of
# appeal) as well as the date on which they received said verdict.
final_guilty_verdict = {'BIVOLARU Gabriel': '01.04.2004',
                        'GHIVECIU Marian': '23.02.2016',
                        'MISCHIE Nicolae': '18.03.2013',
                        'ROŞCA STĂNESCU Sorin Ştefan': '7.10.2014',
                        'DUMITRU Ion': '07.06.2013',
                        'POP Virgil': '26.03.2012',
                        'VOICU Cătălin': '22.04.2013',
                        'SOLOMON Antonie': '20.09.2013',
                        'PANDELE Sorin Andi': '21.01.2014',
                        'PĂSAT Dan': '12.12.2013',
                        'IFTIME Dragoş Adrian': '25.06.2014',
                        'OLOSZ Gergely': '20.12.2018',
                        'CINDREA Ioan': '15.09.2015',
                        'KEREKES Károly': '10.02.2015',
                        'NEACŞU Marian': '23.02.2016',
                        'STANCIU Anghel': '24.11.2015',
                        'POPESCU Dumitru Dian': '31.05.2016',
                        'BUCIUTA Ştefan': '10.03.2015',
                        'STAN Ion': '25.01.2016',
                        'COSTIN Gheorghe': '04.06.2016',
                        'MÁTÉ András Levente': '10.02.2015',
                        'NICULESCU MIZIL ŞTEFĂNESCU Oana': '24.10.2016',
                        'LAZĂR Sorin Constantin': '05.12.2014',
                        'CRĂCIUNESCU Grigore': '28.03.2016',
                        'COMAN Gheorghe': '28.04.2014',
                        'PÂSLARU Florin Costin': '15.07.2016',
                        'GLIGA Vasile Ghiorghe': '30.06.2015',
                        'RĂDULESCU Cătălin Marian': '05.12.2016',
                        'SECĂŞAN Iosif': '25.03.2015',
                        'POPESCU Florin Aurelian': '14.03.2016',
                        'URSĂRESCU Dorinel': '07.06.2020',
                        'CHIRU Gigi Christian': '13.11.2017',
                        'NICOLESCU Theodor Cătălin': '08.10.2019',
                        'THUMA Hubert Petru Ştefan': "14.10.2014",
                        'GIREADĂ Dumitru Verginel': "05.04.2012",
                        'MUNTEAN Mircia': "24.09.2013",
                        'DRĂGHICI Mircea Gheorghe': '15.10.2020',
                        'GHEORGHIU Viorel': '04.06.2008'}

# the next dict shows a count of how many legislators in a given year, in a given party were given final,
# guilty sentences for crimes of corruption

# NB: this first version counts both current and former members of the party. To ascertain party membership I simply
#     look in my own data tables to see which party(/ies) the deputy was listed under their tenure

# Dan Păsat went from PNL to PDL: I count him in both. Likewise for Dumitru Dian Popescu, went from PNL to ALDE.
# I don't include "independents" since no one ever stars in that category. For instance, One Niculescu-Mizil Ştefan
# went from PSD to independent and was then convicted. Gheorghe Coman went from PP DD to PC in 2014. Iosif Secăşan went
# from PDL to PNL in 2012. Florin Aurelian Popescu kept flip-flopping between PDL and PNL (but no more PDL after 2014).
# Dorinel Ursărescu went from PNL to ALDE in 2014. Mircia Muntean went from PDL to PSD in 2014

# TODO: check before Catalin Voicu to make sure nobody switched parties; only chcecked after

legis_guilty_count = {2004: {"PSD": 1},
                      2005: {},
                      2006: {},
                      2007: {},
                      2008: {"PSD": 1},
                      2009: {},
                      2010: {},
                      2011: {},
                      2012: {"PNL": 2},
                      2013: {"PSD": 3, "PP DD": 1, "PDL": 2, "PNL": 2},
                      2014: {"PNL": 1, "PC": 2, "PDL": 2, "PSD": 1, "PP DD": 1},
                      2015: {"PNL": 1, "PDL": 1, "PSD": 3, "UDMR": 2, "MIN": 1},
                      2016: {"PSD": 6, "PNL": 4, "ALDE": 1},
                      2017: {"PNL": 1},
                      2018: {"UDMR": 1},
                      2019: {"PNL": 1},
                      2020: {"PNL": 1, "ALDE": 1, "PSD": 1}}
