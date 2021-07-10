"""Dictionaries that record political affiliations at the county and municipal levels."""

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
#     and PNTCD) which took the mayorality
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