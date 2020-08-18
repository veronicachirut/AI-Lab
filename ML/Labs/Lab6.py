from sklearn.linear_model import LinearRegression, Ridge, Lasso
import numpy as np
from sklearn.utils import shuffle

# definirea modelelor
linear_regression_model = LinearRegression()
ridge_regression_model = Ridge(alpha = 1)
lasso_regression_model = Lasso(alpha = 1)

# calcularea valorii MSE si MAE
from sklearn.metrics import mean_squared_error, mean_absolute_error
# mse_value = mean_squared_error(y_true, y_pred)
# mae_value = mean_absolute_error(y_true, y_pred)

# load training data
training_data = np.load('data/training_data.npy')
prices = np.load('data/prices.npy')

# print the first 4 samples
print('The first 4 samples are:\n ', training_data[:4])
print('The first 4 prices are:\n ', prices[:4])

# shuffle
training_data, prices = shuffle(training_data, prices, random_state = 0)