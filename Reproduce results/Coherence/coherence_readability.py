import os
from readability import Readability
import numpy as np
from nltk import word_tokenize
from nltk import sent_tokenize
from tqdm import tqdm
import pandas as pd
import seaborn as sn
import html
import re
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import nltk
nltk.download('punkt')

PATH = '../../Sets/NHPAR/Raw/'
PATH_all = '../../Sets/All tweets/Raw/'
text = ''

l_not_use = ["earthquakeBohol2013.txt","costaRicaEarthquake2012.txt","philipinnesFloods2012.txt",
            "manilaFloods2013.txt","chileEarthquake2014.txt"]


def clean(x):
      x=' '.join(x.split())
      x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
      x=html.unescape(x)
      x=re.sub(r'http\S+','',x, flags=re.MULTILINE)
      # to remove links that start with HTTP/HTTPS in the tweet
      x=re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)','',x, flags=re.MULTILINE) 
      # to remove other url links
      x=re.sub(r"@(\w+)", '',x, flags=re.MULTILINE)
      x=''.join([i if ord(i) < 128 else ' ' for i in x])
      x=' '.join(x.split())
      return x

"""
-------------------------------------------------------------------------------------------------------
Scores for proposed summaries
-------------------------------------------------------------------------------------------------------
"""

print("------------------------------------------------------------------")
print("Comparison CGS - All tweets")
print("------------------------------------------------------------------")

l_flesch_kincaid = []
l_flesch = []
l_gunning_fog = []
l_coleman_liau = []
l_dale_chall = []
l_ari = []
l_linsear_write = []
l_spache = []
l_flesch_ease = []

for i in os.listdir(PATH):
    if not i.startswith('.'):
        if i not in l_not_use:
            with open(PATH+i,'r') as f:
                text = f.read()
                r = Readability(clean(text))
                s1 = r.flesch_kincaid()
                s2 = r.flesch()
                s3 = r.gunning_fog()
                s4 = r.coleman_liau()
                s5 = r.dale_chall()
                s6 = r.ari()
                s7 = r.linsear_write()
                # r.smog()
                s8 = r.spache()
                l_flesch_kincaid.append(s1.score)
                l_flesch.append(s2.score)
                l_flesch_ease.append(s2.ease)
                l_gunning_fog.append(s3.score)
                l_coleman_liau.append(s4.score)
                l_dale_chall.append(s5.score)
                l_ari.append(s6.score)
                l_linsear_write.append(s7.score)
                l_spache.append(s8.score)
            

"""
-------------------------------------------------------------------------------------------------------
Scores for all tweets
-------------------------------------------------------------------------------------------------------
"""

l_flesch_kincaid2 = []
l_flesch2 = []
l_gunning_fog2 = []
l_coleman_liau2 = []
l_dale_chall2 = []
l_ari2 = []
l_linsear_write2 = []
l_spache2 = []
l_flesch_ease2 = []

for i in os.listdir(PATH):
    if not i.startswith('.'):
        if i not in l_not_use:
            with open(PATH_all+i,'r') as f:
                text = f.read()
                r = Readability(clean(text))
                s1 = r.flesch_kincaid()
                s2 = r.flesch()
                s3 = r.gunning_fog()
                s4 = r.coleman_liau()
                s5 = r.dale_chall()
                s6 = r.ari()
                s7 = r.linsear_write()
                # r.smog()
                s8 = r.spache()
                l_flesch_kincaid2.append(s1.score)
                l_flesch2.append(s2.score)
                l_flesch_ease2.append(s2.ease)
                l_gunning_fog2.append(s3.score)
                l_coleman_liau2.append(s4.score)
                l_dale_chall2.append(s5.score)
                l_ari2.append(s6.score)
                l_linsear_write2.append(s7.score)
                l_spache2.append(s8.score)

"""
-------------------------------------------------------------------------------------------------------
Correlations
-------------------------------------------------------------------------------------------------------
"""

# Proposed summaries

l_methods = [l_ari,l_flesch_kincaid,l_gunning_fog,l_coleman_liau,l_dale_chall,l_linsear_write,l_spache]
name_methods = ['l_ari','l_flesch_kincaid','l_gunning_fog','l_coleman_liau','l_dale_chall','l_linsear_write','l_spache']

data = {}
for i in range(len(l_methods)):
    data[name_methods[i]] = l_methods[i]
    
df = pd.DataFrame(data,columns = name_methods)

corrMatrix = df.corr(method = 'pearson')

sn.heatmap(corrMatrix,linewidths=.5,annot=True)

plt.show()

#  Gunning-Fog, Ari, Linsearwrite, Spache and Flesch-Kincaid are highly correlated

# All tweets

l_methods = [l_ari2,l_flesch_kincaid2,l_gunning_fog2,l_coleman_liau2,l_dale_chall2,l_linsear_write2,l_spache2]
name_methods = ['l_ari','l_flesch_kincaid','l_gunning_fog','l_coleman_liau','l_dale_chall','l_linsear_write','l_spache']

data = {}
for i in range(len(l_methods)):
    data[name_methods[i]] = l_methods[i]
    
df = pd.DataFrame(data,columns = name_methods)

corrMatrix = df.corr(method = 'pearson')

sn.heatmap(corrMatrix,linewidths=.5,annot=True)

plt.show()

#  Gunning-Fog, Ari, Linsearwrite, Spache and Flesch-Kincaid are highly correlated

"""
-------------------------------------------------------------------------------------------------------
Readability scores (as reported in Table 4 of the paper)
-------------------------------------------------------------------------------------------------------
"""

l_event_s = []
for i in os.listdir(PATH):
    if not i.startswith('.'):
        if i not in l_not_use:
            l_event_s.append(i)

for i in range(len(l_flesch_kincaid2)):
    print(l_event_s[i],'&',end=' ')
    print(round(l_flesch_kincaid2[i],1),'&',end=' ')
    print(round(l_flesch_kincaid[i],1),'&',end=' ')
    print(round(l_coleman_liau2[i],1),'&',end=' ')
    print(round(l_coleman_liau[i],1),'&',end=' ')
    print(round(l_dale_chall2[i],1),'&',end=' ')
    print(round(l_dale_chall[i],1))
print(round(np.mean(l_flesch_kincaid2),1),'&',round(np.mean(l_flesch_kincaid),1),'&',round(np.mean(l_coleman_liau2),1),'&',round(np.mean(l_coleman_liau),1),'&',round(np.mean(l_dale_chall2),1),'&',round(np.mean(l_dale_chall),1))
print(round(np.std(l_flesch_kincaid2),1),'&',round(np.std(l_flesch_kincaid),1),'&',round(np.std(l_coleman_liau2),1),'&',round(np.std(l_coleman_liau),1),'&',round(np.std(l_dale_chall2),1),'&',round(np.std(l_dale_chall),1))



cpt=0
# 21*7
for i in range(len(l_flesch_kincaid2)):
    if np.mean(l_flesch_kincaid2[i])-l_flesch_kincaid[i] < 0:
        cpt+=1
    if np.mean(l_gunning_fog2[i])-l_gunning_fog[i] < 0:
        cpt+=1
    if np.mean(l_coleman_liau2[i])-l_coleman_liau[i] < 0:
        cpt+=1
    if np.mean(l_dale_chall2[i])-l_dale_chall[i] < 0:
        cpt+=1
    if np.mean(l_ari2[i])-l_ari[i] < 0:
        cpt+=1
    if np.mean(l_linsear_write2[i])-l_linsear_write[i] < 0:
        cpt+=1
    if np.mean(l_spache2[i])-l_spache[i] < 0:
        cpt+=1
print('Rate of score CGS > score All :',cpt/(21*7))

# Remove outlier "italyEarthquakes2012.txt"

del l_flesch_kincaid2[l_event_s.index("italyEarthquakes2012.txt")]
del l_flesch_kincaid[l_event_s.index("italyEarthquakes2012.txt")]
del l_coleman_liau2[l_event_s.index("italyEarthquakes2012.txt")]
del l_coleman_liau[l_event_s.index("italyEarthquakes2012.txt")]
del l_dale_chall2[l_event_s.index("italyEarthquakes2012.txt")]
del l_dale_chall[l_event_s.index("italyEarthquakes2012.txt")]

stat, p = ttest_ind(l_flesch_kincaid2, l_flesch_kincaid)
print("Flesch-Kincaid :")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')

stat, p = ttest_ind(l_coleman_liau2, l_coleman_liau)
print("\n")
print("Coleman-Liau :")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')

stat, p = ttest_ind(l_dale_chall2, l_dale_chall)
print("\n")
print("Dale-Chall")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')

"""
-------------------------------------------------------------------------------------------------------
Stats texts
-------------------------------------------------------------------------------------------------------
"""

count_word = 0
count_sent = 0
for i in os.listdir(PATH):
    if not i.startswith('.'):
        with open(PATH+i) as file:
            for lines in file:
                count_sent+=len(sent_tokenize(lines))
                count_word+=len(word_tokenize(lines))
            
print("Average length of sentences in words for CGS :",count_word/count_sent)

count_word = 0
count_sent = 0
for i in os.listdir(PATH_all):
    if not i.startswith('.'):
        with open(PATH_all+i) as file:
            for lines in file:
                count_sent+=len(sent_tokenize(lines))
                count_word+=len(word_tokenize(lines))
            
print("Average length of sentences in words for All tweets :",count_word/count_sent)

count_word = 0
count_letter = 0
for i in os.listdir(PATH):
    if not i.startswith('.'):
        with open(PATH+i) as file:
            for lines in file:
                for i in word_tokenize(lines):
                    count_letter+=len(i)
                count_word+=len(word_tokenize(lines))
            
print("Average length of words in characters for CGS :",count_letter/count_word)

count_word = 0
count_letter = 0
for i in os.listdir(PATH_all):
    if not i.startswith('.'):
        with open(PATH_all+i) as file:
            for lines in file:
                for i in word_tokenize(lines):
                    count_letter+=len(i)
                count_word+=len(word_tokenize(lines))
            
print("Average length of words in characters for All tweets :",count_letter/count_word)


"""
-------------------------------------------------------------------------------------------------------
Compare 
-------------------------------------------------------------------------------------------------------
"""

print("------------------------------------------------------------------")
print("Comparison CGS - Random tweets with same length")
print("------------------------------------------------------------------")

PATH_randoms = '../../Sets/Random Summaries Raw/'

l_flesch_kincaid = []
l_flesch = []
l_gunning_fog = []
l_coleman_liau = []
l_dale_chall = []
l_ari = []
l_linsear_write = []
l_spache = []
l_flesch_ease = []

for i in os.listdir(PATH):
    if not i.startswith('.'):
        if i not in l_not_use:
            with open(PATH+i,'r') as f:
                text = f.read()
                r = Readability(clean(text))
                s1 = r.flesch_kincaid()
                s2 = r.flesch()
                s3 = r.gunning_fog()
                s4 = r.coleman_liau()
                s5 = r.dale_chall()
                s6 = r.ari()
                s7 = r.linsear_write()
                # r.smog()
                s8 = r.spache()
                l_flesch_kincaid.append(s1.score)
                l_flesch.append(s2.score)
                l_flesch_ease.append(s2.ease)
                l_gunning_fog.append(s3.score)
                l_coleman_liau.append(s4.score)
                l_dale_chall.append(s5.score)
                l_ari.append(s6.score)
                l_linsear_write.append(s7.score)
                l_spache.append(s8.score)
            

l_flesch_kincaid2 = []
l_flesch2 = []
l_gunning_fog2 = []
l_coleman_liau2 = []
l_dale_chall2 = []
l_ari2 = []
l_linsear_write2 = []
l_spache2 = []
l_flesch_ease2 = []


for i in tqdm(os.listdir(PATH)):
    l_flesch_kincaid2_temp = []
    l_flesch2_temp = []
    l_gunning_fog2_temp = []
    l_coleman_liau2_temp = []
    l_dale_chall2_temp = []
    l_ari2_temp = []
    l_linsear_write2_temp = []
    l_spache2_temp = []
#     l_flesch_ease2 = []
    if i not in l_not_use and not i.startswith('.'):
        for nb in range(1,51):
            with open(PATH_randoms+str(nb)+'/'+i,'r') as f:
                text = f.read()
                r = Readability(clean(text))
                s1 = r.flesch_kincaid()
                s2 = r.flesch()
                s3 = r.gunning_fog()
                s4 = r.coleman_liau()
                s5 = r.dale_chall()
                s6 = r.ari()
                s7 = r.linsear_write()
                # r.smog()
                s8 = r.spache()
                l_flesch_kincaid2_temp.append(s1.score)
                l_flesch2_temp.append(s2.score)
#                 l_flesch_ease2_temp.append(s2.ease)
                l_gunning_fog2_temp.append(s3.score)
                l_coleman_liau2_temp.append(s4.score)
                l_dale_chall2_temp.append(s5.score)
                l_ari2_temp.append(s6.score)
                l_linsear_write2_temp.append(s7.score)
                l_spache2_temp.append(s8.score)
        l_flesch_kincaid2.append(np.mean(l_flesch_kincaid2_temp))
        l_flesch2.append(np.mean(l_flesch2_temp))
        l_gunning_fog2.append(np.mean(l_gunning_fog2_temp))
        l_coleman_liau2.append(np.mean(l_coleman_liau2_temp))
        l_dale_chall2.append(np.mean(l_dale_chall2_temp))
        l_ari2.append(np.mean(l_ari2_temp))
        l_linsear_write2.append(np.mean(l_linsear_write2_temp))
        l_spache2.append(np.mean(l_spache2_temp))

cpt=0
# 21*7
for i in range(len(l_flesch_kincaid2)):
    if np.mean(l_flesch_kincaid2[i])-l_flesch_kincaid[i] < 0:
        cpt+=1
    if np.mean(l_gunning_fog2[i])-l_gunning_fog[i] < 0:
        cpt+=1
    if np.mean(l_coleman_liau2[i])-l_coleman_liau[i] < 0:
        cpt+=1
    if np.mean(l_dale_chall2[i])-l_dale_chall[i] < 0:
        cpt+=1
    if np.mean(l_ari2[i])-l_ari[i] < 0:
        cpt+=1
    if np.mean(l_linsear_write2[i])-l_linsear_write[i] < 0:
        cpt+=1
    if np.mean(l_spache2[i])-l_spache[i] < 0:
        cpt+=1

print('Rate of score CGS > score All :',cpt/(21*7))

del l_flesch_kincaid2[l_event_s.index("italyEarthquakes2012.txt")]
del l_flesch_kincaid[l_event_s.index("italyEarthquakes2012.txt")]
del l_coleman_liau2[l_event_s.index("italyEarthquakes2012.txt")]
del l_coleman_liau[l_event_s.index("italyEarthquakes2012.txt")]
del l_dale_chall2[l_event_s.index("italyEarthquakes2012.txt")]
del l_dale_chall[l_event_s.index("italyEarthquakes2012.txt")]

stat, p = ttest_ind(l_flesch_kincaid2, l_flesch_kincaid)
print("Flesch-Kincaid :")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')

stat, p = ttest_ind(l_coleman_liau2, l_coleman_liau)
print("\n")
print("Coleman-Liau :")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')

stat, p = ttest_ind(l_dale_chall2, l_dale_chall)
print("\n")
print("Dale-Chall")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
    print('Probably the same distribution')
else:
    print('Probably different distributions')