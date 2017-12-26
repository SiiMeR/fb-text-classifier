import os
import numpy as np
import pandas as pd
import scipy as sp
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

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

    text_clf = Pipeline([('vect', CountVectorizer(stop_words=stopwords,ngram_range=(1,3))),
                         ('tfidf', TfidfTransformer(use_idf=True)),
                         ('clf', SGDClassifier(loss='hinge',fit_intercept=True, penalty='l2',
                           alpha = 1e-3, random_state = 42, max_iter = 5, tol = None))])

    htmlParser = MyHTMLParser()


    def learnFromFile(self, file):
        authorsAndText = self.htmlParser.parseChat(file)
        data = pd.DataFrame(authorsAndText, columns=["author", "text"])
        self.text_clf = self.text_clf.fit(data.text.astype('U'), data.author)



    def predictAuthor(self, text):
        predictedAuthor = self.text_clf.predict(text)
        return predictedAuthor


