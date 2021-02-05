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
                          2015: ("PP DD", "PC") ,
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