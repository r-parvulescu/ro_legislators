"""
These are dictionaries indicating which ministers and/or party leaders were convicted when. The dictionaries differ
because we can give different interpretations to the signal that such convictions send to fellow legislators.

WITH RESPECT TO CONVICTED CURRENT PARTY LEADERS

There are two ways of interpreting the conviction: either it messes up the internal party networks in the year in which
it occurs, or it does so permanently until the next legislative elections reset internal party struggles. Therefore:

 (A) leader removal via conviction matters only in the year of conviction

 (B) leader removal via conviction matters for all years after the conviction, until the next election

There are several other judgement calls here. First, I assume that Dan Diaconescu and Dan Voiculescu were the de facto
leaders of their parties (PP DD and PC, respectively) and that the official party leaders were puppets. Second, UNPR's
Gabriel Oprea resigned from parliament and the party leadership not because he was convicted, but because he was under
investigation by the DNA. All these judgement calls suggest the following robustness tests:

 (C) initially include all of PP DD, PC, and UNPR, then remove them one at a time and see effects on the results.

Consequently, I code in two cases (A) and (B), then implement (C) in the r code.

WITH RESPECT TO CONVICTED CURRENT/FORMER MINISTERS

There are several ways in which one could interpret the messages sent by conviction of a current/former minister

 1) all of that minister's party colleagues, past and present and of whichever party, interpret this as "if this could
    happen to one of our ministers, it could happen to me."

 2) only the people in the party of which the minister was a part of WHILE in ministerial office will get the message
    "if they could pin a minister, they might pin me for what I did when I was in that party, in that time."

 3) only people in the current party might get the message, i.e. "after that minister left their former party and came
    to us they lost the former party's protection, and our party isn't strong enough to give this indicted minister
    cover, so our party wouldn't be strong enough to back me."

 4) the people in the current party (in which the minister did NOT serve while they were minister) conclude that they
    personally are safe, since this is really just revenge from the party that the minister left, and not a general
    statement about the new party's ability to protect its people from convictions. Consequently, when a minister who
    changed parties is convicted, nobody gets any message: both old and new party colleagues think "serves them right."

 5) a second(plus) conviction of the same person may not send much of a message: the first conviction already drove
    home the point, subsequent convictions do not contribute new information

 6) additional convictions of different people from the same party contribute to the signal: it matters whether one,
    two, or three former ministers from the same party were convicted in the same time period.

 7) PDL stopped existing in 2015 after its decisive internal split, with some PDL members going to PNL and others into
    the wilds or to PMP. Thus it's unclear who after 2015 would get the message of a former PDL minister being
    convicted: perhaps old colleagues now in other parties, but that's a series of uncertain judgement calls. The
    conservative coding decision is to just through out post-2015 PDL signals

Below I assume that (5), (6), and (7) are true: the second conviction of the same person doesn't matter, the first
convictions of multiple people do add up, and we throw out post-2015 PDL signals. That said, with respect to (6) I don't
discriminate between two or three convictions of different people in the same year: the scale is 0, 1, 2, where "2"
actually means "2+", so it's a sort-of ordinal scale, and is treated numerically, i.e. NOT as factors. It's  bit of a
fudge, gradnted, but IMO justified by the fact that three convictions from the same party in one year are very rare.

I run each of (1)-(4) as a separate robustness test.

"""

# apply rule (A), matters only in that year
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
# NB: Monica Iacob Ridzi also went from PDL (duing which she was minister), to PPDD, to UNPR (by 2014) before losing her
#     seat because she went to jail. Consequently, I mark her in all three parties, on account of she sent a message to
#     all.
# NB: Liviu Dragnea was part of PDL until 2001 when he was still in local politics. I do not mark this, since it was
#     both further ago in time than other cases, and because all of this preceded his first ministerial post by eight
#     years.
# NB: Sorin Frunzăverde was part of both PDL and PNL (though PDL at the time he was minister), so I mark his as both.
# NB: Gabriel Berca was in PDL (as minister) then in PNL. I mark him for both.
# NB: Elena Udrea was part of PDL (as minister) then PMP. I mark her as both.

convicted_ministers_names = {2011: {"PSD": "Dan Ioan Popescu",
                                    "PC": "Dan Ioan Popescu"},
                             2012: {"PSD": "Adrian Năstase"},
                             2013: {"PNL": "Decebal Traian Remeş"},
                             2014: {"PSD": "Adrian Năstase",
                                    "PNL": ("Alexandru Tudor Chiuariu", "Relu Fenechiu"),
                                    "PC": "George Copos",
                                    "UDMR": "Zsolt Nagy"},
                             2015: {"PC": "Ioan Codrut Sereş",
                                    "PSD": "Miron Tudor Mitrea",
                                    "PDL": "Monica Iacob Ridzi",
                                    "UNPR": "Monica Iacob Ridzi",
                                    "UDMR": "Zsolt Nagy"},
                             2016: {"PNL": ("Corneliu Dobriţoiu", "Relu Fenechiu", "Sorin Frunzăverde"),
                                    "PDL": ("Gabriel Sandu", "Soring Frunzăverde", "Stelian Fuia"),
                                    "PC": "Ioan Codruţ Sereş",
                                    "PSD": "Nicolae Liviu Dragnea"},
                             2017: {"PDL": "Gabriel Berca",
                                    "PNL": "Gabriel Berca"},
                             2018: {"PSD": ("Constantin Nită", "Dan Coman Şova"),
                                    "PDL": "Elena Gabriela Udrea",
                                    "PMP": "Elena Udrea"},
                             2019: {"PSD": "Nicolae Liviu Dragnea"}
                             }

# apply rule (1), full signal
min_conv_full = {2011: {"PC": 1, "PSD": 1},
                 2012: {"PSD": 1},
                 2013: {"PNL": 1},
                 2014: {"PNL": 2, "PC": 1, "UDMR": 1},
                 2015: {"PC": 1, "PSD": 1, "PDL": 1, "UNPR": 1},
                 2016: {"PNL": 2, "PSD": 1},
                 2017: {"PNL": 1},
                 2018: {"PSD": 2, "PMP": 1}}

# apply rule (2), signal only reaches old party colleagues
min_conv_old = {2011: {"PSD": 1},
                2012: {"PSD": 1},
                2013: {"PNL": 1},
                2014: {"PNL": 2, "PC": 1, "UDMR": 1},
                2015: {"PC": 1, "PSD": 1, "PDL": 1},
                2016: {"PNL": 2, "PSD": 1},
                2018: {"PSD": 2}}

# apply rule (3), signal only reaches new party colleagues
min_conv_new = {2011: {"PC": 1},
                2012: {"PSD": 1},
                2013: {"PNL": 1},
                2014: {"PNL": 2, "PC": 1, "UDMR": 1},
                2015: {"PC": 1, "PSD": 1, "PDL": 1, "UNPR": 1},
                2016: {"PNL": 2, "PSD": 1},
                2017: {"PNL": 1},
                2018: {"PSD": 2, "PMP": 1}}

# apply rule (4), signals from party-switching former ministers are not consequential, i.e. reach nobody
min_conv_none = {2012: {"PSD": 1},
                 2013: {"PNL": 1},
                 2014: {"PNL": 2, "PC": 1, "UDMR": 1},
                 2015: {"PC": 1, "PSD": 1},
                 2016: {"PNL": 2, "PSD": 1},
                 2018: {"PSD": 2}}

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

media_announcement_dict = {'Bivolaru Gabriel': '1.1.1996',
                           'Ghiveciu Marian': '1.1.2008',
                           'Mischie Nicolae': '4.30.2004',
                           'Copos George': '1.19.2006',
                           'Roșca Stănescu Sorin': '2.7.2006',
                           'Mihăilescu Șerban': '3.15.2006',
                           'Duțu Stelian': '4.5.2006',
                           'Dumitru Ion': '3.16.2007',
                           'Fenechiu Relu': '5.15.2007',
                           'Rus Ioan Aurel': '12.6.2007',
                           'Voiculescu Dan': '9.26.2008',
                           'Șereș Codruț': '10.26.2008',
                           'Pop Virgil': '11.18.2008',
                           'Voicu Cătălin': '12.11.2009',
                           'Solomon Antonie': '3.2.2010',
                           'Pandele Sorin Andi': '6.16.2010',
                           'Păsat Dan': '8.10.2010',
                           'Iftime Dragoș Adrian': '12.20.2010',
                           'Olosz Gergely': '4.12.2011',
                           'Novac Cornelia Brîndușa': '5.16.2011',
                           'Banias Mircea Marius': '5.23.2011',
                           'Strugaru Stelică Iacob': '9.19.2011',
                           'Cindrea Ioan': '9.27.2011',
                           'Kerekes Károly': '9.27.2011',
                           'Neacșu Marian': '11.22.2011',
                           'Stanciu Anghel': '12.30.2011',
                           'Popescu Dumitru Dian': '7.3.2012',
                           'Măgureanu Cezar Mircea': '7.24.2012',
                           'Buciuta Ștefan': '8.6.2012',
                           'Movilă Petru': '9.28.2012',
                           'Trășculescu Alin': '11.11.2012',
                           'Stan Ion': '11.22.2012',
                           'Diaconu Mircea': '11.23.2012',
                           'Costin Gheorghe': '3.3.2013',
                           'Máté András Levente': '3.13.2013',
                           'Niculescu-Mizil Oana': '3.14.2013',
                           'Longher Ghervazen': '3.16.2013',
                           'Lazăr Sorin Constantin': '3.18.2013',
                           'Crăciunescu Grigore': '3.21.2013',
                           'Cătăniciu Steluța Gustica': '3.27.2013',
                           'Oltean Ioan': '9.12.2013',
                           'Silaghi Ovidiu': '9.12.2013',
                           'Bădălău Niculae': '10.28.2013',
                           'Merka Adrian Miroslav': '11.11.2013',
                           'Grosaru Mircea': '11.11.2013',
                           'Mircovici Niculae': '11.11.2013',
                           'Coman Gheorghe': '12.19.2013',
                           'Pâslaru Florin Costin': '1.7.2014',
                           'Gliga Vasile Ghiorghe': '1.8.2014',
                           'Rădulescu Cătălin Marian': '2.17.2014',
                           'Cosma Vlad Alexandru': '2.19.2014',
                           'Rușanu Dan Radu': '2.21.2014',
                           'Drăghici Mircea Gheorghe': '3.4.2014',
                           'Secășan Iosif': '3.27.2014',
                           'Isăilă Marius Ovidiu': '4.4.2014',
                           'Popescu Florin Aurelian': '4.23.2014',
                           'Popoviciu Alin Augustin Florin': '5.30.2014',
                           'Sămărtinean Cornel Mircea': '5.30.2014',
                           'Drăghici Sonia Maria': '6.10.2014',
                           'Cordoș Alexandru': '8.12.2014',
                           'Diniță Ion': '10.10.2014',
                           'Ursărescu Dorinel': '10.21.2014',
                           'Chiru Gigi Christian': '10.30.2014',
                           'Markó Attila': '11.21.2014',
                           'Culețu Dănuț': '1.6.2015',
                           'Greblă Toni': '1.22.2015',
                           'Nicolescu Theodor Cătălin': '3.18.2015',
                           'Roșca Mircea': '4.14.2015',
                           'Ochi Ion': '4.21.2015',
                           'Ghiță Sebastian': '7.7.2015'}

media_announcement_dict_pids = {2359: '1.1.1996',
                                2784: '1.1.2008',
                                1001: '4.30.2004',
                                1616: '1.19.2006',
                                2661: '2.7.2006',
                                1903: '3.15.2006',
                                2418: '4.5.2006',
                                1717: '3.16.2007',
                                992: '5.15.2007',
                                1585: '12.6.2007',
                                1973: '9.26.2008',
                                676: '10.26.2008',
                                1235: '11.18.2008',
                                810: '12.11.2009',
                                2621: '3.2.2010',
                                2516: '6.16.2010',
                                2638: '8.10.2010',
                                360: '12.20.2010',
                                1543: '4.12.2011',
                                1778: '5.16.2011',
                                2531: '5.23.2011',
                                1155: '9.19.2011',
                                1804: '9.27.2011',
                                1673: '9.27.2011',
                                1931: '11.22.2011',
                                2529: '12.30.2011',
                                2314: '7.3.2012',
                                2077: '7.24.2012',
                                966: '8.6.2012',
                                2228: '9.28.2012',
                                1740: '11.11.2012',
                                563: '11.22.2012',
                                2754: '11.23.2012',
                                1294: '3.3.2013',
                                48: '3.13.2013',
                                1397: '3.14.2013',
                                2437: '3.16.2013',
                                1488: '3.18.2013',
                                858: '3.21.2013',
                                2318: '3.27.2013',
                                1371: '9.12.2013',
                                1357: '9.12.2013',
                                286: '10.28.2013',
                                2046: '11.11.2013',
                                930: '11.11.2013',
                                2210: '11.11.2013',
                                2434: '12.19.2013',
                                1253: '1.7.2014',
                                1993: '1.8.2014',
                                705: '2.17.2014',
                                1246: '2.19.2014',
                                2394: '2.21.2014',
                                1068: '3.4.2014',
                                1344: '3.27.2014',
                                144: '4.4.2014',
                                1873: '4.23.2014',
                                40: '5.30.2014',
                                2660: '5.30.2014',
                                2774: '6.10.2014',
                                2476: '8.12.2014',
                                1326: '10.10.2014',
                                1047: '10.21.2014',
                                1092: '10.30.2014',
                                2514: '11.21.2014',
                                948: '1.6.2015',
                                328: '1.22.2015',
                                1075: '3.18.2015',
                                776: '4.14.2015',
                                2574: '4.21.2015',
                                2559: '7.7.2015'}
