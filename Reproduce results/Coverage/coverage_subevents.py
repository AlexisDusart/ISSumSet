"""

The aim is to check the coverage of wikiPortal subevents that are not present in proposed summaries.

Step 1: Create dictionary of distinctive words for each subevent
Step 2: Retrieve each tweet that contains these distinctive words
Step 3: Verifiy each obtained tweet

"""

import pandas as pd
import pickle
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from tqdm import tqdm

"""
------------------------------------------------------------------------------------------------------
Step 1: Create dictionary
------------------------------------------------------------------------------------------------------
"""

PATH_summaries = "../../Sets/All tweets/Raw/"
df_redundancy_check = pd.read_csv("../../Paper annotations/annotations_redundancy.txt")
df_redundancy_check = df_redundancy_check[df_redundancy_check["new"]==False]
coverage_annotations = pd.read_csv("../../Paper annotations/annotations_coverage.txt")
coverage_annotations = coverage_annotations.set_index(["id"])
coverage_annotations = coverage_annotations.drop(set(df_redundancy_check["id"]))
subevents = pickle.load( open( "./subevent.pkl", "rb" ) )
map_subevent_event = pickle.load( open( "./map_subevent_event.pkl", "rb" ) )
s_dataset_subevents = set()
s_subevents = set()

for i in range(1,155):
	s_subevents.add('SubEvent'+str(i))

for i in coverage_annotations["Partly"]:
	for j in s_subevents:
		if "'"+j+"'" in i:
			s_dataset_subevents.add(j)

for i in coverage_annotations["TheWhole"]:
	for j in s_subevents:
		if "'"+j+"'" in i:
			s_dataset_subevents.add(j)

# for i in s_subevents-s_dataset_subevents:
# 	print(i,subevents[i])

d_words_subevents = {'SubEvent126' : ['police','micah','x','johnson','gunman','five','5','officers','seven','7'],#0
'SubEvent93' : ['39','musician','beatles','u2','madonna','lady','gaga','beyonce','katy','perry','lorde','one direction','justin','bieber','charity','album'],#0
'SubEvent18': ['loss','power','100,000','houses'], #0
'SubEvent131' : ['donald','trump','campaign','cancels'],#0
'SubEvent25' : ['close','school','office'],#0
'SubEvent12': ['cincinnati','ohio','power','84,000','home'],#0
'SubEvent51' : ['dzhokhar','tsarnaev','capture','condition','beth','israel','deaconess','medical','center','president','barack','obama','collaboration','lockdown','emergency'],#0
'SubEvent128': ['families','student','parkland','florida','tallahassee','capitol','advocacy','lawmaker','legislative','republican-controlled','vote','motion','debate','assault','weapon','ban','legislation','71-36'],#0
'SubEvent8' : ['interstate','44','close'],#0
'SubEvent133' : ['amtrak','service','cancel','train','washington','flightaware','180','flight','charleston','international','airport','south','california','midnight'],#0.5
'SubEvent54' : ['dzhokhar','tsarnaev','beth','israel','deaconess','medical','center','federal','prison','fort','devens','massachusetts'],#0
'SubEvent59' : ['unsolve','triple','murder','waltham','massachusetts','septemeber','11','2011','brendan','mess','roommate','tamerlan'],#0
'SubEvent71' : ['7.2','balilihan','74'],#1
'SubEvent26' : ['20,000','flee','53'],#0.5
'SubEvent89' : ['world','bank','500','million','$','loan'],#0
'SubEvent81' : ['total','international','aid','140','$','million'],#0
'SubEvent40' : ['london','marathon','3','three'],#0.5
'SubEvent60' : ['ibragim','todashev','suspect'],#0
'SubEvent31' : ['60'],#1
'SubEvent3' : ['curfew'],#0
'SubEvent100' : ['president','chile','michelle','bachelet','northern','disaster','zone','arica','parinacota','tarapaca'],#1
'SubEvent122': ['poland','eu','quota','refugees'],#1
'SubEvent30' : ['70'],#0
'SubEvent28' : ['16'],#1
'SubEvent92' : ['armed','forces','united','states','scales','back','operations'],#0
'SubEvent82' : ['president','benigno','aquino','criticized','survivors','aid','agencies','international','local','media','inadequate'],#0
'SubEvent88' : ['president','benigno','aquino','encamps','oversee','rescue','relief','operations','criticism','disorganize'],#0
'SubEvent129' : ['president','donald','trump','white','house','dining','room','parents','friends','safe','put','politic','aside','control'],#1
'SubEvent6' : ['patients','evacuate','john','regional','medical','center'],#0
'SubEvent85' : ['david','cameron','30','million','£'],#0
'SubEvent72' : ['156','374'],#0
'SubEvent27' : ['haikui','xiangshan','chinese','zhejiang'],#0
'SubEvent52' : ['russian','intelligence','warn','tamerlan','tsarnaev'],#0
'SubEvent53' : ['michael','bloomberg','mayor','new','york','city','federal','bureau','investigation'],#0
'SubEvent61' : ['abdul','baki','abdul-baki','todashev','father','ibragim','innocent','chechens'],#0
'SubEvent42' : ['pressure','cooker','nylon','shrapnel'],#1
'SubEvent130' : ['first','national','bank','omaha','hertz','united','delta','airlines','nra','cancel'],#0
'SubEvent139' : ['30.5','77','swansboro','north','carolina','24','61'],#0
'SubEvent58' : ['bury','al-barzakh','cemetery','doswell','virginia'],#0
'SubEvent98' : ['united','kingdom','billion','$'],#0
'SubEvent132' : ['tar','heels','football','ucf','knights','wolfpack','mountaineers','cancel'],#0
'SubEvent119' : ['social','media','safety','check','facebook','twitter'],#1
'SubEvent43' : ['episode','family','guy','fox','network','film','lions','film4'],#0
'SubEvent29' : ['calamity'],#0
'SubEvent41' : ['nba','season','indiana','pacers','celtics','cancel'],#0
'SubEvent55' : ['prosecutors','plea','deal','avoidance','penalty','wife','connection','extremist'],#0.5
'SubEvent90' : ['china','peace','ark'],#1
'SubEvent24' : ['saola','12','154,000'],#0
'SubEvent39' : ['taliban','deny'],#0
'SubEvent44' : ['president','barack','obama','visit'],#1
'SubEvent118' : ['françois','hollande','cancel','g-20','antalya']}#1

# 0 : 36
# 0.5 : 4
# 1 : 11

"""
------------------------------------------------------------------------------------------------------
Step 2: Retrieve each tweet that contains these distinctive words
------------------------------------------------------------------------------------------------------
"""

for subevent in d_words_subevents:
	for i in range(len(d_words_subevents[subevent])):
		d_words_subevents[subevent][i] = PorterStemmer().stem(d_words_subevents[subevent][i])


d_tweets_subevent = {}
for subevent in tqdm(d_words_subevents):
	d_tweets_subevent[subevent] = []
	with open(PATH_summaries+map_subevent_event[subevent]+'.txt') as f:
		tweets = f.readlines()
		for tweet in tweets:
			for word in word_tokenize(tweet):
				if PorterStemmer().stem(word) in d_words_subevents[subevent]:
					d_tweets_subevent[subevent].append(tweet)
					break

"""
------------------------------------------------------------------------------------------------------
Step 3: Verifiy each obtained tweet
------------------------------------------------------------------------------------------------------
"""

# For each subevent, if at least one tweet is about the subevent, annotated 1 or 0.5 (entirely or partly). If no, annotated 0

for i in d_tweets_subevent:
	print(i)
	print(subevents[i])
	print("\n")
	print(d_tweets_subevent[i])
	
# For each subevent annotated 0.5 or 1, check if it should be in

l_missed = ['SubEvent133','SubEvent71','SubEvent26','SubEvent40','SubEvent31','SubEvent122','SubEvent100','SubEvent28','SubEvent129',
'SubEvent42','SubEvent119','SubEvent55','SubEvent90','SubEvent44','SubEvent118']

for i in d_tweets_subevent:
	if i ==in l_missed:
		print(i)
		print(subevents[i])
		print("\n")
		print(d_tweets_subevent[i])

"""
distant means distant consequences of the event, not a direct narration of the event
example :
event : "boston bombings"
subevent : "Organisers and security officials reassess security plans for Sunday's 2013 London Marathon."

'hurricane florence' : '133' : distant
'earthquake bohol' : '71' : should be in
'philippines floods' : '26' : should be in ; '31' : should be in ; '28' : should be in
'boston bombings' : '40' : distant ; '42' : should be in ; '55' : distant ; '44' : distant
'chile earthquake' : '100' : should be in
'paris attack' : '122' : distant ; '119' : distant ; '118' : distant
'fl school shooting' : '129' : distant
'typhoon yolanda' : '90' : distant
"""