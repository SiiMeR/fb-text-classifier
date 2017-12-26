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

testfile = [["Kristjan Puusepp","Ma oleks haige"],
            ["Siim Raudsepp", "Helge päev täna"],
            ["Siim Raudsepp", "Kõik on sama täna"],
            ["Kristjan Puusepp", "Miski pole enam endine"]]

m = MyHTMLParser()
data = pd.DataFrame(m.parseChat("tekst1.html"), columns=["author","text"])


stopwords = ["aga", "ei", "et", "ja", "jah", "kas", "kui", "kõik", "ma", "me", "mida", "midagi", "mind", "minu",
             "mis", "mu", "mul", "mulle", "nad", "nii", "oled", "olen", "oli", "oma", "on", "pole", "sa", "seda",
             "see", "selle", "siin", "siis", "ta", "te", "ära"]


count_vect = CountVectorizer(stop_words=stopwords)
tfidf_transformer = TfidfTransformer()

X_counts = count_vect.fit_transform(data.text.astype('U'))
X_tfidf = tfidf_transformer.fit_transform(X_counts)
multinomialnb = MultinomialNB().fit(X_tfidf,data.author)

test=["Ma homo", "Helge päev täna", "Miski"]
X_test_counts = count_vect.transform(test)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)

predicted = multinomialnb.predict(X_test_tfidf)

print(predicted)
#for doc, category in zip(test, predicted):
#    print(category)
#    print('%s => %s' % (doc, data.author))


#print(X_tfidf.shape)

