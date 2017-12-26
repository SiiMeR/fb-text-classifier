import os
import numpy as np
import pandas as pd
import scipy as sp
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB

from src.parser import MyHTMLParser

class MyTextClassifier():

    def __init__(self, file):

        self.learnFromFile(file)

    testfile = [["Kristjan Puusepp", "Ma oleks haige"],
                ["Siim Raudsepp", "Helge päev täna"],
                ["Siim Raudsepp", "Kõik on sama täna"],
                ["Kristjan Puusepp", "Miski pole enam endine"]]

    stopwords = ["aga", "ei", "et", "ja", "jah", "kas", "kui", "kõik", "ma", "me", "mida", "midagi", "mind", "minu",
                 "mis", "mu", "mul", "mulle", "nad", "nii", "oled", "olen", "oli", "oma", "on", "pole", "sa", "seda",
                 "see", "selle", "siin", "siis", "ta", "te", "ära"]

    count_vect = CountVectorizer(stop_words=stopwords)
    tfidf_transformer = TfidfTransformer()
    multinomialnb = None

    htmlParser = MyHTMLParser()


    def learnFromFile(self, file):
        authorsAndText = self.htmlParser.parseChat(file)
        data = pd.DataFrame(authorsAndText, columns=["author", "text"])
        X_counts = self.count_vect.fit_transform(data.text.astype('U'))
        X_tfidf = self.tfidf_transformer.fit_transform(X_counts)
        self.multinomialnb = MultinomialNB().fit(X_tfidf, data.author)

    def predictAuthor(self, text):
        X_test_counts = self.count_vect.transform(text)
        X_test_tfidf = self.tfidf_transformer.transform(X_test_counts)

        predictedAuthor = self.multinomialnb.predict(X_test_tfidf)

        return predictedAuthor

    # for doc, category in zip(test, predicted):
    #    print(category)
    #    print('%s => %s' % (doc, data.author))

