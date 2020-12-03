import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu
from nltk.corpus import stopwords
ntlk.download('wordnet')
import argparse
import html
import re
import string
import subprocess
import warnings
warnings.simplefilter("ignore")


stemmer = nltk.stem.porter.PorterStemmer()
stop_words = set(stopwords.words('english')) 

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

def cosine_sim(t1,t2):
	vectorizer = TfidfVectorizer(
		ngram_range=(1,1))
	tfidf = vectorizer.fit_transform([t1,t2])
	return cosine_similarity(tfidf)[0,1]


parser = argparse.ArgumentParser()
parser.add_argument("-summaries", default='../Sets/NHPAR/PreProcessed/', type=str)
parser.add_argument("-model", default='./model/Raw/', type=str)
parser.add_argument("-rouge", default='', type=str)
parser.add_argument("-already_preprocessed", default=False, type=bool)

args = parser.parse_args()

PATH_ALL = args.summaries+"/"
PATH_MODEL_RAW = args.model+"/"
PATH_ROUGE = args.rouge+"/"
PATH_MODEL = "./model/PreProcessed/"

if args.already_preprocessed:
	PATH_MODEL = PATH_MODEL_RAW

"""
------------------------------------------------------------------------------------------
Pre-process the summaries
------------------------------------------------------------------------------------------
"""

if not args.already_preprocessed:
	for event in os.listdir(PATH_MODEL_RAW):
		if not event.startswith('.'):
			with open(PATH_MODEL_RAW+event,'r') as f:
				lines = f.readlines()
				if os.path.exists(PATH_MODEL+event):
					os.remove(PATH_MODEL+event)
				with open(PATH_MODEL+event,'a',encoding='UTF-8') as f2:
					for line in lines:
						f2.write(with_surrogates(cleanPreProcessed(line))+'\n')

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

dico_model = {}
for event in os.listdir(PATH_MODEL):
	if not event.startswith('.'):
		dico_model[event[:-4]] = []
		with open(PATH_MODEL+event,'r') as f:
			lines = f.readlines()
			for line in lines:
				dico_model[event[:-4]].extend(word_tokenize(line))

dico_model_2 = {}
for event in os.listdir(PATH_MODEL):
	if not event.startswith('.'):
		dico_model_2[event[:-4]] = ""
		with open(PATH_MODEL+event,'r') as f:
			lines = f.readlines()
			for line in lines:
				dico_model_2[event[:-4]] = dico_model_2[event[:-4]] + " " + line

"""
------------------------------------------------------------------------------------------
BLEU scores
------------------------------------------------------------------------------------------
"""

df_bleu_1 = pd.DataFrame()
df_bleu_1["id"] = list_events
list_scores = []
for i in list_events:
	list_scores.append(sentence_bleu(dico_all_bleu[i],dico_model[i], weights=(1, 0, 0, 0)))
df_bleu_1["MODEL"] = list_scores
df_bleu_1.to_csv('./BLEU-1.csv',index=False)


df_bleu_2 = pd.DataFrame()
df_bleu_2["id"] = list_events
list_scores = []
for i in list_events:
	list_scores.append(sentence_bleu(dico_all_bleu[i],dico_model[i], weights=(0, 1, 0, 0)))
df_bleu_2["MODEL"] = list_scores
df_bleu_2.to_csv('./BLEU-2.csv',index=False)


"""
------------------------------------------------------------------------------------------
METEOR score
------------------------------------------------------------------------------------------
"""

df_meteor = pd.DataFrame()
df_meteor["id"] = list_events
list_scores = []
for i in list_events:
	list_scores.append(meteor_score([dico_all[i]],dico_model_2[i]))
df_meteor["MODEL"] = list_scores
df_meteor.to_csv('./METEOR.csv',index=False)


"""
------------------------------------------------------------------------------------------
Cosine score
------------------------------------------------------------------------------------------
"""

df_cos = pd.DataFrame()
df_cos["id"] = list_events
list_scores = []
for i in list_events:
	list_scores.append(cosine_sim(dico_all[i],dico_model_2[i]))
df_cos["MODEL"] = list_scores
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
if os.path.exists(PATH_ROUGE) and PATH_ROUGE != '':
	os.makedirs(PATH_ROUGE+'/ROUGE', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/data', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/model', exist_ok=True)
	os.makedirs(PATH_ROUGE+'/ROUGE/truth', exist_ok=True)

	"""
	------------------------------------------------------------------------------------------
	Step 2 : Transform summaries to html format
	------------------------------------------------------------------------------------------
	"""



	for file in os.listdir(PATH_MODEL):
		if not file.startswith('.'):
			if os.path.exists(PATH_ROUGE+"/ROUGE/model/"+file[:-4]+".html"):
				os.remove(PATH_ROUGE+"/ROUGE/model/"+file[:-4]+".html")
			with open(PATH_ROUGE+"/ROUGE/model/"+file[:-4]+".html","a") as f1:
				f1.write("<html>\n<head>\n<title>"+file[:-4]+"</title>\n</head>\n<body bgcolor='white'>\n")
				with open(PATH_MODEL+file) as f2: 
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

	l_events = []
	for file in os.listdir(PATH_ROUGE+'/ROUGE/truth/'):
		if not file.startswith('.'):
			l_events.append(file[:-5])

	if os.path.exists(PATH_ROUGE+'/ROUGE/data/'+"settings.xml"):
		os.remove(PATH_ROUGE+'/ROUGE/data/'+"settings.xml")

	with open(PATH_ROUGE+'/ROUGE/data/'+"settings.xml","a") as f1:
		f1.write("<ROUGE_EVAL version='1.0'>\n")
		for file in l_events:
			f1.write("<EVAL ID='"+file+"'>\n<MODEL-ROOT>\n")
			f1.write(PATH_ROUGE+'/ROUGE/truth'+"\n</MODEL-ROOT>\n<PEER-ROOT>\n")
			f1.write(PATH_ROUGE+'/ROUGE/model'+"\n</PEER-ROOT>\n<INPUT-FORMAT TYPE='SEE'>\n</INPUT-FORMAT>\n<PEERS>\n")
			f1.write("<P ID='model'>"+file+".html"+"</P>\n")
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