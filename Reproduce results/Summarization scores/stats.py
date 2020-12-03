import pandas as pd
import nltk
import numpy as np
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
import operator
from tqdm import tqdm
import os
from scipy.stats import spearmanr
from scipy.stats import pearsonr

l_methods = ["centroid", "clustercmrw", "coverage", "lead", "lexpagerank", "submodular1", "submodular2", "textrank", "COWTS", "SEMCOWTS"]
l_event = ["albertaFloods2013","albertaWildfires2019","australiaBushfire2013","bostonBombings2013","chileEarthquake2014",
 "coloradoStemShooting2019","costaRicaEarthquake2012","cycloneKenneth2019","earthquakeBohol2013","fireYMM2016",
 "flSchoolShooting2018","guatemalaEarthquake2012","hurricaneFlorence2018","italyEarthquakes2012",
 "joplinTornado2011","manilaFloods2013","nepalEarthquake2015","parisAttacks2015","philipinnesFloods2012",
 "philippinesEarthquake2019","queenslandFloods2013","sandiegoSynagogueShooting2019","shootingDallas2017",
 "southAfricaFloods2019","typhoonHagupit2014","typhoonYolanda2013"]

"""
--------------------------------------------------------------------------------------------------
COS scores
--------------------------------------------------------------------------------------------------
"""

df_cos = pd.read_csv("./COS.csv")
df_cos = df_cos.set_index(["id"])
l_mean_random = []
for e in df_cos.index:
	l_mean = []
	for i in range(1,51):
		l_mean.append(df_cos[str(i)][e])
	l_mean_random.append(np.mean(l_mean))
df_cos["mean_random"] = l_mean_random

"""
--------------------------------------------------------------------------------------------------
BLEU scores
--------------------------------------------------------------------------------------------------
"""

df_bleu1 = pd.read_csv("./BLEU-1.csv")
df_bleu1 = df_bleu1.set_index(["id"])
l_mean_random = []
for e in df_bleu1.index:
	l_mean = []
	for i in range(1,51):
		l_mean.append(df_bleu1[str(i)][e])
	l_mean_random.append(np.mean(l_mean))
df_bleu1["mean_random"] = l_mean_random

df_bleu2 = pd.read_csv("./BLEU-2.csv")
df_bleu2 = df_bleu2.set_index(["id"])
l_mean_random = []
for e in df_bleu2.index:
	l_mean = []
	for i in range(1,51):
		l_mean.append(df_bleu2[str(i)][e])
	l_mean_random.append(np.mean(l_mean))
df_bleu2["mean_random"] = l_mean_random

"""
--------------------------------------------------------------------------------------------------
METEOR scores
--------------------------------------------------------------------------------------------------
"""

df_meteor = pd.read_csv("./METEOR.csv")
df_meteor = df_meteor.set_index(["id"])
l_mean_random = []
for e in df_meteor.index:
	l_mean = []
	for i in range(1,51):
		l_mean.append(df_meteor[str(i)][e])
	l_mean_random.append(np.mean(l_mean))
df_meteor["mean_random"] = l_mean_random


"""
--------------------------------------------------------------------------------------------------
ROUGE scores
--------------------------------------------------------------------------------------------------
"""

df_rougescore = pd.read_csv("./ROUGE.txt",header=None)

df_rougescore_filter = df_rougescore[df_rougescore[0].apply(lambda x: True if "Average_F" in x else False)]

l_id = []
l_score = []

for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-2" in x else False)][0]:
    l_id.append(nltk.word_tokenize(i)[0])
    l_score.append(float(nltk.word_tokenize(i)[4]))
    
df_rouge_score = pd.DataFrame()
df_rouge_score["id"] = l_id
df_rouge_score["f_score_rouge2"] = l_score

l_score = []

for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-1" in x else False)][0]:
    l_score.append(float(nltk.word_tokenize(i)[4]))
    
df_rouge_score["f_score_rouge1"] = l_score

l_score = []

for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-SU*" in x else False)][0]:
    l_score.append(float(nltk.word_tokenize(i)[4]))

df_rouge_score["f_score_rougesu"] = l_score

df_rouge_score = df_rouge_score.set_index(["id"])

for i in l_methods:
	print(i,"&",round(df_rouge_score["f_score_rouge2"][i],3),"&",round(df_rouge_score["f_score_rouge1"][i],3),"&",round(df_rouge_score["f_score_rougesu"][i],3),
		"&",round(np.mean(df_cos[i]),3),"&",round(np.mean(df_bleu1[i]),3),"&",round(np.mean(df_bleu2[i]),3),"&",round(np.mean(df_meteor[i]),3))

print("Mean random summaries &",round(np.mean(df_rouge_score["f_score_rouge2"][:-10]),3),"&",round(np.mean(df_rouge_score["f_score_rouge1"][:-10]),3),"&",
	round(np.mean(df_rouge_score["f_score_rougesu"][:-10]),3),"&",round(np.mean(df_cos["mean_random"]),3),"&",round(np.mean(df_bleu1["mean_random"]),3),"&",
		round(np.mean(df_bleu2["mean_random"]),3),"&",round(np.mean(df_meteor["mean_random"]),3))

print("Std random summaries &",round(np.std(df_rouge_score["f_score_rouge2"][:-10]),3),"&",round(np.std(df_rouge_score["f_score_rouge1"][:-10]),3),"&",
	round(np.std(df_rouge_score["f_score_rougesu"][:-10]),3),"&",round(np.std(df_cos["mean_random"]),3),"&",round(np.std(df_bleu1["mean_random"]),3),"&",
		round(np.std(df_bleu2["mean_random"]),3),"&",round(np.std(df_meteor["mean_random"]),3))

#--------------------------------------------------------------------------------------------------

for r in ["ROUGE-1","ROUGE-2","ROUGE-SU"]:
	df_rougescore_filter = df_rougescore[df_rougescore[0].apply(lambda x: True if "Eval" in x else False)]
	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}

	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[6][2:]))
	    
	for i in d_score:
	    df_event_model[i] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('./'+r+'_F.csv')

	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}

	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[5][2:]))
	    
	for i in d_score:
	    df_event_model[i] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('./'+r+'_P.csv')

	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}
	
	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[4][2:]))
	    
	for i in d_score:
	    df_event_model[i] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('./'+r+'_R.csv')




"""
--------------------------------------------------------------------------------------------------
All scores
--------------------------------------------------------------------------------------------------
"""

print("T-tests : If difference is significant, p-value < 0.05 (cell in blue/black for the plots)")

for r in ["ROUGE-2_F","ROUGE-1_F","ROUGE-SU_F","BLEU-1","BLEU-2","METEOR","COS"]:
	df_method = pd.read_csv("./"+r+".csv")
	l_mean = []
	for i in range(len(df_method["id"])):
	    l_values = []
	    for j in range(1,51):
	        l_values.append(df_method[str(j)][i])
	    l_mean.append(np.mean(l_values))
	df_method["mean_random"] = l_mean
	df_method = df_method.set_index(["id"])

	l_models = ["centroid","coverage","lead","clustercmrw","lexpagerank","submodular1","submodular2","textrank","COWTS","SEMCOWTS","mean_random"]

	df_stats = pd.DataFrame()
	l_temp = []
	for i in l_models:
	    l_temp = []
	    if i != "id":
	        for j in l_models:
	            if j != "id":
	                stat, p = ttest_ind(df_method[i], df_method[j])
	                l_temp.append(p)
	        df_stats[i] = l_temp

	df_stats["id"] = l_models
	df_stats = df_stats.set_index(["id"])

	# sns.set()
	# mask = np.triu(np.ones_like(df_stats, dtype=np.bool))
	# f, ax = plt.subplots(figsize=(7, 7))
	# ax = sns.heatmap(df_stats,linewidths=.5,vmax=0.05)
	# ax.set_title(r)

	# plt.show()

"""
--------------------------------------------------------------------------------------------------
Scores analysis

Metrics terms-based -> term analysis
--------------------------------------------------------------------------------------------------
"""

d_event = {'joplinTornado2011': 190.84313725490196,
 'costaRicaEarthquake2012': 12.509803921568627,
 'guatemalaEarthquake2012': 186.8235294117647,
 'philipinnesFloods2012': 53.05882352941177,
 'italyEarthquakes2012': 151.33333333333334,
 'bostonBombings2013': 578.0392156862745,
 'typhoonYolanda2013': 447.9019607843137,
 'australiaBushfire2013': 224.37254901960785,
 'queenslandFloods2013': 1278.6274509803923,
 'earthquakeBohol2013': 28.607843137254903,
 'albertaFloods2013': 187.2156862745098,
 'manilaFloods2013': 71.0,
 'chileEarthquake2014': 85.84313725490196,
 'typhoonHagupit2014': 1493.0392156862745,
 'parisAttacks2015': 595.0196078431372,
 'nepalEarthquake2015': 1397.3333333333333,
 'fireYMM2016': 1115.4117647058824,
 'shootingDallas2017': 194.31372549019608,
 'flSchoolShooting2018': 289.52941176470586,
 'hurricaneFlorence2018': 596.3529411764706,
 'philippinesEarthquake2019': 1470.7843137254902,
 'southAfricaFloods2019': 686.4313725490196,
 'cycloneKenneth2019': 1154.5294117647059,
 'albertaWildfires2019': 1826.137254901961,
 'coloradoStemShooting2019': 150.49019607843138,
 'sandiegoSynagogueShooting2019': 129.54901960784315}

dico_terms_all = {}

for event in tqdm(l_event):
	dico_terms_all[event] = {}
	with open('../../Sets/All tweets/PreProcessed/'+event+'.txt','r') as f:
		lines = f.readlines()
		for line in lines:
			for word in nltk.word_tokenize(line):
				if word not in dico_terms_all[event]:
					dico_terms_all[event][word]=1
				else:
					dico_terms_all[event][word]+=1

limit_freq = {}
for i in dico_terms_all:
	# dico_terms_all[i] = set(dict(sorted(dico_terms_all[i].items(), key=operator.itemgetter(1),reverse=True)[:int(d_event[i])]).keys())
	limit_freq[i] = sorted(dico_terms_all[i].items(), key=operator.itemgetter(1),reverse=True)[int(d_event[i])-1][1]

dico_terms_oracle = {}
dico_terms_maybe = {}
for event in dico_terms_all:
	dico_terms_oracle[event] = set()
	dico_terms_maybe[event] = set()
	for word in dico_terms_all[event]:
		if dico_terms_all[event][word] > limit_freq[event]:
			dico_terms_oracle[event].add(word)
		elif dico_terms_all[event][word] == limit_freq[event]:
			dico_terms_maybe[event].add(word)
	dico_terms_oracle[event] = dico_terms_oracle[event].union(sorted(dico_terms_maybe[event])[:(int(d_event[event])-len(dico_terms_oracle[event]))])

"""
--------------------------------------------------------------------------------------------------
Uncomment to generate Oracle frequence terms summaries in the /Model Evaluation/model/PreProcessed repository

Be careful if you have a model in the /Model Evaluation/model/PreProcessed, it will overwrite it 
--------------------------------------------------------------------------------------------------


for event in dico_terms_oracle:
	if os.path.exists('../../Model evaluation/model/PreProcessed/'+event+'.txt'):
		os.remove('../../Model evaluation/model/PreProcessed/'+event+'.txt')
	for word in dico_terms_oracle[event]:
		with open('../../Model evaluation/model/PreProcessed/'+event+'.txt',"a") as file:
			file.write(word+" ")

"""

"""
--------------------------------------------------------------------------------------------------
Once you created the Oracle summaries, generate the scores with the /Model Evaluation/model_evaluation.py file.
Then, you can uncomment the following sections

Oracle
--------------------------------------------------------------------------------------------------

df_rougescore = pd.read_csv("../../Model evaluation/ROUGE.txt",header=None)

df_rougescore_filter = df_rougescore[df_rougescore[0].apply(lambda x: True if "Average_F" in x else False)]

for r in ["ROUGE-1","ROUGE-2","ROUGE-SU"]:
	df_rougescore_filter = df_rougescore[df_rougescore[0].apply(lambda x: True if "Eval" in x else False)]
	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}

	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[6][2:]))
	    
	for i in d_score:
	    df_event_model["MODEL"] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('../../Model evaluation/'+r+'_F.csv')

	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}

	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[5][2:]))
	    
	for i in d_score:
	    df_event_model["MODEL"] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('../../Model evaluation/'+r+'_P.csv')

	df_event_model = pd.DataFrame()
	l_id = []
	d_score = {}
	
	for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if r in x else False)][0]:
	    if nltk.word_tokenize(i)[0] not in l_id:
	        l_id.append(nltk.word_tokenize(i)[0])
	        d_score[nltk.word_tokenize(i)[0]] = []
	    d_score[nltk.word_tokenize(i)[0]].append(float(nltk.word_tokenize(i)[4][2:]))
	    
	for i in d_score:
	    df_event_model["MODEL"] = d_score[i]

	df_event_model["id"] = l_event
	df_event_model = df_event_model.set_index(["id"])

	df_event_model.to_csv('../../Model evaluation/'+r+'_R.csv')

"""

"""
--------------------------------------------------------------------------------------------------
Ttest Oracle
Uncommment if you have scores for the Oracle frequence terms summaries
--------------------------------------------------------------------------------------------------
"""

# """
# --------------------------------------------------------------------------------------------------
# COS scores
# --------------------------------------------------------------------------------------------------
# """

# df_cos = pd.read_csv("../../Model evaluation/COS.csv")
# df_cos = df_cos.set_index(["id"])

# """
# --------------------------------------------------------------------------------------------------
# BLEU scores
# --------------------------------------------------------------------------------------------------
# """

# df_bleu1 = pd.read_csv("../../Model evaluation/BLEU-1.csv")
# df_bleu1 = df_bleu1.set_index(["id"])

# df_bleu2 = pd.read_csv("../../Model evaluation/BLEU-2.csv")
# df_bleu2 = df_bleu2.set_index(["id"])

# """
# --------------------------------------------------------------------------------------------------
# METEOR scores
# --------------------------------------------------------------------------------------------------
# """

# df_meteor = pd.read_csv("../../Model evaluation/METEOR.csv")
# df_meteor = df_meteor.set_index(["id"])


# """
# --------------------------------------------------------------------------------------------------
# ROUGE scores
# --------------------------------------------------------------------------------------------------
# """

# df_rougescore = pd.read_csv("../../Model evaluation/ROUGE.txt",header=None)

# df_rougescore_filter = df_rougescore[df_rougescore[0].apply(lambda x: True if "Average_F" in x else False)]

# l_id = []
# l_score = []

# for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-2" in x else False)][0]:
#     l_id.append(nltk.word_tokenize(i)[0])
#     l_score.append(float(nltk.word_tokenize(i)[4]))
    
# df_rouge_score = pd.DataFrame()
# df_rouge_score["id"] = l_id
# df_rouge_score["f_score_rouge2"] = l_score

# l_score = []

# for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-1" in x else False)][0]:
#     l_score.append(float(nltk.word_tokenize(i)[4]))
    
# df_rouge_score["f_score_rouge1"] = l_score

# l_score = []

# for i in df_rougescore_filter[df_rougescore_filter[0].apply(lambda x: True if "ROUGE-SU*" in x else False)][0]:
#     l_score.append(float(nltk.word_tokenize(i)[4]))

# df_rouge_score["f_score_rougesu"] = l_score

# df_rouge_score = df_rouge_score.set_index(["id"])

# for i in ["MODEL"]:
# 	print(i,"&",df_rouge_score["f_score_rouge2"][i.lower()],"&",df_rouge_score["f_score_rouge1"][i.lower()],"&",df_rouge_score["f_score_rougesu"][i.lower()],
# 		"&",round(np.mean(df_cos[i]),4),"&",round(np.mean(df_bleu1[i]),4),"&",round(np.mean(df_bleu2[i]),4),"&",round(np.mean(df_meteor[i]),4))


# print("T-tests : If difference is significant, p-value < 0.05 (cell in blue/black for the plots)")

# for r in ["ROUGE-2_F","ROUGE-1_F","ROUGE-SU_F","BLEU-1","BLEU-2","METEOR","COS"]:
# 	df_method = pd.read_csv("./"+r+".csv")
# 	df_method_oracle = pd.read_csv("../../Model evaluation/"+r+".csv")
# 	l_oracle = []
# 	l_mean = []
# 	for i in range(len(df_method["id"])):
# 	    l_values = []
# 	    for j in range(1,51):
# 	        l_values.append(df_method[str(j)][i])
# 	    l_mean.append(np.mean(l_values))
# 	df_method["mean_random"] = l_mean
# 	for event in df_method.index:
# 		l_oracle.append(df_method_oracle["MODEL"][event])
# 	df_method["oracle_freq"] = l_oracle
# 	df_method = df_method.set_index(["id"])

# 	l_models = ["centroid","coverage","lead","clustercmrw","lexpagerank","submodular1","submodular2","textrank","COWTS","SEMCOWTS","mean_random","oracle_freq"]

# 	df_stats = pd.DataFrame()
# 	l_temp = []
# 	for i in l_models:
# 	    l_temp = []
# 	    if i != "id":
# 	        for j in l_models:
# 	            if j != "id":
# 	                stat, p = ttest_ind(df_method[i], df_method[j])
# 	                l_temp.append(p)
# 	        df_stats[i] = l_temp

# 	df_stats["id"] = l_models
# 	df_stats = df_stats.set_index(["id"])

# 	sns.set()
# 	mask = np.triu(np.ones_like(df_stats, dtype=np.bool))
# 	f, ax = plt.subplots(figsize=(7, 7))
# 	ax = sns.heatmap(df_stats,linewidths=.5,vmax=0.05)
# 	ax.set_title(r)

# 	plt.show()