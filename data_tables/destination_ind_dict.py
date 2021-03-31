"""
I count party departures as when a person renounced their party membership, NOT when they left their parliamentary party
group, i.e. the people that they caucus with in the legislature. This is because PPG dynamics can be quite unstable
since sometimes a PPG disappears because they lose the minimum number of people to have it registered, but most members
will not have left the party. So party membership is a more reliable measure of party affiliation than PPG usually is.

The exception is when it comes to party switching. If a person genuinely leaves their party (i.e. renounces membership)
then they will also (almost) always get booted out of the caucus. However, a party switcher (who renounced both general
membership and caucus) may have gone to another caucus WITHOUT joining the new party as a member. This might be because
they still have some reservations, or because that caucus actually is not yet associated with a larger party (the case
sometimes with parties that start in parliament as splinters of other parties), or because the accepting party wants the
vote in parliament but not the reputation of accepting turncoats, etc. In any case, substantively the legislator DID
switch parties, but this only shows up in the caucus information, NOT in general membership.

Another thing complicating the caucus measure is that some parties are known as go-betweens, so that a switching
parliamentarian leaves party X for Y, but is in party Y only for a short while before moving to party Z, which was the
destination all along. The fact that there is this intermediary step partly depends on the complicated horse-trading in
parliament, because nominal membership can be helpful in some cases, even if for a short time. But in this case someone
with wider knowledge of the scene needs to be to look at the history of caucus switching and decide which party was
actually the destination party. I do not think that in a reasonable amount of time I could train a computer to replicate
my own knowledge of Romanian parliamentary switching dynamics. Note that this go-betweening minimally affects those who
formally join another party as members, since that's a much louder and clearer message: it wouldn't make sense to delay
caucuses affiliation while immediately registering in the destination party.

Finally, the same PPG might change names and/or formal identity several times in one legislature, especially those
that form out of splinters/factions from other parties: UNPR and ALDE both experienced this in different legislatures.

ERGO, below we have a dictionary of all party switchers in the 2008-2012, 2012-2016, and 2016-2020 legislatures who are
marked as having become permanently independent after their first switch (since they did not formally join another
general party organisation) but who in fact did ultimately join some other party/faction with  whom they caucused. As is
the case for the baseline measure, I only include the code of the FIRST party to which the person switched: if they
genuinely switched twice in the same legislature, I only count the first one (since this ultimately feeds into a single-
event hazard model).

NB: for the 2008-2012, "Grupul Deputaților Independenți" was actually the pre-cursor to the UNPR. Granted there were
    further schisms etc. in this group, but the switch was "home --> UNPR." For this legislature genuinely independent
    legislators were called "neafiliați"

NB: There is only one case in which a person leaves the party formally but still caucuses with them: Cosmin Mihai
    POPESCU, in the 2008-2012 legislature.

     CHECK WHY Gheorghe ROMAN 2008-2012 WASN'T MARKED AS A STRAIGHT PDL-PSD SWTICH

NB: for future extensions, note that for whatever reason Siminica Mirea is listed as two separate people for the
    2016-2020 and 2020-2024 legislature
"""

destination_ind_dict = {"2008-2012": {'TĂRÂŢĂ Culiţă': "UNPR",
                                      'BOSTAN Emil': "UNPR",
                                      'IACOB RIDZI Monica Maria': "IND",
                                      'MAZILU Constantin': "UNPR",
                                      'DAVID Gheorghe': "PDL",
                                      'NECULAI Marius': "IND",
                                      'STERIU Valeriu Andrei': "UNPR",
                                      'CHIVU Sorin Serioja': "UNPR",
                                      'AVRAM Marian': "IND",
                                      'BOLDEA Mihail': "UNPR",
                                      'DOBRA Nicolae': "UNPR",
                                      'JIPA Florina Ruxandra': "UNPR",
                                      'DUGULESCU Marius Cristinel': "UNPR",
                                      'IORDACHE Luminiţa': "UNPR",
                                      'DUMITRU Constantin': "PNL",
                                      'IORDĂNESCU Anghel': "UNPR",
                                      'MĂRCUŢIANU Ovidius': "UNPR",
                                      'VASILE Aurelia': "UNPR",
                                      'TABUGAN Ion': "UNPR",
                                      'IRIMESCU Mircea': "PNL",
                                      'CHIRVĂSUŢĂ Laurenţiu': "UNPR",
                                      'MOREGA Dan Ilie': "UNPR",
                                      'PRODAN Tiberiu Aurelian': "PDL",
                                      'GEOANĂ Mircea Dan': "IND",
                                      'NICOLICEA Eugen': "UNPR",
                                      'NEDELCU Vasile': "UNPR",
                                      'CÂMPANU Liviu': "UNPR",
                                      'OAJDEA Daniel Vasile': "IND",
                                      'ŢAGA Claudiu': "UNPR",
                                      'CĂRARE Viorel': "UNPR",
                                      'PIRPILIU Ştefan Daniel': "IND",
                                      'CRĂCIUN Avram': "UNPR",
                                      'DIACONESCU Cristian': "UNPR",
                                      'POPESCU Cosmin Mihai': "IND",
                                      'MARIAN Ovidiu': "PNL",
                                      'ZOICAŞ Gheorghe': "UNPR",
                                      'CIBU Constantin Sever': "UNPR",
                                      'SÂRBU Marian': "UNPR",
                                      'FRUNZULICĂ Doru Claudian': "UNPR",
                                      'GROSU Corneliu': "UNPR",
                                      'ŢUREA Răzvan': "UNPR",
                                      'MIHĂILESCU Petru Şerban': "UNPR",
                                      'BARNA Maria Eugenia': "UNPR",
                                      'NICULESCU MIZIL ŞTEFĂNESCU Oana': "IND",
                                      'SĂNIUŢĂ Marian Florian': "IND",
                                      'TOMA Ion': "UNPR",
                                      'PRIGOANĂ Vasile Silviu': "IND",
                                      'OPREA Gabriel': "UNPR",
                                      'STAVROSITU Maria': "UNPR",
                                      'SOPORAN Vasile Filip': "UNPR",
                                      'ROMAN Gheorghe': "PSD"},
                        "2012-2016": {'DUMITRESCU Florinel': "PSD",
                                      'FENECHIU Cătălin Daniel': "PNL",
                                      'ANGHEL Gabriela Lola': "PNL",
                                      'MARIN Nicolae': "PSD",
                                      'BUTNARU Florinel': "PSD",
                                      'MARCU Nicu': "ALDE",
                                      'CHIŢOIU Daniel': "ALDE",
                                      'MOCANU Victor': "IND",
                                      'TARARACHE Mihai': "IND",
                                      'COSTE Marius': "PSD",
                                      'PALEOLOGU Theodor': "IND",
                                      'POPA Octavian Marius': "ALDE",
                                      'BUDURESCU Daniel Stamate': "ALDE",
                                      'MANOLACHE Marius': "IND",
                                      'NASTA Nicolae': "ALDE",
                                      'TALOŞ Gheorghe Mirel': "ALDE",
                                      'PĂRAN Dorin': "ALDE",
                                      'EPARU Ion': "IND",
                                      'EHEGARTNER Petru': "ALDE",
                                      'ZGONEA Valeriu Ştefan': "IND",
                                      'GUST BĂLOŞIN Florentin': "IND",
                                      'MIHAI Aurelian': "ALDE",
                                      'GEOANĂ Mircea Dan': "IND",
                                      'NIŢU Remus Daniel': "ALDE",
                                      'BLĂJUŢ Viorel Ionel': "PP DD",
                                      'ZAHARCU Neviser': "IND",
                                      'CALIMENTE Mihăiţă': "ALDE",
                                      'CIOBANU Liliana': "PP DD",
                                      'BĂIŞANU Ştefan Alexandru': "ALDE",
                                      'BECALI George': "IND",
                                      'NICOLAE Alexandri': "ALDE",
                                      'MARIAN Valer': "PP DD",
                                      'CADĂR Leonard': "PSD",
                                      'STURZU Mihai Răzvan': "IND",
                                      'POPESCU Corneliu': "IND",
                                      'GHIŞE Ioan': "IND",
                                      'TOMAC Eugen': "IND",
                                      'POPEANGĂ Vasile': "PNL",
                                      'VOLOSEVICI Andrei Liviu': "IND",
                                      'GEREA Andrei Dominic': "ALDE",
                                      'RĂDULESCU Romeo': "ALDE",
                                      'DRAGOMIR Maria': "IND",
                                      'PELICAN Dumitru': "IND",
                                      'BARBU Daniel Constantin': "ALDE",
                                      'DEACONU Mihai': "IND",
                                      'SAGHIAN Gheorghe': "IND",
                                      'DIACONU Mihai Bogdan': "IND",
                                      'TĂTARU Dan': "IND",
                                      'DRĂGUŞANU Vasile Cătălin': "PNL",
                                      'STOICA Ştefan': "IND",
                                      'STOICA Mihaela': "PSD",
                                      'FRĂTICIU Gheorghe': "IND",
                                      'TOCUŢ Dan Laurenţiu': "ALDE",
                                      'CĂTĂNICIU Steluţa Gustica': "ALDE",
                                      'ARITON Ion': "PNL",
                                      'NEGRUŢ Clement': "IND",
                                      'VOSGANIAN Varujan': "ALDE",
                                      'UDREA Elena Gabriela': "IND",
                                      'IONIŢĂ Dan Aurel': "PSD",
                                      'CALOTĂ Florică Ică': "ALDE",
                                      'PETRESCU Petre': "IND",
                                      'OAJDEA Daniel Vasile': "IND",
                                      'GAVRILESCU Graţiela Leocadia': "ALDE",
                                      'POPESCU TĂRICEANU Călin Constantin Anton': "ALDE",
                                      'TEJU Sorin': "ALDE",
                                      'ENACHE Marian': "IND",
                                      'BOT Octavian': "ALDE",
                                      'BURLACU Ştefan': "UNPR",
                                      'PALAŞCĂ Viorel': "ALDE",
                                      'HARBUZ Liviu': "IND",
                                      'GUNIA Dragoş Ionel': "IND",
                                      'DUMITRU Ovidiu Ioan': "IND",
                                      'GURZĂU Adrian': "IND",
                                      'MOVILĂ Petru': "IND",
                                      'POPESCU Florin Aurelian': "IND",
                                      'COMŞA Cornel George': "IND",
                                      'SAVU Daniel': "IND",
                                      'AXENTE Ioan': "IND",
                                      'MOCANU Adrian': "IND",
                                      'URSĂRESCU Dorinel': "ALDE",
                                      'KHRAIBANI Camelia': "IND",
                                      'ILIEŞIU Sorin': "PSD",
                                      'POPESCU Dumitru Dian': "ALDE",
                                      },
                        "2016-2020": {'PETREA Gabriel': "PRO",
                                      'BOGACIU Alexandra Corina': "PRO",
                                      'POPA Ion': "ALDE",
                                      'BODEA Marius': "IND",
                                      'SAVIN Emanoil': "PSD",
                                      'GIOANCĂ Eugen': "PNL",
                                      'MELEŞCANU Teodor Viorel': "PSD",
                                      'BURCIU Cristina': "PNL",
                                      'DRĂGHICI Mircea Gheorghe': "IND",
                                      'SIBINESCU Ionuţ': "PSD",
                                      'NIŢĂ Mihai': "PRO",
                                      'MOCIOALCĂ Ion': "PRO",
                                      'CALOTĂ Florică Ică': "PNL",
                                      'GANEA Ion': "PSD",
                                      'POP Georgian': "PRO",
                                      'STANCU Florinel': "PRO",
                                      'MEIROŞU Marilena Emilia': "IND",
                                      'TUDOSE Mihai': "PRO",
                                      'HUNCĂ Mihaela': "PRO",
                                      'BĂDULESCU Dorin Valeriu': "ALDE",
                                      'MARICA Petru Sorin': "PRO",
                                      'NECHIFOR Cătălin Ioan': "IND",
                                      'CÎMPEANU Sorin Mihai': "IND",
                                      'DOBROVIE Matei Adrian': "PNL",
                                      'JIVAN Luminiţa Maria': "IND",
                                      'BOTNARIU Emanuel Gabriel': "IND",
                                      'MIREA Siminica': "PSD",
                                      'BORZA Remus Adrian': "PSD",
                                      'RĂDULESCU Dan Răzvan': "IND",
                                      'IRIZA Scarlat': "PSD",
                                      'TEIŞ Alina': "PRO",
                                      'PODAŞCĂ Gabriela Maria': "IND",
                                      'CUCŞA Marian Gheorghe': "PSD",
                                      'SITTERLI Ovidiu Ioan': "IND",
                                      'ANDREI Alexandru Ioan': "PNL",
                                      'ZAMFIR Daniel Cătălin': "ALDE",
                                      'MOHACI Mihai': "PSD",
                                      'IFTIMIE Neculai': "IND",
                                      'PETCU Toma Florin': "PNL",
                                      'CONSTANTIN Daniel': "IND",
                                      'BIRCHALL Ana': "IND",
                                      'NICOARĂ Marius Petre': "ALDE",
                                      'VĂCARU Alin Vasile': "IND",
                                      'DOBRE Mircea Titus': "IND",
                                      'SURGENT Marius Gheorghe': "PNL",
                                      'PETRIC Octavian': "PRO",
                                      'BĂNICIOIU Nicolae': "IND",
                                      'HĂRĂTĂU Elena': "PNL",
                                      'GĂINĂ Mihăiţă': "PNL",
                                      'PONTA Victor Viorel': "IND",
                                      'COSMA Lavinia Corina': "IND",
                                      'NIŢĂ Ilie': "PSD",
                                      'BANIAS Mircea Marius': "IND",
                                      'HAVRICI Emanuel Iuliu': "PRO",
                                      'DOHOTARU Adrian Octavian': "IND",
                                      'POPA Mihai Valentin': "PRO",
                                      'BÎZGAN GAYRAL Oana Mioara': "IND",
                                      'VLĂDUCĂ Oana Silvia': "PRO",
                                      'TALPOŞ Ioan Iustin': "PSD",
                                      'BĂLĂNESCU Alexandru': "PRO",
                                      'SPÂNU Ion': "PRO",
                                      'PAU Radu Adrian': "PRO",
                                      }
                        }
