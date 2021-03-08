# Reproduce results

In this directory you can find the detailed information about our experiments, some examples and the code to reproduce our experiments.

## Coherence

Run the [coherence_readability.py](./Coherence/coherence_readability.py) file to obtain all the results.

## Cohesion

You can compare the order of the tweets in the summary and the order of the tweets using the subevents date with the [chronological_cohesion.py](./Cohesion/chronological_cohesion.py) file.

## Coverage

Once you run the file [initialization](../initialization.py), the file verification.txt has been updated and the file df.csv has been created. Then you can annotate yourself the coverage using the [coverage.py](./Coverage/coverage.py) file. At the left of the interface you have the tweet and in the box on the right you have the subevent. You can annotate if the tweet cover partly, the whole, or not at all the subevent. Breathe, this tool is a little bit slow.
You can also check the subevents missing in the summary compared to the entire dataset using [coverage_subevents.py](./Coverage/coverage_subevents.py).

## Redundancy

Once you run the file [initialization](../initialization.py) the input.txt and output.txt has been initialized. You can run the [redundancy.py](./Redundancy/redundancy.py) file to annotate yourself the redundancy. Annotations will be in outuput.txt file, the *new* column represents the novelty or redundancy of a tweet. We presented the tool in the paper, see Section 4.2.1.
You can also check the tweets removed automatically by ROUGE score using the file [rouge_redundancy.py](./Coverage/rouge_redundancy.py). The output of this file is the list of pairs tweets : the deleted tweet and the tweet with the max ROUGE score for the deleted tweet.

## Run state-of-the-art approaches

We used two tools to run the state-of-the-art approaches : **PKUSUMSUM** and **disaster_summarizer_TWEB_2018**.

### PKUSUMSUM

Download the PKUSUMSUM package [here](https://github.com/PKULCWM/PKUSUMSUM "PKUSUMSUM Github Repository")

```
git clone https://github.com/PKULCWM/PKUSUMSUM.git
```

Modify lines to the code/Tokenizer.java file in the tokenizeEng method (around line 100-120) :
Remove : 
```
if (token.equals(".") || token.equals("?") ||token.equals("!"))
	{
	    ifend=true;
	}
```
And add :

```
if (token.equals("<END_OF_TWEET>")) {
	ifend = true;
	continue;
}
```

The result should be:
```
while (ptbt.hasNext()) {
	CoreLabel label = (CoreLabel)ptbt.next();
	String token = label.toString();
	if (!ifend) {
		if (token.equals("<END_OF_TWEET>")) {
  			ifend = true;
  			continue;
		} 
	if (token.equals("-LRB-") || token.equals("-RRB-") || token.equals("-LCB-") || token.equals("-RCB-") || token.equals("\""))
  	continue; 
```

Then regenerate the PKUSUMSUM.jar file.
Remind the PATH of this new jar file and the PATH of the **stopwords_english.txt** file.

You can now generate summaries for the methods : Centroid, ClusterCMRW, Coverage, Lead, LexPageRank, SubModular1, SubModular2, and TextRank.
Move to the [Models summarization](./Models%20summarization) folder and run the [pkusumsum.py](./Models%20summarization/pkusumsum.py) file :
```
python pkusumsum.py -PATH_JAR PATH_JAR_FILE -PATH_STOPWORDS PATH_STOPWORDS_FILE
```

* Submodular1 and Submodular2 methods can take several hours to run.

### COWTS and SEMCOWTS

* To generate summaries with COWTS and SEMCOWTS methods, download the code [here](https://github.com/krudra/disaster_summarizer_TWEB_2018 "Github Repository")
```
git clone https://github.com/krudra/disaster_summarizer_TWEB_2018
```

* Follow the instructions on their README, to sum up:
	- First you have to run the "disaster_summarizer_TWEB_2018/classification/Future_Classifier.py" file for each event (you have to download the Twitter POS Tagger [here](https://code.google.com/archive/p/ark-tweet-nlp/downloads) or [here](http://www.cs.cmu.edu/~ark/TweetNLP/))
	Before runnging Future_Classifier.py modifications:
		- Set the TAGGER_PATH variable l.52 (path for ark-tweet-nlp-0.3.2/)
		- Modify "classifier_disctionary/english_pronoun.txt" to "classifier_dictionary/english_pronoun.txt" (remove misprint 's' letter) l.30
		- Lines 30 to 37 and l.227 (train_clf = joblib.load('DISMODEL.pkl')), add prefix PATH to match your PATH
		- Modify lines 273 and 286 : unigram = tok.tokenize(s) -> unigram = list(tok.tokenize(s)) and temp = tok.tokenize(row[3]) -> temp = list(tok.tokenize(row[3]))

	```
	python Future_Classifier.py PATH_event_tweets_file PATH_output_classification_file
	```

	- Second you have to run the "disaster_summarizer_TWEB_2018/summarization/COWTS/content_word_extraction.py" file for each event

	Before runnging content_word_extraction.py modifications:
		- PATH_hybd_place is PATH_to/summarization/COWTS/hydb_place.txt
		- Set the TAGGER_PATH variable l.29 (path for ark-tweet-nlp-0.3.2/)
		- Add : "from nltk.tokenize import word_tokenize" to the import section at the top of the file
		- Modify (around l.130-150):

		```
			s = ''
			for x in temp:
				if len(x) > 0:
					try:
						s = s + x.encode('ascii','ignore') + ' '
					except Exception as e:
						pass
			
			z = ''
			for x in All:
				if len(x) > 0:
					try:
						z = z + x.encode('ascii','ignore') + ' '
					except Exception as e:
						pass
			temp1 = Tweet[index]

			try:
				p = str(count) + '\t' + temp1[0].strip(' \t\n\r') + '\t' + temp1[1].strip(' \t\n\r') + '\t' + temp1[2].strip(' ,\t\n\r') + '\t' + temp1[3].strip(' ,\t\n\r') + '\t' + s.strip(' \t') + '\t' + z.strip(' \t\n\r') + '\t' + str(L) + '\t' + temp1[4].strip(' \t\n\r') + '\t' + temp1[5].strip(' \t\n\r')
				fo.write(p)
				fo.write('\n')
				count+=1
			except Exception as e:
				r+=1
				pass
			index+=1
			temp = set([])
			All = set([])
			L = 0
		```

		to :

		```
			s = ''
			for x in temp:
				if len(x) > 0:
					s = s + x.encode('utf-8').decode('utf-8') + ' '#x.encode(encoding='utf-8',errors='ignore') + ' '
			z = ''
			for x in All:
				if len(x) > 0:
					z = z + x.encode('utf-8').decode('utf-8') + ' '
			temp1 = Tweet[index]

			try:
				p = str(count) + '\t' + temp1[0].strip(' \t\n\r') + '\t' + temp1[1].strip(' \t\n\r') + '\t' + temp1[2].strip(' ,\t\n\r') + '\t' + temp1[3].strip(' ,\t\n\r') + '\t' + s.strip(' \t') + '\t' + z.strip(' \t\n\r') + '\t' + str(len(nltk.word_tokenize(temp1[3].strip(' ,\t\n\r')))) + '\t' + temp1[4].strip(' \t\n\r') + '\t' + temp1[5].strip(' \t\n\r')
				fo.write(p)
				fo.write('\n')
				count+=1
			except Exception as e:
				r+=1
				pass
			index+=1
			temp = set([])
			All = set([])
			L = 0
		```

	```
	python content_word_extraction.py PATH_output_classification_file PATH_hybd_place PATH_output_content_file
	```

	- Third you can (finally :) ) run the COWTS and SEMCOWTS:
		* You need to install Gurobi (Gurobi License is required) : https://www.gurobi.com/
		* PATH_breakpoint_file is PATH_to/Reproduce results/breakpoint/event_name.txt
		* PATH_Synsets is PATH_to/summarization/SEMCOWTS/Total_UMBC_Synset.txt
		* COWTS:
			- Modify the TAGGER_PATH variable l.29 (path for ark-tweet-nlp-0.3.2/)
			- Modify lines 103 to 107 (remove 2 first lines and untab 3 last):
				```
				k = compute_selection_criteria(All,TW)
				if k==1:
					T[index] = temp
					TW[index] = [tid,text,temp,All,Length]
					index+=1
				```
			to
				```
				# k = compute_selection_criteria(All,TW)
				# if k==1:
				T[index] = temp
				TW[index] = [tid,text,temp,All,Length]
				index+=1
				```
			- Modify file output name line 120 : ofname = keyterm + '_TWEB_PNCOWTS_' + str(window) + '.txt' -> ofname = keyterm + '.txt'
			- Set the ouput path to "PATH_to/Reproduce results/Models summarization/COWTS/"+ofname line 245
			- Modify the iteritems methods to items (l.134,147,265) and the sort method to sorted (l.161-162) :
				```
				sen = tweet_word.keys()
				sen.sort()
				```
				to
				```
				sen = sorted(tweet_word.keys())
				```
			- Modify lines 203,217,223 to:
				- if entities[j] in v: -> if list(entities)[j] in v:
				- P += word[entities[i]] * con_var[i] -> P += word[list(entities)[i]] * con_var[i]
				- if entities[i] in v: -> if list(entities)[i] in v:

			Run the "disaster_summarizer_TWEB_2018/summarization/COWTS/NCOWTS.py" file:
				```
				python NCOWTS.py PATH_output_content_file PATH_breakpoint_file PATH_hybd_place event_name
				```
		* SEMCOWTS:
			- Modify the TAGGER_PATH variable l.28 (path for ark-tweet-nlp-0.3.2/)
			- Modify lines 117 to 121 (remove 2 first lines and untab 3 last):
				```
				k = compute_selection_criteria(All,TW)
				if k==1:
					T[index] = temp
					TW[index] = [tid,text,temp,All,Length]
					index+=1
				```
			to
				```
				# k = compute_selection_criteria(All,TW)
				# if k==1:
				T[index] = temp
				TW[index] = [tid,text,temp,All,Length]
				index+=1
			- Set the ouput path you want lines 157 and 166 (we recommend to create a directory /content/ for these outputs)
			- Modify file output name line 248 : ofname = keyterm + '_NSEMCOWTS_' + str(window) + '.txt' -> ofname = keyterm + '.txt'
			- Set the ouput path to "PATH_to/Reproduce results/Models summarization/SEMCOWTS/"+ofname line 385
			- Untab 1 time lines 394 and 412			
			- Modify line 392:
				```
				fo.write(tweet_word[int(temp[1])][2] + ' ')
				```
				to
				```
				fo.write(tweet_word[int(temp[1])][2])
				fo.write('\n')
				```
			- Modify the iteritems methods to items (l.158,167,177,184,194,199,229,234,238,291,304,402) and the sort method to sorted (l.318-319)
			- Modify lines 354,363,368 to:
				- if entities[j] in v: -> if list(entities)[j] in v:
				- P += word[entities[i]] * con_var[i] -> P += word[list(entities)[i]] * con_var[i]
				- if entities[i] in v: -> if list(entities)[i] in v:

			Run the "disaster_summarizer_TWEB_2018/summarization/SEMCOWTS/NSEMCOWTS.py" file:
				```
				python NSEMCOWTS.py PATH_output_content_file PATH_breakpoint_file PATH_Synsets PATH_hybd_place event_name
				```

Once you have generated the summaries, put them in the [COWTS](./Models%20Summarization/COWTS) and [SEMCOWTS](./Models%20Summarization/SEMCOWTS) repositories.

## Evaluate state-of-the-art approaches

Once you have summaries for all the methods and put them in the associated folders, see this [README](./Summarization%20scores) to evaluate the models with the ROUGE, BLEU, COS and METEOR measures.
