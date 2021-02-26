# Cohesion

The cohesion criterion is defined by [1] as the way to organize the different passages of text (here tweets) in a way that is efficient for the reader. Cohesion can be expressed, among others, in terms of topic-cohesion or time line ordering.

First, we evaluated the time line cohesion of our candidate gold standard (CGS) by comparing their chronological ordering with the chronological order of the sub-events in the Wikipedia portal. For this purpose, we created two lists. The first lists tweets in chronological order using their timestamp. The second lists tweets using the sub-event chronological order.  For this second list, each tweet should be associated to only one sub-event, which is not necessarily the case in our annotations. To do so, if the tweet is about the totality of a sub-event, it is associated to this sub-event. If no, the tweet is assigned to the newest sub-event it mentions. The Manhattan distance between the two lists gave a mean difference of 7 for a tweet position. We deeply go inside these results by comparing each triplet of tweets in the lists. In 63% of the cases, the tweet before and/or after a given tweet is the same in both lists. 

Second, the manual checking for coverage allowed to shed some light on topic-cohesion. As previously indicated, 67% of the CGS tweets do not refer to a sub-event reported in the Wikipedia portal. Consequently, topic-cohesion is guaranteed only for the subset comprising the 33% of the CGS tweets that refer to Wikipedia portal sub-events.


Below an example about the 2015 Paris attacks. Here, the 3rd tweet is not about the same topic as the others. The 3rd tweet is about a victim of the attacks whereas the others are all about the attackers. There is also a time-line mismatch between the 2nd and the 4th tweets, we know the possible bomber has been identified before knowing a bomber tried to enter the stadium.

1. RT @nytimesworld: ISIS reportedly claims responsibility for Paris attacks, referring to them as "miracles." https://t.co/5cf9F4J0S1 https:/…
2. Young Frenchman Identified As Possible Bomber In Attack On Bataclan Concert Hall: PARIS (AP) — Two French poli... https://t.co/qPlHNVawa3
3. [BBC News] VIDEO: Paris attack survivor: 'It was a bloodbath' https://t.co/eqs6HTrHz4 https://t.co/601PDL265R
4. RT @BrookingsFP: Paris Attacks: Suicide bomber tried to enter stadium, but was blocked by a French security guard. https://t.co/7gzJUXRdKm …
5. RT @PatVPeters: Possible link between Germany arrest and Paris attacks: senior official https://t.co/h9zflOIAgW


[1] Goldstein, J., Mittal, V., Carbonell, J., and Kantrowitz, M. (2000). Multi-documentsummarization by sentence extraction.   InNAACL-ANLP Workshop on AutomaticSummarization - Volume 4, NAACL-ANLP-AutoSum ’00, pages 40–48.