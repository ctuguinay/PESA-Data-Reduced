import spacy
from spacy import displacy
from collections import Counter
import pandas as pd

from tqdm import tqdm

import os

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize


WITH_STOP_WORD_FILTERING = True
if WITH_STOP_WORD_FILTERING:
    fname = "corpus_counts_filtering"
else:
    fname = "corpus_counts_no_filtering"

DATA_FILENAME = os.path.join("PESA-data","data","unlabeled","cleaned","combined",
    "data_relevance_filtered.csv")
OUTPUT_FILENAME = os.path.join("PESA-data","data","processed",fname)

if __name__ == "__main__":

    f = open(DATA_FILENAME)

    nlp = spacy.load('en_core_web_sm')

    lines = f.read().splitlines()[1:]

    cts_arr = []

    for line in tqdm(lines):
        cts = {}
        parts = line.split(".")
        if len(parts) != 2:
            continue

        payload = parts[-1]


        document = nlp(payload)

        for token in document:
            if str(token) in stopwords.words() and WITH_STOP_WORD_FILTERING:
                continue
            word_type = token.pos_
            if word_type not in cts:
                cts[word_type] = 0
            cts[word_type] += 1
        
        cts_arr.append(cts)

    labels = list()

    for cts in cts_arr:
        for label in cts:
            if label not in labels:
                labels.append(label)

    outfile = open(OUTPUT_FILENAME,"w+")

    outfile.write(",".join(labels) + "\n")

    for cts in cts_arr:
        cts_list = []
        for label in labels:
            if label not in cts:
                cts_list.append("0")
            else:
                cts_list.append(str(cts[label]))
        cts_string = ",".join(cts_list) + "\n"
        outfile.write(cts_string)
