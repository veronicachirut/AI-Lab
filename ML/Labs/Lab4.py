import numpy as np
import matplotlib.pyplot as plt

class KnnClassifier:
    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels
    def classify_image(self, test_image, num_neighbors = 3, metric = 'l2'):
        if(metric == 'l1'):
            distances = np.sum(abs(self.train_images - test_image), axis = 1)
        elif(metric == 'l2'):
            distances = np.sqrt(np.sum((self.train_images - test_image) ** 2, axis = 1))
        else:
            print("Error! Metric {} is not defined!", format(metric))

        # Sortez distantele crescator si memorez indicii acestora
        sort_index = np.argsort(distances)

        # Ia indecsii celor mai mici num_neighbors vecini
        sort_index = sort_index[:num_neighbors]

        # Etichetele vecinilor care au cele mai mici num_neighbors distante
        nearest_labels = self.train_labels[sort_index]

        # Calculez numarul de aparitii al fiecarei etichete in cei mai apropiati vecini
        histc = np.bincount(nearest_labels)

        # Returnez indexul etichetei care are cele mai multe aparitii
        return np.argmax(histc)
    def classify_images(self, test_images, num_neighbors = 3, metric = 'l2'):
        num_test_images = test_images.shape[0]
        predicted_labels = np.zeros(num_test_images, np.int)

        for i in range(num_test_images):
            predicted_labels[i] = self.classify_image(test_images[i, :], num_neighbors = num_neighbors, metric = metric)
        return predicted_labels

def accuracy_score(y_true, y_pred):
    return (y_true == y_pred).mean()

def confusion_matrix(y_true, y_pred):
    num_classes = max(y_true.max(), y_pred.max())
    conf_matrix = np.zeros(num_classes+1, num_classes+1)

    for i in range(len(y_true)):
        conf_matrix[int(y_true[i]), int(y_pred[i])] += 1
    return conf_matrix

train_images = np.loadtxt('data/train_images.txt')
train_labels = np.loadtxt('data/train_labels.txt', 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')

classifier = KnnClassifier(train_images, train_labels)
predicted_labels = classifier.classify_images(test_images, 3, metric = 'l2')
accuracy = accuracy_score(predicted_labels, test_labels)
print("Accuracy for num_neighbors = 3 and metric = 'l2': ", accuracy)
np.savetxt('predictii_3nn_l2_mnist.txt', predicted_labels)

### 4 a ###
num_neighbors = [1, 3, 5, 7, 9]
accuracy = np.zeros(len(num_neighbors))

for i in range(len(num_neighbors)):
    predicted_labels = classifier.classify_images(test_images, num_neighbors = num_neighbors[i], metric = 'l2')
    accuracy[i] = accuracy_score(predicted_labels, test_labels)
print(accuracy)
np.savetxt('acuratete_l2.txt', accuracy)

plt.plot(num_neighbors, accuracy)
plt.xlabel('number of neighbors')
plt.ylabel('accuracy')
plt.show()

### 4 b ###
accuracy_l1 = np.zeros(len(num_neighbors))
for i in range(len(num_neighbors)):
    predicted_labels = classifier.classify_images(test_images, num_neighbors = num_neighbors[i], metric = 'l1')
    accuracy_l1[i] = accuracy_score(predicted_labels, test_labels)
print(accuracy_l1)
np.savetxt('acuratete_l1.txt', accuracy_l1)

accuracy_l2 = np.loadtxt('acuratete_l2.txt')

plt.plot(num_neighbors, accuracy_l1)
plt.plot(num_neighbors, accuracy_l2)
plt.gca().legend(('L1', 'L2'))
plt.xlabel('number of neughbors')
plt.ylabel('accuracy')
plt.show()