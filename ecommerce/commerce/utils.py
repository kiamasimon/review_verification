from random import random
import numpy as np
#from nltk.corpus import movie_reviews, product_reviews_1
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy as nltk_accuracy
import pandas as pd
#import nltk
#nltk.download('movie_reviews')
import nltk
from nltk.corpus import movie_reviews


def extract_features(words):
    return dict([(word, True) for word in words])

#
nltk.download('movie_reviews')
# nltk.download('product_reviews_2')


def SentimentAnalyzer():
    text = "The movie was amazing"
    fileids_pos = movie_reviews.fileids('pos')
    fileids_neg = movie_reviews.fileids('neg')

    features_pos = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in fileids_pos]
    features_neg = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in fileids_neg]

    threshold = 0.8
    num_pos = int(threshold*len(features_pos))
    num_neg = int(threshold*len(features_neg))

    features_train = features_pos[:num_pos] + features_neg[:num_neg]
    features_test = features_pos[num_pos:] + features_neg[num_neg:]

    classifier = NaiveBayesClassifier.train(features_train)

    probabilities = classifier.prob_classify(extract_features(text.split()))
    predicted_sentiment = probabilities.max()

    response = {
        "accuracy": nltk_accuracy(classifier, features_test),
        "predicted_sentiment": predicted_sentiment,
        "probability": round(probabilities.prob(predicted_sentiment), 2)
    }
    print(response)
    return response


# def Analyzer():
#     # -*- coding: utf-8 -*-
#     """
#     @author: Julie
#
#     """
#
#     # adding libraries
#
#     nltk.download('punkt')
#     nltk.download('wordnet')
#     from collections import Counter
#     from sklearn.metrics import accuracy_score
#
#     # load dataset
#     np.random.seed(2000)  # to ensure run results are kept consistent
#     Corpus = pd.read_csv('C:/Users/kiama/reviews.csv')  # corpus is a collection of data/text(dataset)
#
#     Corpus.describe()  # show numerical column statistics
#     Corpus.info()  # get detailed column details
#
#     # data cleaning
#     print(Corpus.isnull().sum().sort_values(
#         ascending=False))  # check total missing values for all columns (in descending order)
#     Corpus.drop(
#         columns=['reviews.userCity', 'reviews.userProvince', 'reviews.dateSeen', 'reviews.didPurchase', 'reviews.id',
#                  'reviews.dateAdded'], inplace=True)  # drop columns with too much missing data
#     print(Corpus.shape)  # confirm column delete was successful
#     # fill empty columns
#     for col in Corpus:
#         if type(Corpus[col]) == 'object':
#             Corpus[col] = Corpus[col].fillna(value='Unknown')
#         else:
#             Corpus[col] = Corpus[col].fillna(value=0)
#     print(Corpus.isnull().sum().sort_values(ascending=False))
#     # convert all text to lowercase
#     Corpus['reviews.text'] = Corpus['reviews.text'].str.lower()
#     # change reviews.date column to datetime type, and strip off date, time & timezone
#     print(Corpus['reviews.date'].head())
#     Corpus['reviews.date'] = pd.to_datetime(Corpus['reviews.date'])
#     Corpus['reviews.date'] = Corpus['reviews.date'].astype(str).str[:-21]
#     # rename the column
#     Corpus.rename(columns={'reviews.date': 'reviews.year'}, inplace=True)
#     Corpus.info()
#     # remove punctuations and special characters
#     special = ["!", "@", "#", "%", "^", "&", "*", "_", "+", "=", ":", '"', ";", "/", "'", "[", "<", ">", "]", ".", "{",
#                "|",
#                "}", "`", "\\", "?", "(", ")", ",", "-", "~"]
#     for char in special:
#         Corpus['reviews.text'] = Corpus['reviews.text'].str.replace(char, '')
#     # remove digits from the text
#     nodigit = Corpus['reviews.text'].str.replace('\d+', '')
#     print(nodigit)
#     # map(lambda x: x.isdigit(), Corpus['reviews.text'])
#     # list(*map(print, Corpus['reviews.text']))  # * character unpacks the mapping to produce printable output
#     # print(*Corpus['reviews.text'])  #this is an alternative way to print the mapping results
#
#     # tokenization
#     tokenize = nodigit.fillna("").apply(nltk.word_tokenize)
#     print(tokenize)
#     # remove stopwords using gensim library
#     import gensim
#
#     stopwords = gensim.parsing.preprocessing.STOPWORDS
#     print(stopwords)
#     from gensim.parsing.preprocessing import STOPWORDS
#
#     stopwords_gensim = STOPWORDS.union(set(['inch', 'however', 'my', 'e', 'i', 've', 'ive', 'far', 'this']))
#     stopwords_gensim2 = stopwords_gensim.difference(set(['not', 'no', 'fire']))
#     nostop = tokenize.fillna("").apply(lambda x: [item for item in x if item not in stopwords_gensim2])
#     print(nostop.head(10))
#     # detokenization
#     # nostop = nostop.str.join(' ')
#     # # nostop1 = nostop.apply(lambda x: ''.join(map(str, x)))
#     # from nltk.tokenize.treebank import TreebankWordDetokenizer
#     # # print("\n".join(' '.join(elems) for elems in nostop)
#     # TreebankWordDetokenizer().detokenize(nostop)
#
#     # word lemmatization with POS tags to get appropriate word roots
#     from nltk.corpus import wordnet as wn
#     from nltk.tag import pos_tag
#     from nltk.stem import WordNetLemmatizer
#     from collections import defaultdict
#
#     tag_map = defaultdict(lambda: wn.NOUN)
#     tag_map['J'] = wn.ADJ
#     tag_map['V'] = wn.VERB
#     tag_map['R'] = wn.ADV
#     # nostop = nostop.astype(str)
#     for index, entry in enumerate(nostop):  # iterates over items in nostop
#         cleantext = []  # empty list to store the resultant words produced
#         # nostop = np.asarray(nostop)
#         nostop.iloc[0:34659, cleantext] = str(cleantext)
#     # def lemmatize_text(nostop):
#     #     nostop = pd.Series.apply(lemmatize_text(nostop))
#     #     return [lemmatizer.lemmatize(w) for w in nostop]
#     for token, tag in pos_tag(nostop):
#         lemmatizer = WordNetLemmatizer()
#         lemtext = lemmatizer.lemmatize(token, tag_map[tag[0]])
#         cleantext.append(lemtext)
#         print(nostop, "=>", lemtext)
#
#         # data visualization and analysis
#     import matplotlib.pyplot as plt
#     import seaborn as sns
#
#     # check consistency of reviews posted over the years
#     plt.subplots(figsize=(5, 5))
#     sns.set(style="dark")
#     sns.countplot(Corpus['reviews.year'], data=Corpus)
#     plt.xticks(rotation=90)
#     plt.show()
#     # check reviews.rating column to see how many users used each rating
#     newC = pd.DataFrame(Corpus.groupby('reviews.rating', as_index=True).size().sort_values(ascending=False).rename(
#         'no of customers').reset_index())
#     sns.set(style="darkgrid")
#     f, ax = plt.subplots(figsize=(5, 5))
#     sns.set_color_codes("pastel")
#     sns.barplot(x='reviews.rating', y='no of customers', data=newC)
#     ax.set(ylabel="no of customers", xlabel="ratings")
#     plt.show()
#
#     # classify reviews as either positive or negative
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn import model_selection, naive_bayes, svm
#
#     #reviews label encoding
#     from sklearn.preprocessing import LabelEncoder
#
#     #place main columns in separate dataframe
#     maindf = Corpus['reviews.rating' , 'reviews.text' , 'reviews.title' , 'reviews.username', 'reviews.year'].dropna()
#     maindf.head()
#     #identify reviews with ratings 1, 2, 4, 5
#     check = maindf[(maindf['reviews.rating'] == 1), (maindf['reviews.rating'] == 2), (maindf['reviews.rating'] == 4), (maindf['reviews.rating'] == 5)]
#     check.shape
#
#     y = check['reviews.rating']
#     x = check['reviews.text']
#     len(y)
#     X = x['reviews.text']
#     print(X)
#     len(X)
#     #vectorize input variable (X)
#     from sklearn.feature_extraction.text import CountVectorizer
#     bow_transformer = CountVectorizer(analyzer = nostop).fit(X)
#     len(bow_transformer.vocabulary_)
#
#     # split data into training and testing sets
#     from sklearn import linear_model
#     from sklearn.model_selection import train_test_split
#     #create train and test variables
#     y = Corpus['reviews.text']
#     X_train, X_test, Y_train, Y_test = train_test_split(lemtext, y, test = 0.3)
#
#     #fitting a training model
#     from sklearn.linear_model import LinearRegression
#     # model = linear.model.LinearRegression()


#nltk.download('movie_reviews')
# nltk.download('product_reviews_2')













