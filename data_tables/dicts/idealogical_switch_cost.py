"""
Different party switches have different ideological costs: it's not the same whether one moves from a left to a center p
arty, or a left to a right party. Since I do not know of inductive, ideological left-right scales for Romania, and since
the Poole & Rosenthal method (averaged across party members) isn't doable in closed-list parliamentary systems as there
is extremely little variance in roll call votes, I do a simpler method.

First, each party is cateorised as "left", "center" or "right" which agrees with previously published research.
Then each observed edge connecting two parties is given a weight: for example, left-left has value zero, left-center
has weight one, and left-right has weight two. The idea is that moving in your own family has no ideological cost,
that moving to and from the center has some cost, and moving across the spectrum is most costly.

The categorisation of parties is:
    PSD: left
    PRM: left
    UNPR: center
    PNTCD: right
    PNL: right (pre-merger with PDL in 2014), center (post-merger with PDL in 2014)
    PDL: center
    PP DD: center
    ALDE: center
    PC: center
    PRO: left
    PMP: right
    USR: right
    PUNR: left
    PL'93: right
    FC: center
    PAC: center
    PNL CD: right

NB: I treat becoming independent as having zero ideological cost. Certainly there is great practical cost when you
    caucus with nobody, but there is no cost of looking like a turncoat

NB: any movement post-2014 (inclusive) that's PDL-PNL is treated as 0, since that's the year in which those two parties
    merged.
"""

ideological_pswitch_costs = {"any period": {'PRM-PSD': 0,
                                            'PSD-UNPR': 1,
                                            'PNTCD-IND': 0,
                                            'PDL-UNPR': 0,
                                            'PDL-IND': 0,
                                            'PDL-PSD': 1,
                                            'PSD-IND': 0,
                                            'PDSR-IND': 0,
                                            'PP DD-UNPR': 0,
                                            'ALDE-PSD': 1,
                                            'PRM-PDL': 1,
                                            'PSD-PC': 1,
                                            'PSD-PRO': 0,
                                            'PRM-IND': 0,
                                            'PP DD-PSD': 1,
                                            'PMP-PSD': 2,
                                            'PSD-PDL': 1,
                                            'USR-IND': 0,
                                            'PMP-ALDE': 1,
                                            'PUNR-IND': 0,
                                            'PRM-PC': 1,
                                            'UNPR-PSD': 1,
                                            "PL'93-IND": 0,
                                            'PDL-PC': 0,
                                            'PP DD-ALDE': 0,
                                            'PSD-PRM': 0,
                                            "PAC-PL'93": 0,
                                            'PP DD-PC': 0,
                                            'ALDE-IND': 0,
                                            'PC-IND': 0,
                                            'PSM-IND': 0,
                                            'PNTCD-UNPR': 1,
                                            'PP DD-IND': 0,
                                            'UNPR-IND': 0,
                                            'PNL CD-IND': 0,
                                            'PP DD-PDL': 0,
                                            'PDL-ALDE': 0,
                                            'ALDE-PMP': 1,
                                            'PC-UNPR': 0,
                                            'UDMR-IND': 0,
                                            'PSD-PP DD': 1,
                                            'ALDE-PRO': 1,
                                            'PSD-ALDE': 1,
                                            'PC-PSD': 1,
                                            'PC-PRM': 1},
                             "pre-2014": {'PSD-PNL': 2,
                                          'PNL-PSD': 2,
                                          'PC-PNL': 1,
                                          'PP DD-PNL': 1,
                                          'FC-PNL': 1,
                                          'PNL-ALDE': 1,
                                          'ALDE-PNL': 1,
                                          'PNL-IND': 0,
                                          'PNL-UNPR': 1,
                                          'PNL-PDL': 1,
                                          'PRM-PNL': 2,
                                          'PDL-PNL': 1},
                             "post-2014": {'PSD-PNL': 1,
                                           'PNL-PSD': 1,
                                           'PC-PNL': 0,
                                           'PP DD-PNL': 0,
                                           'FC-PNL': 0,
                                           'PNL-ALDE': 1,
                                           'ALDE-PNL': 0,
                                           'PDL-PNL': 0,
                                           'PNL-IND': 0,
                                           'PNL-UNPR': 0,
                                           'USR-PNL': 1
                                           }
                             }
