import numpy as np

# Citire imagini
import glob
images = []
for file_path in glob.glob("images/*"):
    images.append(np.load(file_path))
images = np.array(images)

# Calcul suma pixeli toate imaginile
sumas = np.sum(images)
print(sumas)

# Calcul suma pixeli pentru fiecare imagine
suma = np.sum(images, axis = (1,2))
print(suma)

# Indexul imaginii cu suma maxima
index = np.where(suma == np.max(suma))
print(index[0])

# Imaginea medie + afisare
mean_image = np.mean(images, axis = 0)
from skimage import io
io.imshow(mean_image.astype(np.uint8))
# io.show()

# Deviatia standard
dev = np.std(images)
print(dev)

# Normalizare
norm = images - mean_image
norm /= dev

# Decupare
cropped = np.copy(images[:, 200:301, 280:401])