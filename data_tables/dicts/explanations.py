"""

### ON PARTY SWITCHING ###

relates esp. to dict in destination_dict.py

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
with wider knowledge of the scene needs to look at the history of caucus switching and decide which party was
actually the destination party. I do not think that in a reasonable amount of time I could train a computer to replicate
my own knowledge of Romanian parliamentary switching dynamics. Note that this go-betweening minimally affects those who
formally join another party as members, since that's a much louder and clearer message: it wouldn't make sense to delay
caucuses affiliation while immediately registering in the destination party.

Finally, the same PPG might change names and/or formal identity several times in one legislature, especially those
that form out of splinters/factions from other parties: UNPR and ALDE both experienced this in different legislatures.

"""


"""

### ON PARLIAMENTARY PARTIES ###

relates to reference_dicts.py

NB: not enough variance to see if timing of loss of parliamentary caucus group affects timing of party switch
    --> PUR-SL 2000-2004 always caucased with PSD, never had a PPG to lose
    --> PC (former PUR-SL) in 2008-2012 caucused first with PSD then with PNL, so didn't actually lose a caucus
    --> PC in 2012-2016 caucused on its own then merged with PNL splinter to form ALDE caucus in CDEP,
        always had its caucus in senate; either way, never lost a caucus
    --> PP-DD lost its caucuses in summer 2015: in Senat (July) and CDEP (August). Party leader Dan Diaconescu had
        been sent to jail several months prior, in March 2015
    --> PMP lost Senate caucus in June 2018, but kepy CDEP caucus
    --> ALDE lost both CDEP and Senat caucuses in September 2019
"""