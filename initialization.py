import json
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
from pandas.io.json import json_normalize
import os
import time
import re
import html
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from rouge.rouge import rouge_n_sentence_level
import argparse
import string

# You have to follow instructions here : http://dcs.gla.ac.uk/~richardm/TREC_IS/2020/data.html (if no changes)
# and download 'trecis2018-test', 'trecis2018-train', 'trecis2019-A-test' and 'trecis2019-B-test' sets'

# Map TREC IS annotators event labels to event label
d_map = {'costaRicaEarthquake2012':'costaRicaEarthquake2012',
		'fireColorado2012':'fireColorado2012',
		'floodColorado2013':'floodColorado2013',
		'typhoonPablo2012':'typhoonPablo2012',
		'laAirportShooting2013':'laAirportShooting2013',
		'westTexasExplosion2013':'westTexasExplosion2013',
		'guatemalaEarthquake2012':'guatemalaEarthquake2012',
		'bostonBombings2013':'bostonBombings2013',
		'flSchoolShooting2018':'flSchoolShooting2018',
		'chileEarthquake2014':'chileEarthquake2014',
		'joplinTornado2011':'joplinTornado2011',
		'typhoonYolanda2013':'typhoonYolanda2013',
		'queenslandFloods2013':'queenslandFloods2013',
		'nepalEarthquake2015S3':'nepalEarthquake2015',
		'nepalEarthquake2015':'nepalEarthquake2015',
		'australiaBushfire2013':'australiaBushfire2013',
		'philipinnesFloods2012':'philipinnesFloods2012',
		'albertaFloods2013':'albertaFloods2013',
		'nepalEarthquake2015S2':'nepalEarthquake2015',
		'typhoonHagupit2014S2':'typhoonHagupit2014',
		'manilaFloods2013':'manilaFloods2013',
		'parisAttacks2015':'parisAttacks2015',
		'italyEarthquakes2012':'italyEarthquakes2012',
		'typhoonHagupit2014':'typhoonHagupit2014',
		'typhoonHagupit2014S1':'typhoonHagupit2014',
		'nepalEarthquake2015S4':'nepalEarthquake2015',
		'nepalEarthquake2015S1':'nepalEarthquake2015',
		'floodChoco2019':'floodChoco2019',
		'earthquakeCalifornia2014':'earthquakeCalifornia2014',
		'shootingDallas2017A':'shootingDallas2017',
		'earthquakeBohol2013':'earthquakeBohol2013',
		'fireYMM2016E':'fireYMM2016',
		'shootingDallas2017E':'shootingDallas2017',
		'hurricaneFlorence2018A':'hurricaneFlorence2018',
		'hurricaneFlorence2018B':'hurricaneFlorence2018',
		'fireYMM2016A':'fireYMM2016',
		'hurricaneFlorence2018C':'hurricaneFlorence2018',
		'hurricaneFlorence2018D':'hurricaneFlorence2018',
		'fireYMM2016B':'fireYMM2016',
		'shootingDallas2017B':'shootingDallas2017',
		'shootingDallas2017C':'shootingDallas2017',
		'fireYMM2016D':'fireYMM2016',
		'philippinesEarthquake2019A':'philippinesEarthquake2019',
		'philippinesEarthquake2019C':'philippinesEarthquake2019',
		'philippinesEarthquake2019B':'philippinesEarthquake2019',
		'southAfricaFloods2019C':'southAfricaFloods2019',
		'cycloneKenneth2019B':'cycloneKenneth2019',
		'albertaWildfires2019A':'albertaWildfires2019',
		'albertaWildfires2019B':'albertaWildfires2019',
		'coloradoStemShooting2019A':'coloradoStemShooting2019',
		'coloradoStemShooting2019C':'coloradoStemShooting2019',
		'coloradoStemShooting2019B':'coloradoStemShooting2019',
		'cycloneKenneth2019A':'cycloneKenneth2019',
		'southAfricaFloods2019A':'southAfricaFloods2019',
		'cycloneKenneth2019C':'cycloneKenneth2019',
		'southAfricaFloods2019B':'southAfricaFloods2019',
		'philippinesEarthquake2019D':'philippinesEarthquake2019',
		'sandiegoSynagogueShooting2019A':'sandiegoSynagogueShooting2019',
		'sandiegoSynagogueShooting2019C':'sandiegoSynagogueShooting2019',
		'sandiegoSynagogueShooting2019B':'sandiegoSynagogueShooting2019',
		'albertaWildfires2019C':'albertaWildfires2019',
		'albertaWildfires2019D':'albertaWildfires2019',
		'cycloneKenneth2019D':'cycloneKenneth2019',
# Labels below are not taking into account in our paper, we did not have them at the time we wrote it 
		'fireYMM2016C':'fireYMM2016',
		'shootingDallas2017D':'shootingDallas2017'}

tweet_id_map = {}

PATH_json = "./TREC IS annotations/TRECIS_2018_2019-labels.json"
PATH_tweets = "./Tweets/"

"""
---------------------------------------------------------------------------------------------
Association tweets-annotations
---------------------------------------------------------------------------------------------
"""

with open(PATH_json, "r",encoding='ISO-8859-1') as file:
	tweets = json.load(file)
	for tweet in tweets:
		if tweet["eventID"] != 'fireYMM2016C' and tweet["eventID"] != 'shootingDallas2017D':
			tweet_id_map[tweet["postID"]]={}
			tweet_id_map[tweet["postID"]]["categories"]=tweet["postCategories"]
			tweet_id_map[tweet["postID"]]["priority"]=tweet["postPriority"]
			tweet_id_map[tweet["postID"]]["event"]=d_map[tweet["eventID"]]

l_encoding = ["albertaWildfires2019","coloradoStemShooting2019","cycloneKenneth2019","earthquakeBohol2013","fireYMM2016",
"joplinTornado2011","manilaFloods2013","philippinesEarthquake2019","sandiegoSynagogueShooting2019",
"shootingDallas2017","southAfricaFloods2019"]

for files in tqdm(os.listdir(PATH_tweets)):
	if not files.startswith('.'):
		with open(PATH_tweets+files, "r",encoding='UTF-8') as file:
			for line in file:
				tweet = json.loads(line)
				if tweet["allProperties"]["id"] in tweet_id_map:
					tweet_id_map[tweet["allProperties"]["id"]]["text"] = tweet["allProperties"]["text"]
					src = json.loads(tweet["allProperties"]["srcjson"])
					if "created_at" in src:
						if "+0000" in src["created_at"]:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
						else:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["created_at"],'%b %d, %Y %H:%M:%S %p'))
					else:
						if "+0000" in src["createdAt"]:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["createdAt"],'%a %b %d %H:%M:%S +0000 %Y'))
						else:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["createdAt"],'%b %d, %Y %H:%M:%S %p'))
					if "user.id_str" in tweet["allProperties"]:
						tweet_id_map[tweet["allProperties"]["id"]]["user_id_str"] = tweet["allProperties"]["user.id_str"]
					else:
						tweet_id_map[tweet["allProperties"]["id"]]["user_id_str"] = tweet["allProperties"]["user.id"]

tweet_id_json = []
for i in tweet_id_map:
	tweet_id_json.append(dict(id=i,content=dict(tweet_id_map[i])))

df = pd.DataFrame.from_dict(json_normalize(tweet_id_json), orient='columns')

# The tweets ids were reported High Priority or News by one of the TREC assessor in the first version of the data gave by TREC
l_ids_other_assessor = ['1040371051706953728','1041619713078571008','1040360701586489344',
'1040599786125185024','1040614324681826305','1040205012117479424','1040622759368421376','1041401444669288448','1039920284827086848']

stemmer = nltk.stem.porter.PorterStemmer()
stop_words = set(stopwords.words('english')) 

def high_priority(priority,ids):
	if priority in ["High","Critical"] or ids in l_ids_other_assessor:
		return True
	return False

def news(categories,ids):
	for i in categories:
		if i=="ContinuingNews" or i=="News":
			return True
	if ids in l_ids_other_assessor:
		return True
	return False


def cleanRaw(x):
	x=' '.join(x.split())
	x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
	x=html.unescape(x)
	x=' '.join(x.split())
	return x

def clean(x):
	x=' '.join(x.split())
	x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
	x=html.unescape(x)
	x=re.sub(r'http\S+','',x, flags=re.MULTILINE)
	# to remove links that start with HTTP/HTTPS in the tweet
	x=re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)','',x, flags=re.MULTILINE) 
	# to remove other url links
	x=re.sub(r"@(\w+)", '',x, flags=re.MULTILINE)
	x=' '.join(x.split())
	return x

def cleanPreProcessed(x):
	text = ''
	x=' '.join(x.split())
	x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
	x=html.unescape(x)
	punctuation = string.punctuation
	for y in x.split():
		if y.lower()!='rt' and y.lower()!='mt' and y.startswith('#')==False and y.startswith('@')==False and y.lower().startswith('http:')==False and y.lower().startswith('https:')==False and y not in punctuation and y.startswith('!')==False and y.startswith('.')==False and y.startswith('?')==False and y.lower() not in stop_words:
			text+=' '+ stemmer.stem(y)
	return text

def _surrogatepair(match):
	char = match.group()
	assert ord(char) > 0xffff
	encoded = char.encode('UTF-8')
	return (
		chr(int.from_bytes(encoded[:2], 'little')) + 
		chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
	return _nonbmp.sub(_surrogatepair, text)

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')
# _nonbmp = re.compile(r'[\U0800-\UFFFF]'))


# Order tweets with twin timestamps
l_twin_timestamp_order = [["665284743156637696","665284742686773248"],
["727629011728224256","727629009207463937"],
["727630033846603776","727630033288712192"],
["1121111562779938816","1121111562704437248"],
["1121111567594950656","1121111566324101120"],
["1121111566324101120","1111567943327744"],
["1122228237365587970","1122228235658518531"],
["1125882096403320833","1125882096877281280"]]

"""
Add tweets to cover all needed subevents
"""
parser = argparse.ArgumentParser()
parser.add_argument("-remove_coverage", default=False, type=bool)
args = parser.parse_args()

l_tweets_subevents = ['390389747950309376','389917091823763456',
'233012889387147265',
'232919062806675456',
'233148805846011904',
'324340772008763394',
'451295348175011840']

# if not args.remove_coverage:
# 	l_ids_other_assessor.extend(l_tweets_subevents)

def timestamp_ordering(df,list_timestamp):
	l_df_order = []
	for i in df["id"]:
		if i in list_timestamp:
			l_df_order.append(i)
	if list_timestamp[0]!=l_df_order[0]:
		l1 = list(df.index[df["id"]==list_timestamp[0]])[0]
		l2 = list(df.index[df["id"]==list_timestamp[1]])[0]
		temp = df.loc[l1].copy()
		df.loc[l1] = df.loc[l2]
		df.loc[l2] = temp
	return df

"""
Create events file with all tweets
"""

for i in df["content.event"].unique():
	if os.path.exists('./Sets/All tweets/Raw/'+i+'.txt'):
		os.remove('./Sets/All tweets/Raw/'+i+'.txt')
	for j in df[df["content.event"]==i]["content.text"]:
		with open('./Sets/All tweets/Raw/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanRaw(j))+'\n')

for i in df["content.event"].unique():
	if os.path.exists('./Sets/All tweets/PreProcessed/'+i+'.txt'):
		os.remove('./Sets/All tweets/PreProcessed/'+i+'.txt')
	for j in df[df["content.event"]==i]["content.text"]:
		with open('./Sets/All tweets/PreProcessed/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanPreProcessed(j))+'\n')

df_summary = df[df.apply(lambda x: high_priority(x["content.priority"],x["id"]),axis=1)]
df_summary = df_summary[df_summary.apply(lambda x: news(x["content.categories"],x["id"]),axis=1)]
df_summary["content.timestamp"] = pd.to_datetime(df_summary["content.timestamp"])
df_summary = df_summary.sort_values(by=["content.timestamp"])
for i in l_twin_timestamp_order:
	df_summary = timestamp_ordering(df_summary,i)

"""
Create NHP events file with News High Priority tweets
"""

for i in df_summary["content.event"].unique():
	if os.path.exists('./Sets/NHP/Raw/'+i+'.txt'):
		os.remove('./Sets/NHP/Raw/'+i+'.txt')
	for j in df_summary[df_summary["content.event"]==i]["content.text"]:
		with open('./Sets/NHP/Raw/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanRaw(j))+'\n')

for i in df_summary["content.event"].unique():
	if os.path.exists('./Sets/NHP/PreProcessed/'+i+'.txt'):
		os.remove('./Sets/NHP/PreProcessed/'+i+'.txt')
	for j in df_summary[df_summary["content.event"]==i]["content.text"]:
		with open('./Sets/NHP/PreProcessed/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanPreProcessed(j))+'\n')

"""
Create events file for the tool PKUSUMSUM
"""

df_pku = df.sort_values(by=["content.timestamp"])
for i in l_twin_timestamp_order:
	df_pku = timestamp_ordering(df_pku,i)

for i in df_summary["content.event"].unique():
	cpt=1
	for j in df_pku[df_pku["content.event"]==i]["content.text"]:
		if os.path.exists('./Sets/PKUSet/'+i+'/'+str(cpt)+'.txt'):
			os.remove('./Sets/PKUSet/'+i+'/'+str(cpt)+'.txt')
		with open('./Sets/PKUSet/'+i+'/'+str(cpt)+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanPreProcessed(j))+'<END_OF_TWEET>')
		cpt+=1

"""
Create events file with all tweets and with tweets ids, user ids and timestamps
"""

for i in df_pku["content.event"].unique():
	if os.path.exists('./Sets/Tweets with ids/'+i+'.txt'):
		os.remove('./Sets/Tweets with ids/'+i+'.txt')
	l_ids = []
	l_uids = []
	l_timestamp = []
	for j in df_pku[df_pku["content.event"]==i]["id"]:
		l_ids.append(j)
	for j in df_pku[df_pku["content.event"]==i]["content.user_id_str"]:
		l_uids.append(j)
	for j in df_pku[df_pku["content.event"]==i]["content.timestamp"]:
		l_timestamp.append(j)
	cpt=0
	for j in df_pku[df_pku["content.event"]==i]["content.text"]:
		with open('./Sets/Tweets with ids/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(l_timestamp[cpt]+'\t'+l_ids[cpt]+'\t'+l_uids[cpt]+'\t'+with_surrogates(cleanPreProcessed(j))+'\n')
		cpt+=1

"""
Generate randoms summaries as in the paper
"""

number_tweets_per_event = [17,1,15,4,13,52,43,20,117,3,18,6,8,159,52,161,111,17,22,36,72,50,62,90,15,12]
event_list = ["joplinTornado2011","costaRicaEarthquake2012","guatemalaEarthquake2012",
                    "philipinnesFloods2012","italyEarthquakes2012","bostonBombings2013","typhoonYolanda2013",
                    "australiaBushfire2013","queenslandFloods2013","earthquakeBohol2013","albertaFloods2013",
                    "manilaFloods2013","chileEarthquake2014","typhoonHagupit2014","parisAttacks2015",
                    "nepalEarthquake2015","fireYMM2016","shootingDallas2017","flSchoolShooting2018",
                    "hurricaneFlorence2018","philippinesEarthquake2019","southAfricaFloods2019",
                    "cycloneKenneth2019","albertaWildfires2019","coloradoStemShooting2019",
                    "sandiegoSynagogueShooting2019"]
for i in tqdm(range(1,51)):
    cpt=0
    df_randoms = pd.DataFrame()
    for j in event_list:
        df_randoms = df_randoms.append(df[df["content.event"]==j].sample(n=number_tweets_per_event[cpt], random_state=i))
        cpt+=1
    for k in df_randoms["content.event"].unique():
        if os.path.exists('./Reproduce results/Models Summarization/'+str(i)+'/'+k+'.txt'):
            os.remove('./Reproduce results/Models Summarization/'+str(i)+'/'+k+'.txt')
        if os.path.exists('./Sets/Random Summaries Raw/'+str(i)+'/'+k+'.txt'):
            os.remove('./Sets/Random Summaries Raw/'+str(i)+'/'+k+'.txt')
        for l in df_randoms[df_randoms["content.event"]==k]["content.text"]:
            with open('./Reproduce results/Models Summarization/'+str(i)+'/'+k+'.txt','a',encoding='utf-8') as file:
                file.write(with_surrogates(cleanPreProcessed(l))+'\n')
            with open('./Sets/Random Summaries Raw/'+str(i)+'/'+k+'.txt','a',encoding='utf-8') as file:
                file.write(with_surrogates(cleanRaw(l))+'\n')

df_summary.to_csv("./Reproduce results/Redundancy/df.csv",index=False)

"""
---------------------------------------------------------------------------------------------
Redundancy reproductibility files initialization
---------------------------------------------------------------------------------------------
"""

df2_event = {}
for i in df_summary["content.event"].unique():
	df2_event[i] = []
    
for i in range(len(df_summary["content.event"])):
	df2_event[df_summary["content.event"].iloc[i]].append((df_summary.index[i],clean(df_summary["content.text"].iloc[i])))

d_scores = {}
for i in df2_event:
	d_scores[i]=[]
    
delete_pair_max = []
delete_pair = []
            
cpt=0  
for i in df2_event:
	cpt=0
	while cpt < len(df2_event[i]):
		l_rouge_score = []
		l_rouge_score_max = []
		for k in range(0,cpt):
			if k != cpt:
				*_,rouge = rouge_n_sentence_level(df2_event[i][k][1].split(),df2_event[i][cpt][1].split(),2)
				l_rouge_score.append(rouge)
				l_rouge_score_max.append((rouge,df2_event[i][k][1],df2_event[i][cpt][1]))
				if rouge >= 0.3:
					delete_pair.append((df2_event[i][k][1],df2_event[i][cpt][1]))
		if l_rouge_score:
			if max(l_rouge_score) >= 0.3:
				delete_pair_max.append((max(l_rouge_score_max)[1],max(l_rouge_score_max)[2]))
				df2_event[i].pop(cpt)
				cpt-=1
		cpt+=1

set_resume = set()
for i in df2_event:
    for j in df2_event[i]:
        set_resume.add(j[0])
set_all = set(df_summary.index)

df2 = df_summary.drop(set_all-set_resume)


df2.to_csv("./Reproduce results/Redundancy/input.txt", index=False)
df2["vu"] = False
df2["new"] = False
df2.to_csv("./Reproduce results/Redundancy/output.txt",index=False)

"""
---------------------------------------------------------------------------------------------
Generate summaries with redundancy annotations: NHPAR
---------------------------------------------------------------------------------------------
"""

df_redundancy = pd.read_csv("./Paper annotations/annotations_redundancy.txt")
l_redundancy = df_redundancy[df_redundancy["new"]==True]["id"]
s_redundancy = set()
for i in l_redundancy:
	s_redundancy.add(str(i))
if not args.remove_coverage:
	for i in l_tweets_subevents:
		s_redundancy.add(str(i))
df3 = df
df3 = df3.sort_values(by=["content.timestamp"])
for i in l_twin_timestamp_order:
	df3 = timestamp_ordering(df3,i)
df3 = df3[df3["id"].apply(lambda x: True if x in s_redundancy else False)]
for i in df3["content.event"].unique():
	if os.path.exists('./Sets/NHPAR/Raw/'+i+'.txt'):
		os.remove('./Sets/NHPAR/Raw/'+i+'.txt')
	for j in df3[df3["content.event"]==i]["content.text"]:
		with open('./Sets/NHPAR/Raw/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanRaw(j))+'\n')

for i in df3["content.event"].unique():
	if os.path.exists('./Sets/NHPAR/PreProcessed/'+i+'.txt'):
		os.remove('./Sets/NHPAR/PreProcessed/'+i+'.txt')
	for j in df3[df3["content.event"]==i]["content.text"]:
		with open('./Sets/NHPAR/PreProcessed/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanPreProcessed(j))+'\n')

"""
---------------------------------------------------------------------------------------------
Generate summaries with SubEvents WikiPortal annotations
---------------------------------------------------------------------------------------------
"""

l_coverage = []
df_coverage = pd.read_csv("./Reproduce results/Coverage/verification.txt")
for i in df_coverage["id"]:
	l_coverage.append(df_summary[df_summary["id"]==str(i)]["content.text"].iloc[0])
df_coverage["content.text"] = l_coverage
df_coverage.to_csv("./Reproduce results/Coverage/verification.txt",index=False)
