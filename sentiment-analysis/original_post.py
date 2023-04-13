import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet, stopwords
import string


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

DATA_RANGE = [0.001,0.005,0.010,0.020,0.030]
X_LABEL = "Learning Rate"

TYPES = ["MLP"]

TITLE = "Multi-layer Perceptron"

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

    parser = argparse.ArgumentParser(description='Analysis of combined data file')
    parser.add_argument('--comments_added', '-c', action='store_true', help='If this run utilizes comments or not')
    args = parser.parse_args()




    data: pd.DataFrame = pd.read_csv(os.path.join("PESA-data","data","labeled",
        "cleaned","combined","data_relevance_training.csv"))
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
    tf_idf.shape


    for var in TYPES:
        train_means = []
        crossval_means = []
        for i in DATA_RANGE:
            print(i)
            train_scores = []
            crossval_scores = []
            for j in tqdm(range(1)):
                x_train, x_test, y_train, y_test = train_test_split(tf_idf, df.relevance, test_size= .2)

                # svc = SVC(kernel=var, gamma=i)
                # knc = KNeighborsClassifier(n_neighbors=i,weights=var)
                # mnb = MultinomialNB(alpha=i)
                # dtc = DecisionTreeClassifier(min_samples_split=i,criterion=var)
                # if var == "elasticnet":
                #     solver = "saga"
                # elif var == "l1":
                #     solver = "liblinear"
                # else:
                #     solver = "lbfgs"
                
                # if var == "elasticnet":
                #     l1_r = 0.5
                # else:
                #     l1_r = None
                
                # if var == "none":
                #     C_val = None
                # else:
                #     C_val = i

                # lrc = LogisticRegression(solver=solver, penalty=var, C=i, l1_ratio=l1_r)
                # rfc = RandomForestClassifier(n_estimators=31,criterion=var)
                # ada = AdaBoostClassifier(n_estimators=i)
                mlp = MLPClassifier(learning_rate_init=i)

                classifiers = {
                            # 'SVC': svc,
                            # 'KNeighborsClassifier': knc,
                            # 'Multinomial Naive Bayes': mnb,
                            # 'Decision Tree': dtc,
                            # 'Logistic Regression': lrc,
                            # 'Random Forest': rfc,
                            # 'AdaBoost': ada,
                            'Multi-Layer Perceptron': mlp
                            }

                for name, model in classifiers.items():
                    model.fit(x_train, y_train)
                    y_pred = model.predict(x_test)
                    train_scores.append(accuracy_score(y_test , y_pred))

                for name, model in classifiers.items():
                    scores = cross_val_score(model, x_test, y_test, cv=5)
                    crossval_scores.append(scores.mean())

            train_means.append(sum(train_scores)/len(train_scores))
            crossval_means.append(sum(crossval_scores)/len(crossval_scores))
        


        plt.plot(DATA_RANGE,crossval_means,label=var)
        
    plt.legend()
    plt.xlabel(X_LABEL)
    plt.ylabel("Test Accuracy")
    plt.title(TITLE)
    plt.show()

        # print('Model Training Scores')
        # for item in train_scores:
        #     print(f'{item[0]}: {item[1]}')
            
        # print('\nCross-Validation Scores')
        # for item in crossval_scores:
        #     print(f'{item[0]}: {item[1]}')

    # TEXT = [["Imagine if late president ferdinand marcos sr was still alive and witnessed this glorious moment sneezing"],
    #         ["Long live APO UN PBBM Red Heart Red Heart The AFTR shocks are still on the ABRA POEPICENTER STAYSAFE FOLDED HANDS FOLDED HANDS Bangonabrenios"],
    #         ["The amount of appreciation gratitude and respect he has for the frontliners"],
    #         ["random word"]]

    # DECODING = ['Irrelevant', 'Relevant']

    # for tweet in TEXT:
    #     tweettfidf = vectorizer.transform(tweet).toarray()
    #     print(f'"{tweet[0]}"')
    #     for name, model in classifiers.items():
    #         print(f'\t{name}: {DECODING[model.predict(tweettfidf)[0]]}')
    #     print()