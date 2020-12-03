import pandas as pd
import pickle
from pandas.io.json import json_normalize
import numpy as np
import os
from scipy.spatial import distance

PATH_annotated_tweets = "../../Paper annotations/annotations_coverage.txt"
PATH_subevents = "../Coverage/subevent_date.pkl"

df_tweets = pd.read_csv(PATH_annotated_tweets)
map_subevent_date = pickle.load( open( PATH_subevents, "rb" ) )


df = pd.DataFrame.from_dict(json_normalize(map_subevent_date), orient='columns')
df = df.T
df.columns = ["timestamp"]
df = df.sort_values(by=["timestamp"],ascending=False)

# print(df)

# Arrange tweets in chronological order using subevents

map_tweet_whole = {}
for i in range(len(df_tweets["id"])):
	map_tweet_whole[df_tweets["id"][i]] = df_tweets["TheWhole"][i]
map_tweet_partly = {}
for i in range(len(df_tweets["id"])):
	map_tweet_partly[df_tweets["id"][i]] = df_tweets["Partly"][i]
map_tweet_subevent = {}
for tweets in df_tweets["id"]:
	for i in df.index:
		if str(i) in map_tweet_whole[tweets] and tweets not in map_tweet_subevent:
			map_tweet_subevent[tweets] = str(i)
for tweets in df_tweets["id"]:
	for i in df.index:
		if str(i) in map_tweet_partly[tweets] and tweets not in map_tweet_subevent:
			map_tweet_subevent[tweets] = str(i)

# print(map_tweet_subevent)
# print(len(map_tweet_subevent))

df = df.sort_values(by=["timestamp"])

l_tweets_subevents = []
for i in df.index:
	for tweets in df_tweets["id"]:
		if tweets in map_tweet_subevent:
			if map_tweet_subevent[tweets]==str(i):
				l_tweets_subevents.append(tweets)

d_tweets_subevents = {}
cpt = 0
for i in l_tweets_subevents:
	d_tweets_subevents[i] = cpt
	cpt+=1

l_df_tweets_ids = []
for i in list(df_tweets["id"]):
	if i in l_tweets_subevents:
		l_df_tweets_ids.append(d_tweets_subevents[i])

l_tweets_subevents2 = []
for i in l_tweets_subevents:
	l_tweets_subevents2.append(d_tweets_subevents[i])
# l_tweets_subevents2.reverse()
# print(l_tweets_subevents2)
# print(l_df_tweets_ids)

print("Number of tweets compared :" + str(len(l_tweets_subevents2)))

print("Manhattan distance :" + str(distance.cityblock(l_tweets_subevents2, l_df_tweets_ids)/len(l_tweets_subevents2)))

# print(l_tweets_subevents2)
# print(l_df_tweets_ids)

nb_neighbors = 0
nb_good_neighbors = 0
for i in range(len(l_tweets_subevents2)):
	if i==0:
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])+1] == l_tweets_subevents2[i+1]:
			nb_good_neighbors+=1
		nb_neighbors+=1
	elif i==len(l_tweets_subevents2)-1:
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])-1] == l_tweets_subevents2[i-1]:
			nb_good_neighbors+=1
		nb_neighbors+=1
	elif l_df_tweets_ids.index(l_tweets_subevents2[i])==0:
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])+1] == l_tweets_subevents2[i+1]:
			nb_good_neighbors+=1
		nb_neighbors+=1
	elif l_df_tweets_ids.index(l_tweets_subevents2[i])==len(l_tweets_subevents2)-1:
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])-1] == l_tweets_subevents2[i-1]:
			nb_good_neighbors+=1
		nb_neighbors+=1
	else:
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])+1] == l_tweets_subevents2[i+1]:
			nb_good_neighbors+=1
		if l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])-1] == l_tweets_subevents2[i-1]:
			nb_good_neighbors+=1
		# nb_good_neighbors+=len({l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])+1],
		# 	l_df_tweets_ids[l_df_tweets_ids.index(l_tweets_subevents2[i])-1]}.intersection({l_tweets_subevents2[i-1],l_tweets_subevents2[i+1]}))
		nb_neighbors+=2

print("Number of neighbors : " + str(nb_neighbors))
print("Number of good neighbors : " + str(nb_good_neighbors))
print("Rate : " + str(nb_good_neighbors/nb_neighbors))


"""
For tweets assessed to subevents, we compared the chronological order and the subevents chronological order.
We created two lists. The first lists tweets in chronological order using the tweet timestamp. The second lists tweets using the
subevent chronological order. A tweet is assigned to the older subevent it mentionned, priorizing subevent it whole mentionned.
The Manhattan distance between the two lists gave a means difference of 7 for the right position of a tweet.
We also compared the differences between the surrounding tweets, the previous and the next one.
Only 63% of the cases were right in place.
"""