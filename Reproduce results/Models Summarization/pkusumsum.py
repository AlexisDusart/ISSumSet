import subprocess
import os
import argparse

PATH = "../../Sets/PKUSet/"

# Average size of summaries in number of words for each event

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

parser = argparse.ArgumentParser()
parser.add_argument("-PATH_JAR", default='', type=str)
parser.add_argument("-PATH_STOPWORDS", default='', type=str)
args = parser.parse_args()
PATH_JAR = args.PATH_JAR
PATH_STOPWORDS=args.PATH_STOPWORDS

if os.path.exists(PATH_JAR) and os.path.exists(PATH_STOPWORDS):

	l_events = []
	for file in os.listdir("../../Sets/NHP/PreProcessed/"):
		if not file.startswith('.'):
			l_events.append(file[:-4])

	# Method Coverage

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input', PATH+i,
			"-output", "./coverage/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "0", "-stop", PATH_STOPWORDS])

	# Method Lead

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',
		 PATH+i,"-output", "./lead/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "1", "-stop", PATH_STOPWORDS])

	# Method Centroid

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',
		 PATH+i,"-output", "./centroid/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "2", "-stop", PATH_STOPWORDS])

	# Method LexPageRank

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',
		 PATH+i,"-output", "./lexpagerank/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "4", "-stop", PATH_STOPWORDS])

	# Method TextRank

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',
		 PATH+i,"-output", "./textrank/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "5", "-stop", PATH_STOPWORDS])

	# Method ClusterCMRW

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',
		 PATH+i,"-output", "./clustercmrw/"+i+".txt", "-L", "2", "-n", str(int(d_event[i])), "-m", "7", "-stop", PATH_STOPWORDS])

	# Method SubModular1

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',PATH+i,"-output", "./submodular1/"+i+".txt",
		 "-L", "2", "-n", str(int(d_event[i])), "-m", "6", "-stop", PATH_STOPWORDS, "-sub","1"])

	# Method SubModular2

	for i in l_events:
		subprocess.call(['java', '-jar', PATH_JAR, '-T', "2", '-input',PATH+i,"-output", "./submodular2/"+i+".txt",
		 "-L", "2", "-n", str(int(d_event[i])), "-m", "6", "-stop", PATH_STOPWORDS, "-sub","2"])

else:
	print("Invalid PATH")