# Coherence

The coherence criterion is defined by [1] as the ability for a summary to be relevant and readable to the reader. On the one hand, the relevance is induced by the annotations of the TREC IS task. On the other hand, we evaluated readability with state-of-the-art metrics. These metrics are Flesch-Kincaid [2], Gunning-Fog [3], Coleman-Liau [4], Dale-Chall [5], Automatic readability index (Ari) [6], Linsear write [7], and Spache [8]. The features used by these metrics focus on number of words, number of characters, number of syllables, and number of difficult words. We used the U.S. grade score obtained by these metrics with the library [py-readability-metrics](https://pypi.org/project/py-readability-metrics) in our readability evaluation. We performed the evaluation of the entire dataset and the candidate gold standard (CGS) for each event whose CGS contains more than 100 words, which affects the events ''earthquakeBohol2013'', ''costaRicaEarthquake2012'', ''philipinnesFloods2012'', ''manilaFloods2013'' that do not contain 100 words. The results for the Gunning-Fog, Ari, Linsear write and Spache metrics were highly correlated to Flesch-Kincaid (Pearson correlations, r > 0.85, p-value<0.01).

We can observe that the readability scores are, except for the event ''italyEarthquake2012'', between the 7th grade and the college graduate grade (college grade is greater than 12 and college graduate grade is greater than college grade). We can also notice that readability scores are greater for CGS than when considering all tweets per event in most cases (80%). However, except for the Coleman-Liau metric, the difference is not significant (Student t-test, without the outlier ''italyEarthquake'', p-value<0.05). The Coleman-Liau measure takes into account the number of words in sentences and the number of characters in words. Indeed, the average length of words in terms of characters is 4.6 for the entire TREC IS dataset and 4.8 for the CGS, and the average length of sentences in terms of words is 13.0 for the entire TREC IS dataset and 14.0 for the CGS. We think that these reserved results are due to the technical aspect of the tweets labeled News and High Priority.
We hypothesize that an explanation for this difference comes from higher priority tweets. These tweets are supposed to return an alert and be processed in less than 30 minutes by the operators. This involves detailed information, complex words... We therefore assessed readability for all tweets of high or critical priority, on the one hand, and for random summaries of tweets (50 summaries) of the same size, of lower priority, in chronological order on the other hand, per event. The results show that in 77% of the cases the readability of tweets with a higher priority is worse than the readability of tweets with a lower priority. Also, the Coleman-Liau metric difference is still significant (Student t-test, without the outlier ''italyEarthquake'', p-value<0.05). The difference in readability scores can therefore be explained, at least in part, by the presence of high-priority tweets in our CGSs.


An example of tweet readability below, from the 2012 Guatemala Earthquake event, the tweets with **IN** are in the summary, the others not. We can see that the tweets in the summary are less easy to read than the others but give more information.

**IN** Strong tremor felt in Guatemala City, El Salvador: GUATEMALA CITY (Reuters) - A strong earthquake shook building... http://t.co/UMauuZrS  
RT @cnnbrk: USGS: 7.5-magnitude earthquake strikes off #Guatemala http://t.co/N2BohJRd  
RT @BreakingNews: Magnitude 7.3 earthquake hits off Guatemala's Pacific coast, USGS reports - @Reuters  
RT @djfxtrader: Magnitude 7.5 Quake Hits Off Guatemala's Pacific Coast -USGS  
Watching the news when the earthquake alarm went off. 7.3 along the border with Guatemala from what I know.  
**IN** RT @NewEarthquake: Revised (7.5 -> 7.4): 7.4 earthquake, 24km S of Champerico, Guatemala. Nov 7 10:35 at epicenter (20m ago, depth 42 ...


[1] Goldstein, J., Mittal, V., Carbonell, J., and Kantrowitz, M. (2000). Multi-documentsummarization by sentence extraction.   InNAACL-ANLP Workshop on AutomaticSummarization - Volume 4, NAACL-ANLP-AutoSum ’00, pages 40–48.

[2] Kincaid, J. (1975).Derivation of New Readability Formulas: (automated ReadabilityIndex, Fog Count and Flesch Reading Ease Formula) for Navy Enlisted Personnel. ResearchBranch report. Chief of Naval Technical Training, Naval Air Station Memphis.

[3] Gunning, R. (1968).The technique of clear writing. McGraw-Hill.

[4] Coleman, M. and Liau, T. L. (1975). A computer readability formula designed formachine scoring.Journal of Applied Psychology, 60:283–284.

[5] Dale, E. and Chall, J. S. (1948).  A formula for predicting readability.EducationalResearch Bulletin, 27(1):11–28.

[6] Smith, E., Senter, R., and (U.S.), A. F. A. M. R. L. (1967).Automated ReadabilityIndex. AMRL-TR. Aerospace Medical Research Laboratories.

[7] Klare, G. R. (1974). Assessing readability.Reading Research Quarterly, 10(1):62–102.

[8] Spache, G. (1953). A new readability formula for primary-grade reading materials.The Elementary School Journal, 53(7):410–413.