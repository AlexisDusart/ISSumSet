# Evaluate state-of-the-art methods

In this section you can evaluate state-of-the-art models with ROUGE-1, ROUGE-2, ROUGE-SU, BLEU-1, BLEU-2, METEOR, and Cosine similarity metrics.
You can also find the results we obtained in the files BLEU-1.csv, BLEU-2.csv, COS.csv, METEOR.csv, ROUGE.txt, ROUGE-1_F.csv, ROUGE-1_P.csv, ROUGE-1_R.csv, ROUGE-2_F.csv, ROUGE-2_P.csv, ROUGE-2_R.csv, ROUGE-SU_F.csv, ROUGE-SU_P.csv and ROUGE-SU_R.csv.

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

* You need to have the summaries for each event for each method in the [Models Summarization](./../Summarization%20scores) repository.

## Run

python evaluate_summaries.py -rouge REPOSITORY_OF_ROUGE-1.5.5.pl

* -rouge is the path of the repository wich contains the ROUGE-1.5.5.pl file (if not specified, rouge will not be evaluated)


## Some statistics

* Once scores files generated, you can report some statistics using the [Statistics](./stats.py) file.
