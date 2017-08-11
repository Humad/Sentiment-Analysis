import nltk
import pickle

from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from statistics import mode

# A classifier class that uses multiple classifiers
# to get a more accurate result for a set of features
class VoteClassifier(ClassifierI):

    # Takes multiple classifiers and stores them
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    # Takes a set of features
    # Returns the most common classification result
    def classify(self, features):
        votes = self.count(features)
        return mode(votes)

    # Takes a set of features
    # Returns how confident it is with the classification result
    def conf(self, features):
        votes = self.count(features)
        return votes.count(mode(votes)) / len(votes)

    # Takes a set of features
    # Returns a list of results from each classifier
    def count(self, features):
        votes = []
        for c in self._classifiers:
            votes.append(c.classify(features))

        return votes


load_file = open("pickled/top_words.pickle", "rb")
top_words = pickle.load(load_file)
load_file.close()

# Tokenizes words from document and checks whether or not
# each of the words is in the list of most popular words.
# Returns a mapping of words to their existence.
def find_features(document):
    given_words = word_tokenize(document)
    features = {}
    for word in top_words:
        features[word] = (word in given_words)
    return features

load_file = open("pickled/all_classifiers.pickle", "rb")
all_classifiers = pickle.load(load_file)
load_file.close()

vote_classifier = VoteClassifier(all_classifiers[0],
                                 all_classifiers[1],
                                 all_classifiers[2],
                                 all_classifiers[3],
                                 all_classifiers[4])

# Takes text and returns its classification and confidence regarding classification
def sentiment(text):
    feature_set = find_features(text)
    return vote_classifier.classify(feature_set), vote_classifier.conf(feature_set) * 100







