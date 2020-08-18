import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import f1_score

# load data
def load_data(path):
    data = []
    ids = []
    with open(path, mode = 'r', encoding = 'utf-8') as fin:
        document = fin.readlines()

    # read each line
    for line in document:
        id, sentence = line.split('\t')

        # remove spaces to the right of the string, in case there are more
        sentence = sentence.rstrip()

        # store the samples in data and the indexes in ids
        data.append(sentence)
        ids.append(id)
    data = np.array(data)
    ids = np.array(ids)
    return (ids, data)

class BagOfWords:

    def __init__(self):
        self.vocabulary = []
        self.vocabulary_length = 0

    # build vocabulary going through the data and storing the words without duplicates
    def build_vocabulary(self, data):
        self.vocabulary = [word for sentence in data
                           for word in sentence.split(' ')]
        self.vocabulary = list(set(self.vocabulary))
        self.vocabulary_length = len(self.vocabulary)
        self.vocabulary = np.array(self.vocabulary)

    # count occurrences of each word of the dictionary in each sample of the document
    def get_features(self, data):
        # create a dictionary which stores the words (keys) in vocabulary
        dictionary = dict(zip(self.vocabulary, range(self.vocabulary_length)))
        features = []
        for sentence in data:
            features_sentence = np.zeros([self.vocabulary_length])
            for word in sentence.split(' '):
                if word in dictionary:
                    features_sentence[[dictionary[word]]] += 1
            features.append(features_sentence)
        features = np.array(features)
        return features

# calculate accuracy
def compute_accuracy(gt_labels, predicted_labels):
    accuracy = np.sum(predicted_labels == gt_labels) / len(predicted_labels)
    return accuracy

## load data
id_train, train_samples = load_data('data/train_samples.txt')
id_train, train_labels = load_data('data/train_labels.txt')
id_validation, validation_samples = load_data('data/validation_samples.txt')
id_validation, validation_labels = load_data('data/validation_labels.txt')

## create vocabulary
BOW_Model = BagOfWords()
BOW_Model.build_vocabulary(train_samples)

## get the features for each document
train_features = BOW_Model.get_features(train_samples)
validation_features = BOW_Model.get_features(validation_samples)

## tranform data into discrete values

# set the number of intervals to which will divide the length of the continous intervals
num_bins = 200
stop = int(max(train_features.max(), validation_features.max()))
# return the intervals
bins = np.linspace(start = 0, stop = stop, num = num_bins)

# return for each element the corresponding interval
def values_to_bins(matrix, bins):
    matrix = np.digitize(matrix, bins)
    return matrix - 1
train_features_to_bins = values_to_bins(train_features, bins)
validation_features_to_bins = values_to_bins(validation_features, bins)

## define the model
naive_bayes_model = MultinomialNB()
# training the model
naive_bayes_model.fit(train_features_to_bins, train_labels)
# predict labels for validation data
predicted_validation_labels = naive_bayes_model.predict(validation_features_to_bins)
# calculate the accuracy for the validation set
accuracy = compute_accuracy(predicted_validation_labels, validation_labels)
print("Accuracy ", accuracy)

## F1 score for validation data
validation_labels = [int(label) for label in validation_labels]
predicted_validation_labels = [int(label) for label in predicted_validation_labels]
print('F1 score', f1_score(np.asarray(validation_labels), predicted_validation_labels))

## confusion matrix for validation data
def confusion_matrix(true, pred):
    num_classes = 2
    conf_matrix = np.zeros((num_classes, num_classes))

    for i in range(len(true)):
        conf_matrix[int(true[i]), int(pred[i])] += 1
    return conf_matrix
print('Confusion matrix:', confusion_matrix(validation_labels, predicted_validation_labels))

## load test data
id_test, test_samples = load_data('data/test_samples.txt')
# get features for test data
test_features = BOW_Model.get_features(test_samples)
# tranform test data into discrete values
test_features_to_bins = values_to_bins(test_features, bins)

# predict test labels
predicted_test_labels = naive_bayes_model.predict(test_features_to_bins)

## write submission
def submission(file, predictions, ids):
    with open(file, 'w') as fout:
        fout.write("id,label\n")
        for id, pred in zip(ids, predictions):
            fout.write(id + ',' + str(int(pred)) + '\n')
submission("submission.csv", predicted_test_labels, id_test)