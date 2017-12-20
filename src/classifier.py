import os
import numpy as np
import pandas as pd
import scipy as sp
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB



stopwords = ["aga", "ei", "et", "ja", "jah", "kas", "kui", "kõik", "ma", "me", "mida", "midagi", "mind", "minu",
             "mis", "mu", "mul", "mulle", "nad", "nii", "oled", "olen", "oli", "oma", "on", "pole", "sa", "seda",
             "see", "selle", "siin", "siis", "ta", "te", "ära"]


count_vect = CountVectorizer(stop_words=stopwords)
tfidf_transformer = TfidfTransformer()
