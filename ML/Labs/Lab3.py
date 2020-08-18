import numpy as np
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt

train_images = np.loadtxt('data/train_images.txt')
train_labels = np.loadtxt('data/train_labels.txt', 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')


### ---- 2 ----
num_bins = 5
bins = np.linspace(start = 0, stop = 255, num = num_bins)

def values_to_bins(matrix, bins):
    matrix = np.digitize(matrix, bins)
    return matrix - 1

train_images_to_bins = values_to_bins(train_images, bins)
test_images_to_bins = values_to_bins(test_images, bins)


### ---- 3 ----
naive_bayes_model = MultinomialNB()
naive_bayes_model.fit(train_images_to_bins, train_labels)
accuracy = naive_bayes_model.score(test_images_to_bins, test_labels)
print("Accuracy ", accuracy)


### ---- 4 ----
for num_bins in [3, 5, 7, 9, 11]:
    bins = np.linspace(start = 0, stop = 255, num = num_bins)
    test_images_to_bins = values_to_bins(test_images, bins)
    train_images_to_bins = values_to_bins(train_images, bins)

    naive_bayes_model.fit(train_images_to_bins, train_labels)
    accuracy = naive_bayes_model.score(test_images_to_bins, test_labels)
    print("Accuracy for num_bins = %s is %s" % (num_bins, accuracy))


### ---- 5 ----
num_bins = 11
bins = np.linspace(start = 0, stop = 255, num = num_bins)
train_images_to_bins = values_to_bins(train_images, bins)
test_images_to_bins = values_to_bins(test_images, bins)

naive_bayes_model.fit(train_images_to_bins, train_labels)
predicted_labels = naive_bayes_model.predict(test_images_to_bins)
misclasified_indices = np.where(predicted_labels != test_labels)[0]

for i in range(10):
    image = train_images[misclasified_indices[i], :]
    image = np.reshape(image, (28, 28))
    plt.imshow(image.astype(np.uint8), cmap = 'gray')
    plt.show()


### ---- 6 ----
def confusion_matrix(y_true, y_pred):
    num_classes = max(y_true.max(), y_pred.max())
    matrix = np.zeros((num_classes + 1, num_classes + 1))

    for i in range(len(y_true)):
        matrix[y_true[i], y_pred[i]] += 1
    return matrix
print(confusion_matrix(test_labels, predicted_labels))