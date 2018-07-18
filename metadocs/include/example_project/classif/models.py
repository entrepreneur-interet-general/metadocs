"""
Module models in package ``classif``
"""

import random
import time


class LogisticRegressor(object):

    """Logistic ression model
    """

    def __init__(self, weights=None):
        """Initialize the LR

        Args:
            weights (list, optional): Defaults to None.
                Weights to start the training from,
        """

        self.weights = weights

    def train(self, X_train, Y_train, X_test, Y_test):
        """Train and validate the LR on a train and test dataset

        Args:
            X_train (np.array): Training data
            Y_train (np.array): Training labels
            X_test (np.array): Test data
            Y_test (np.array): Test labels
        """

        while True:
            print(1)
            time.sleep(1)
            if random.randint(0, 9) >= 5:
                break
