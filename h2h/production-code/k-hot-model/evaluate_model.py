from sklearn.metrics import accuracy_score, classification_report
from get_data import condensed_name

def eval_accuracy(model, X_test, y_test):
    """
    Quick method that uses sklearn's metrics module to evaluate the accuracy
    for the model in relation to a given test set
    """
    y_pred = lr.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:",accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

def make_pred(model, home_team_players, away_team_players, feature_list):
    """ Separates data into train, test, and validation.

    Args:
        model: sklearn machine learning model
        home_team_players: list of NBA players (as strings) on the home team
        away_team_players: list of NBA players (as strings) on the away team
        feature_list: list of condensed player names in the same order as the
            columns of the features of the model's training set

    Returns:
        - predicted_probability: float in (0,1), representing the probability
        of the given training example being a home win
        - prediction: integer in {0,1}, representing the predicted class of the
        training example.

    Raises:
        None
    """
    inp = np.zeros(len(feature_list))
    for player in home_team_players:
        try:
            inp[feature_list.index(condensed_name(player))] = 1
        except ValueError:
            print("Name not found:", player)
    for player in away_team_players:
        try:
            inp[feature_list.index(condensed_name(player))] = 1
        except ValueError:
            print("Name not found:", player)
    return model.predict_proba(inp), model.predict(inp)
