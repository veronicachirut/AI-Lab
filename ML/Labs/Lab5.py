from sklearn import preprocessing
import numpy as np
from sklearn import svm
from sklearn.metrics import f1_score, classification_report


def normalize_data(train_data, test_data, type=None):
    scaler = None
    if type == 'standard':
        scaler = preprocessing.StandardScaler()

    elif type == 'min_max':
        scaler = preprocessing.MinMaxScaler()

    elif type == 'l1':
        scaler = preprocessing.Normalizer(norm='l1')

    elif type == 'l2':
        scaler = preprocessing.Normalizer(norm='l2')

    if scaler is not None:
        scaler.fit(train_data)
        scaled_train_data = scaler.transform(train_data)
        scaled_test_data = scaler.transform(test_data)
        return (scaled_train_data, scaled_test_data)
    else:
        print("No scaling was performed. Raw data is returned.")
        return (train_data, test_data)

class BagOfWords:

    def __init__(self):
        self.vocabulary = []
        self.vocabulary_length = 0
    def build_vocabulary(self, data):
        self.vocabulary = [word for sentence in data
                           for word in sentence]
        self.vocabulary = list(set(self.vocabulary))
        self.vocabulary_length = len(self.vocabulary)
        print(self.vocabulary)
        print(self.vocabulary_length)

    # def build_vocabulary(self, data):
    #     for document in data:
    #         for word in document:
    #             # word = word.lower()
    #             if word not in self.vocabulary:
    #                 self.vocabulary.append(word)
    #
    #     self.vocabulary_length = len(self.vocabulary)
    #     self.vocabulary = np.array(self.vocabulary)
    #     print(self.vocabulary)
    #     print(self.vocabulary_length)

    def get_features(self, data):
        dictionary = dict(zip(self.vocabulary, range(self.vocabulary_length)))
        features = []
        for sentence in data:
            features_sentence = np.zeros([self.vocabulary_length])
            for word in sentence:
                if word in dictionary:
                    features_sentence[[dictionary[word]]] += 1
            features.append(features_sentence)
        features = np.array(features)
        return features

    # def get_features(self, data):
    #     features = np.zeros((len(data), self.vocabulary_length))
    #
    #     for document_idx, document in enumerate(data):
    #         for word in document:
    #             if word in self.vocabulary:
    #                 features[document_idx, np.where(self.vocabulary == word)[0]] += 1
    #     return features

def compute_accuracy(y_true, y_predicted):
    accuracy = np.sum(y_true == y_predicted) / len(y_predicted)
    return accuracy

test_labels = np.load('data/test_labels.npy')
test_data = np.load('data/test_sentences.npy', allow_pickle = True)
train_labels = np.load('data/training_labels.npy')
train_data = np.load('data/training_sentences.npy', allow_pickle = True)

BOW_Model = BagOfWords()

BOW_Model.build_vocabulary(train_data)

train_features = BOW_Model.get_features(train_data)
test_features = BOW_Model.get_features(test_data)

scaled_train_data, scaled_test_data = normalize_data(train_features, test_features, type='l2')

svm_model = svm.SVC(C = BOW_Model.vocabulary_length, kernel = 'linear')
svm_model.fit(scaled_train_data, train_labels)
predicted_labels = svm_model.predict(scaled_test_data)
accuracy = compute_accuracy(np.asarray(test_labels), predicted_labels)
f1_score = f1_score(np.asarray(test_labels), predicted_labels)
print("Accuracy: ", accuracy)
print("F1 score: ", f1_score)

print("WTF is this??\n ", classification_report(np.asarray(test_labels), predicted_labels))
coefs = np.squeeze(np.array(svm_model.coef_))
idx = np.argsort(coefs)
print('the first 10 negative words are', BOW_Model.vocabulary[:10])

print('the first 10 positive words are', BOW_Model.vocabulary[-10:])