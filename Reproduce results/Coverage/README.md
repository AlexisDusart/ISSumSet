# Coverage

Regarding coverage, we hypothesized that it is intrinsic to the original TREC IS collection construction. Indeed, important news (i.e., high or critical ones) from the original dataset are kept to build our candidate gold standard (CGS) summaries.
To support this hypothesis we analysed the CGS with respect to the sub-events associated to our events reported in the [Wikipedia portal Current_events](https://en.wikipedia.org/wiki/Portal:Current_events). This portal daily reports world-wide current events.
For each event, we extracted from the portal the sub-events corresponding to the period covered by the original TREC IS collection. Each event of the TREC IS collection corresponds at least to one sub-event in the portal.  The total number of sub-events is 154 with 6 sub-events per event on average.

Here is an example of the extracted sub-events for the event ``albertaFloods2013''.
* June 20, 2013 (Thursday):
Extensive flooding begins throughout southern Alberta, Canada, leading to the evacuation of more than 100,000 people, notably in the City of Calgary and Town of High River. It would become the costliest natural disaster in Canadian history.

* June 21, 2013 (Friday):
75,000 people are evacuated from their homes during flooding in Calgary, Alberta, Canada. (CNN)

* June 22, 2013 (Saturday):
100,000 residents are displaced on the third day of flooding in Alberta. (CBC)

In an additional step, we compared the sub-events represented in the CGS with the sub-events extracted from the Wikipedia portal. To do so, we made another assessment tool. With this tool, for each pair (CGS tweet, sub-event) we determined if the tweet is related to either the whole sub-event, a part of it, or not at all. Note that a tweet can thus be associated to multiple sub-events. In total, we annotated 6,560 pairs as 'not at all' (92%), 543 pairs as 'partly' (about 7%), and 29 pairs as 'whole' (less than 1%). 67% of the CGS tweets do not refer to any sub-events of the Wiki portal.

Among the 154 sub-events in the Wikipedia portal, 103 are represented in the CGS (about 67%). The 51 sub-events for which there are no tweet references are spread over 10 of the 26 events, which represents one third of the sub-events and affects 38% of the events.

To go further in the coverage analysis, we examined the sub-events that are not represented in the CGS. We searched for the associated keywords in the original tweet collection associated with the event.
36 of 51 sub-events cannot be found at all. For the 15 remaining sub-events, we distinguish two categories : 1) those who are not directly linked to the event (9 sub-events),  2) the others, which should have been mentioned. An example of sub-event in the first group is 'Organisers and security officials reassess security plans for Sunday's 2013 London Marathon.' for the event 'bostonBombings2013, which can be considered as a consequence of the Boston Bombing attack. 

We added the 7 tweets corresponding to the 6 sub-events (one sub-event is expressed in two tweets)  of the second category to the candidate gold standards. This allows us to reach 100% of coverage in the collection, which we call ISSumSet in the paper. At the end of the redundancy and coverage check phases, 1,177 tweets are kept to form the ``new'' CGS summaries, simply referred as CGS. The smallest CGS is now composed of one tweet, while the biggest contains 161 tweets.