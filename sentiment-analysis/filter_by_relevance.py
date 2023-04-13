import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import pickle

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
import string

# Uncomment these out if this is your first time running this file.
# Comment them once you are done running the file, for the first time.
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#nltk.download('wordnet')
#nltk.download('omw-1.4')

stops = set(word.lower() for word in list(stopwords.words('english')))
lemmatizer = WordNetLemmatizer()

def getPOS(word):
    """
    Gets the part of speech for some word.
    """
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

ENCODING = {'irrelevant': 0, 'relevant': 1}

def processText(text: str) -> str:
    text = (text.translate(str.maketrans('', '', string.punctuation))
                .split(' . ')[0]
                .lower())
    split = [w for w in text.split(' ') if (not w in stops and len(w) > 1)]
    uniques = ' '.join(sorted(set(split), key=split.index))
    lemmatized = []
    for w in nltk.word_tokenize(uniques):
        lemmatizedW = lemmatizer.lemmatize(w, getPOS(w))
        if len(lemmatizedW) > 1:
            lemmatized.append(lemmatizedW)
    return ' '.join(lemmatized)


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    data: pd.DataFrame = pd.read_csv(os.path.join(script_dir,"data","labeled",
        "cleaned","combined","data_relevance_training.csv").replace("sentiment-analysis\\", ""))
    encoded: pd.Series = data['relevance'].apply(lambda x: ENCODING[x])
    text: pd.Series = data['text'].apply(processText)

    # Splits on the separator ' . ' and takes the first element, the original post.
    df = pd.DataFrame([text, encoded]).T
    df = df.astype({'text': 'string', 'relevance': 'int'})
    df.head(5)

    # Vectorizes the text using sklearn Tfidfvectorizer.
    vectorizer = TfidfVectorizer(max_df=0.95, lowercase=True)
    tf_idf = vectorizer.fit_transform(df['text'])
    words = vectorizer.get_feature_names_out()
    tf_idf = normalize(tf_idf).toarray()

    # Train test split.
    x_train, x_test, y_train, y_test = train_test_split(tf_idf, df.relevance, test_size= .2, random_state=10)

    # Test saved model's accuracy.
    filename = 'svc_model.sav'
    loaded_svc = pickle.load(open(filename, 'rb'))
    loaded_y_pred = loaded_svc.predict(x_test)
    accuracy = accuracy_score(y_test ,loaded_y_pred)

    if accuracy > 0.81:
        pre_filtered_data: pd.DataFrame = pd.read_csv(os.path.join(script_dir,"data","unlabeled",
            "cleaned","combined","data_pre_filtering.csv").replace("sentiment-analysis\\", ""))
        text: pd.Series = pre_filtered_data['text'].apply(processText)

        # Splits on the separator ' . ' and takes the first element, the original post.
        pre_filtered_df = pd.DataFrame([text]).T
        pre_filtered_df = pre_filtered_df.astype({'text': 'string'})

        # Vectorizes the text using the original Tfidfvectorizer.
        pre_filtered_tf_idf = vectorizer.transform(pre_filtered_df['text'])
        pre_filtered_words = vectorizer.get_feature_names_out()
        pre_filtered_tf_idf = normalize(pre_filtered_tf_idf).toarray()

        # Get Predicted Load.
        loaded_predicted = loaded_svc.predict(pre_filtered_tf_idf)

        # Drop rows that were deemed irrelevance by the SVC.
        index_list = []
        for index, value in enumerate(loaded_predicted):
            if value == 0:
                index_list.append(index)
        filtered_data = pre_filtered_data.drop(pre_filtered_data.index[index_list])

        # Save filtered data into CSV.
        filtered_data.to_csv(os.path.join(script_dir,"data","unlabeled",
            "cleaned","combined","data_relevance_filtered.csv").replace("sentiment-analysis\\", ""),
            index = False)