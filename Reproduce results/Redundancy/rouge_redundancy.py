import pandas as pd
import re
import html
from rouge.rouge import rouge_n_sentence_level

df_summary = pd.read_csv("./df.csv")

THRESHOLD = 0.3

def clean2(x):
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

df2_event = {}
for i in df_summary["content.event"].unique():
	df2_event[i] = []
    
for i in range(len(df_summary["content.event"])):
	df2_event[df_summary["content.event"].iloc[i]].append((df_summary.index[i],clean2(df_summary["content.text"].iloc[i])))

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
				if rouge >= THRESHOLD:
					delete_pair.append((df2_event[i][k][1],df2_event[i][cpt][1]))
		if l_rouge_score:
			if max(l_rouge_score) >= THRESHOLD:
				delete_pair_max.append((max(l_rouge_score_max)[1],max(l_rouge_score_max)[2]))
				df2_event[i].pop(cpt)
				cpt-=1
		cpt+=1

print(delete_pair_max)