import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
from tqdm import tqdm
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu
nltk.download('wordnet')
import argparse
import subprocess
import warnings
warnings.simplefilter("ignore")


def cosine_sim(t1,t2):
	vectorizer = TfidfVectorizer(
		ngram_range=(1,1))
	tfidf = vectorizer.fit_transform([t1,t2])
	return cosine_similarity(tfidf)[0,1]


parser = argparse.ArgumentParser()
parser.add_argument("-summaries", default='../../Sets/NHPAR/PreProcessed/', type=str)
parser.add_argument("-models", default='../Models Summarization/', type=str)
parser.add_argument("-rouge", default='', type=str)

args = parser.parse_args()

PATH_ALL = args.summaries+"/"
PATH_MODEL = args.models+"/"
PATH_ROUGE = args.rouge+"/"



"""
------------------------------------------------------------------------------------------
Reference initialisation, the text is transformed in list
------------------------------------------------------------------------------------------
"""

dico_all = {}
dico_all_bleu = {}
list_events = []

for event in os.listdir(PATH_ALL):
	if not event.startswith('.'):
		dico_all[event[:-4]] = ""
		list_events.append(event[:-4])
		with open(PATH_ALL+event,'r') as f:
			lines = f.readlines()
			for line in lines:
				dico_all[event[:-4]] = dico_all[event[:-4]] + " " + line

for event in os.listdir(PATH_ALL):
	if not event.startswith('.'):
		dico_all_bleu[event[:-4]] = []
		with open(PATH_ALL+event,'r') as f:
			lines = f.readlines()
			for line in lines:
				dico_all_bleu[event[:-4]].extend(word_tokenize(line))

for i in dico_all:
	dico_all_bleu[i] = [dico_all_bleu[i]]

"""
------------------------------------------------------------------------------------------
BLEU scores
------------------------------------------------------------------------------------------
"""

df_bleu_1 = pd.DataFrame()
df_bleu_1["id"] = list_events
df_bleu_2 = pd.DataFrame()
df_bleu_2["id"] = list_events

for method in tqdm(os.listdir(PATH_MODEL)):
	if method != "pkusumsum.py" and not method.startswith('.'):
		dico_method = {}
		for event in list_events:
			dico_method[event] = []
			with open(PATH_MODEL+method+'/'+event+'.txt','r') as f:
				lines = f.readlines()
				for line in lines:
					dico_method[event].extend(word_tokenize(line))
		list_scores_1 = []
		list_scores_2 = []
		for i in list_events:
			list_scores_1.append(sentence_bleu(dico_all_bleu[i],dico_method[i], weights=(1, 0, 0, 0)))
			list_scores_2.append(sentence_bleu(dico_all_bleu[i],dico_method[i], weights=(0, 1, 0, 0)))
		df_bleu_1[method] = list_scores_1
		df_bleu_2[method] = list_scores_2

df_bleu_1.to_csv('./BLEU-1.csv',index=False)
df_bleu_2.to_csv('./BLEU-2.csv',index=False)


"""
------------------------------------------------------------------------------------------
METEOR score
------------------------------------------------------------------------------------------
"""

df_meteor = pd.DataFrame()
df_meteor["id"] = list_events

for method in tqdm(os.listdir(PATH_MODEL)):
	if method != "pkusumsum.py" and not method.startswith('.'):
		dico_method = {}
		for event in list_events:
			dico_method[event] = ""
			with open(PATH_MODEL+method+'/'+event+'.txt','r') as f:
				lines = f.readlines()
				for line in lines:
					dico_method[event] = dico_method[event] + " " + line
		list_scores = []
		for i in list_events:
			list_scores.append(meteor_score([dico_all[i]],dico_method[i]))
		df_meteor[method] = list_scores

df_meteor.to_csv('./METEOR.csv',index=False)


"""
------------------------------------------------------------------------------------------
Cosine score
------------------------------------------------------------------------------------------
"""

df_cos = pd.DataFrame()
df_cos["id"] = list_events

for method in tqdm(os.listdir(PATH_MODEL)):
	if method != "pkusumsum.py" and not method.startswith('.'):
		dico_method = {}
		for event in list_events:
			dico_method[event] = ""
			with open(PATH_MODEL+method+'/'+event+'.txt','r') as f:
				lines = f.readlines()
				for line in lines:
					dico_method[event] = dico_method[event] + " " + line
		list_scores = []
		for i in list_events:
			list_scores.append(cosine_sim(dico_all[i],dico_method[i]))
		df_cos[method] = list_scores

df_cos.to_csv('./COS.csv',index=False)


"""
------------------------------------------------------------------------------------------
ROUGE scores
------------------------------------------------------------------------------------------
"""

"""
------------------------------------------------------------------------------------------
Step 1 : Repository creation
------------------------------------------------------------------------------------------
"""
if os.path.exists(PATH_ROUGE):
	os.makedirs(PATH_ROUGE+'/ROUGE', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/data', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/methods', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/truth', exist_ok=True)

	"""
	------------------------------------------------------------------------------------------
	Step 2 : Transform summaries to html format
	------------------------------------------------------------------------------------------
	"""

	for rep in range(1,51):
		os.makedirs(PATH_ROUGE+'/ROUGE/methods/'+str(rep), exist_ok=True)
		for file in os.listdir(PATH_MODEL+str(rep)):
			if not file.startswith('.'):
				if os.path.exists(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html"):
					os.remove(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html")
				with open(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html","a") as f1:
					f1.write("<html>\n<head>\n<title>"+file[:-4]+"</title>\n</head>\n<body bgcolor='white'>\n")
					with open(PATH_MODEL+str(rep)+"/"+file) as f2: 
						lines = f2.readlines() 
						cpt=0
						for line in lines:
							cpt+=1
							f1.write("<a name=\""+str(cpt)+"\">["+str(cpt)+"]</a> <a href=\"#"+str(cpt)+"\" id="+str(cpt)+">"+line+"</a>\n")
					f1.write("</body>\n</html>")


	l_methods=["coverage","lead","centroid","lexpagerank","textrank","submodular1","submodular2","clustercmrw","COWTS","SEMCOWTS"]


	for rep in l_methods:
		os.makedirs(PATH_ROUGE+'/ROUGE/methods/'+str(rep), exist_ok=True)
		for file in os.listdir(PATH_MODEL+str(rep)):
			if not file.startswith('.'):
				if os.path.exists(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html"):
					os.remove(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html")
				with open(PATH_ROUGE+'/ROUGE/methods/'+str(rep)+"/"+file[:-4]+".html","a") as f1:
					f1.write("<html>\n<head>\n<title>"+file[:-4]+"</title>\n</head>\n<body bgcolor='white'>\n")
					with open(PATH_MODEL+str(rep)+"/"+file) as f2: 
						lines = f2.readlines() 
						cpt=0
						for line in lines:
							cpt+=1
							f1.write("<a name=\""+str(cpt)+"\">["+str(cpt)+"]</a> <a href=\"#"+str(cpt)+"\" id="+str(cpt)+">"+line+"</a>\n")
					f1.write("</body>\n</html>")

	for file in os.listdir(PATH_ALL):
		if not file.startswith('.'):
			if os.path.exists(PATH_ROUGE+'/ROUGE/truth/'+file[:-4]+".html"):
				os.remove(PATH_ROUGE+'/ROUGE/truth/'+file[:-4]+".html")
			with open(PATH_ROUGE+'/ROUGE/truth/'+file[:-4]+".html","a") as f1:
				f1.write("<html>\n<head>\n<title>"+file[:-4]+"</title>\n</head>\n<body bgcolor='white'>\n")
				with open(PATH_ALL+file) as f2: 
					lines = f2.readlines() 
					cpt=0
					for line in lines:
						cpt+=1
						f1.write("<a name=\""+str(cpt)+"\">["+str(cpt)+"]</a> <a href=\"#"+str(cpt)+"\" id="+str(cpt)+">"+line+"</a>\n")
				f1.write("</body>\n</html>")

	"""
	------------------------------------------------------------------------------------------
	Step 3 : Settings file creation
	------------------------------------------------------------------------------------------
	"""

	if os.path.exists(PATH_ROUGE+'/ROUGE/data/'+"settings.xml"):
		os.remove(PATH_ROUGE+'/ROUGE/data/'+"settings.xml")
	with open(PATH_ROUGE+'/ROUGE/data/'+"settings.xml","a") as f1:
		f1.write("<ROUGE_EVAL version='1.0'>\n")
		for file in list_events:
			f1.write("<EVAL ID='"+file+"'>\n<MODEL-ROOT>\n")
			f1.write(PATH_ROUGE+'/ROUGE/truth'+"\n</MODEL-ROOT>\n<PEER-ROOT>\n")
			f1.write(PATH_ROUGE+'/ROUGE/methods'+"\n</PEER-ROOT>\n<INPUT-FORMAT TYPE='SEE'>\n</INPUT-FORMAT>\n<PEERS>\n")
			for i in range(1,51):
				f1.write("<P ID='"+str(i)+"'>"+str(i)+"/"+file+".html"+"</P>\n")
			for i in l_methods:
				f1.write("<P ID='"+i+"'>"+i+"/"+file+".html"+"</P>\n")
			f1.write("</PEERS>\n<MODELS>\n")
			f1.write("<M ID='"+file+"'>"+file+".html</M>\n")
			f1.write("</MODELS>\n</EVAL>\n")
		f1.write("</ROUGE_EVAL>")

	"""
	------------------------------------------------------------------------------------------
	Step 4 : Call ROUGE
	------------------------------------------------------------------------------------------
	"""
	f = open("ROUGE.txt", "w")
	subprocess.call(['perl', PATH_ROUGE+'ROUGE-1.5.5.pl', '-a', '-e', PATH_ROUGE+"/data", '-n',
	 "2", "-x", "-m", "-2", "-4", "-u", "-c", "95", "-r", "1000", 
	  "-f","-A","-p","0.5","-t","0","-d",PATH_ROUGE+"/ROUGE/data/settings.xml"], stdout=f)
	f.close()