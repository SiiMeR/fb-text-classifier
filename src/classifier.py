import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from src.parser import MyHTMLParser


class MyTextClassifier:

    def __init__(self, file):
        if isinstance(file, bytes):  # was given file contents(bytes)
            self.learn(file, True)
        if isinstance(file, str):  # was given a file name
            self.learn(file)

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
                           alpha=1e-3, random_state=42, max_iter=5, tol=None))])

    htmlParser = MyHTMLParser()

    def learn(self, file, isString = False):
        print("Learning from the file...")
        authorsAndText = self.htmlParser.parseChat(file, isString)
        data = pd.DataFrame(authorsAndText, columns=["author", "text"])
        self.text_clf = self.text_clf.fit(data.text.astype('U'), data.author)
        print("Learning is finished.")

    def predictAuthor(self, text):
        predictedAuthor = self.text_clf.predict(text)
        return predictedAuthor


