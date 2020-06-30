from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from joblib import dump
import numpy as np

def train_test_val_split(train, val, test, X, y, random_state = None):
    """ Separates data into train, test, and validation.

    Args:
        train: float in range (0,1). Percentage of X that will be the training
            set.
        val: float in range [0,1). Percentage of X that will be the validation
            set.
        test: float in range (0,1). Percentage of X that will be the test
            set.
        X: numpy array of dimension:
            [number_of_data_points, number_of_features]
        y: numpy array of dimension:
            [number_of_data_points, 1]
        random_state: int, in case you want reproducibility

    Returns:
        - X_train: numpy array of dimension:
            [number_of_data_points*train, number_of_players]
        - y_train: numpy array of dimension:
            [number_of_data_points*train, 1]
        - X_val: numpy array of dimension:
            [number_of_data_points*val, number_of_players]
        - y_val: numpy array of dimension:
            [number_of_data_points*val, 1]
        - X_test: numpy array of dimension:
            [number_of_data_points*test, number_of_players]
        - y_test: numpy array of dimension:
            [number_of_data_points*test, 1]

    Raises:
        ValueError: If train, test, and validation don't add to 1, raises this
        error
    """
    if train+val+test != 1:
        raise ValueError("Train + Validation + Test don't add to 1")
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = test, random_state = random_state)
    if val != 0:
        X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=val/(1-test), random_state = random_state)
        return X_train, y_train, X_val, y_val, y_test, X_test
    return X_train, y_train, None, None, y_test, X_test


def random_forest(X_train, y_train, filename, random_state = None):
    """ Trains a vanilla random forest model and saves it.

    Args:
        X_train: numpy array of dimension:
            [number_of_training_examples, number_of_features]
        y_train: numpy array of dimension:
            [number_of_training_examples, 1]
        filename: str, should end in .joblib, allows model to be saved
        random_state: int, in case you want reproducibility

    Returns:
        - rf, instance of scikit-learn's `RandomForestClassifier`
    """
    rf = RandomForestClassifier(n_estimators = 150, verbose = 1, random_state = random_state)
    rf.fit(X_train, y_train)
    dump(rf, filename)
    return rf

def logistic_regression(X_train, y_train, filename, random_state = None):
    """ Trains a vanilla logistic regression model and saves it.

    Args:
        X_train: numpy array of dimension:
            [number_of_training_examples, number_of_features]
        y_train: numpy array of dimension:
            [number_of_training_examples, 1]
        filename: str, should end in .joblib, allows model to be saved
        random_state: int, in case you want reproducibility

    Returns:
        - rf, instance of scikit-learn's `RandomForestClassifier`
    """
    lr = LogisticRegression(random_state = random_state, verbose = 1, max_iter = 100000)
    lr.fit(X_train, y_train)
    dump(lr, filename)
    return lr
