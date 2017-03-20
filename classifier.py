import nltk
import random
import pickle

from nltk.tokenize import word_tokenize
from nltk.classify import ClassifierI
from nltk.corpus import stopwords
from nltk.classify.scikitlearn import SklearnClassifier
from statistics import mode

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC

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
short_pos_words = nltk.pos_tag(short_pos_words)
short_neg_words = word_tokenize(short_neg)
short_neg_words = nltk.pos_tag(short_neg_words)

for word in short_pos_words:
    if word[0] not in stop and word[1][0] == "J":
        all_words.append(word[0].lower())

for word in short_neg_words:
    if word[0] not in stop and word[1][0] == "J":
        all_words.append(word[0].lower())

save_file = open("pickled/documents.pickle", "wb")
pickle.dump(documents, save_file)
save_file.close()

all_words = nltk.FreqDist(all_words)
top_words = list(all_words.keys())[:5000]

save_file = open("pickled/top_words.pickle", "wb")
pickle.dump(top_words, save_file)
save_file.close()

def find_features(review):
    review_words = word_tokenize(review)
    features = {}
    for word in top_words:
        features[word] = (word in review_words)
    return features

feature_sets = []

for (review, category) in documents:
    feature_sets.append((find_features(review), category))

random.shuffle(feature_sets)

save_file = open("pickled/feature_sets.pickle", "wb")
pickle.dump(feature_sets, save_file)
save_file.close()

training_set = feature_sets[:10000]
testing_set = feature_sets[10000:]

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

save_file = open("pickled/all_classifiers.pickle", "wb")
pickle.dump(all_classifiers, save_file)
save_file.close()

vote_classifier = VoteClassifier(all_classifiers[0],
                                        all_classifiers[1],
                                        all_classifiers[2],
                                        all_classifiers[3],
                                        all_classifiers[4])

print("Voted Final Classifier accuracy: ",
      (nltk.classify.accuracy(vote_classifier, testing_set)) * 100,
      "%")

save_file = open("pickled/vote_classifier.pickle", "wb")
pickle.dump(vote_classifier, save_file)
save_file.close()








