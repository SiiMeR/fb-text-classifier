# CLI implementation of the bot : useful for testing
from src.classifier import MyTextClassifier
import requests

print("Welcome to Facebook chat history classifier")

fileName = input("Enter the filename of the facebook chat history \n")

print("Learning from file...")
clf  = MyTextClassifier(fileName)
print("Learned successfully, we may continue")


while True:
    sentence = input("Enter a random sentence and I will predict the author \n")
    predictedAuthor = clf.predictAuthor([sentence])
    print("I think this sentence is said by " + predictedAuthor[0])

