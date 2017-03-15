import nltk
import random
import pickle

from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from statistics import mode

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = count(features)
        return mode(votes)

    def conf(self, features):
        votes = count(features)
        return votes.count(mode(votes)) / len(votes)

    def count(self, features):
        votes = []
        for c in self._classifiers:
            votes.append(c.classify(features))

        return votes



short_pos = open("training_data/positive.txt", "r").read()
short_neg = open("training_data/negative.txt", "r").read()

documents = []

for review in short_pos.split('\n'):
    documents.append((review, "pos"))

for review in short_neg.split('\n'):
    documents.append((review, "neg"))

all_words = []
stop = set(stopwords.words("english"))
short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for word in short_pos_words:
    if word not in stop:
        all_words.append(word.lower())

for word in short_neg_words:
    if word not in stop:
        all_words.append(word.lower())

all_words = nltk.FreqDist(all_words)
top_words = list(all_words.keys())[:2000]
feature_sets = []

def find_features(review):
    review_words = word_tokenize(review)
    features = {}
    for word in top_words:
        features[word] = (word in review_words)
    return features

for (review, category) in documents:
    feature_sets.append((find_features(review), category))

random.shuffle(feature_sets)

training_set = feature_sets[:1000]
testing_set = feature_sets[1000:]

all_classifiers = [MultinomialNB(),
                   BernoulliNB(),
                   LogisticRegression(),
                   LinearSVC(),
                   NuSVC()]

all_classifier_names = ["MultinomialNB",
                        "BernoulliNB",
                        "Logistic Regression",
                        "LinearSVC",
                        "NuSVC"]

for i in range(0, len(all_classifiers)):
    classifier = SklearnClassifier(all_classifiers[i])
    classifier.train(training_set)
    all_classifiers[i] = classifier
    print(all_classifier_names[i], " accuracy: ",
          (nltk.classify.accuracy(classifier, testing_set)) * 100,
          "%")

voted_final_classifier = VoteClassifier(all_classifiers[0],
                                        all_classifiers[1],
                                        all_classifiers[2],
                                        all_classifiers[3],
                                        all_classifiers[4])

print("Voted Final Classifier accuracy: ",
      (nltk.classify.accuracy(voted_final_classifier, testing_set)) * 100,
      "%")
    








