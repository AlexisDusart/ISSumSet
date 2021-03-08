# Evaluate your model

In this section you can evaluate your own model with ROUGE-1, ROUGE-2, ROUGE-SU, BLEU-1, BLEU-2, METEOR, and Cosine similarity metrics.

## Requirements

```
nltk==3.5
numpy==1.17.2
pandas==0.23.4
scikit-learn==0.22.2.post1
```

* Clone the ROUGE package and remind the path of the ROUGE-1.5.5.pl file

```
git clone https://github.com/kylehg/summarizer
```

* Put your summaries for each event (26 files) in the [model](./model/Raw) repository (or specify the repository path when you call the python file).
The repository should only contains summaries files. Files format : tweets separated by \n; Files name : event_name.txt.

* For now you can evaluate one model at a time.

* It will generate in this directory the scores file BLEU-1.csv, BLEU.csv, COS.csv, METEOR.csv and ROUGE.txt if -rouge specified.

## Run

```
python model_evaluation.py -summaries SUMMARIES_YOU_WANT_TO_BE_COMPARED -model YOUR_SUMMARIES_FROM_YOUR_MODEL -rouge REPOSITORY_OF_ROUGE-1.5.5.pl -already_preprocessed False
```

* -summaries is the path of the repository wich contains the summaries you want to be compared (default is ../Sets/NHPAR/PreProcessed)
* -model is the path of the repository wich contains your model summaries (default is /model/Raw/)
* -rouge is the path of the repository wich contains the ROUGE-1.5.5.pl file (if not specified, rouge will not be evaluated)
* -already_preprocessed: set to True if your model is already preprocessed (default is False)

* Do not forget to specifiy the length of your summaries when you report your results
