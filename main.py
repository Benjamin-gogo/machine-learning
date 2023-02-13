import os

from flask import Flask, request, abort
import pickle
from sklearn.metrics import confusion_matrix, mean_squared_error, accuracy_score, r2_score, mean_squared_log_error
import matches_manager as mm
from teams_manager import TeamManager
import json
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from consts import *

app = Flask(__name__)


@app.route('/')
def index():
    init_machine()
    return json.dumps('ENTRY POINT - OCTOPRONOS')


@app.route('/teams')
def countries():
    dataframe = get_initial_df()
    return TeamManager.getTeams(dataframe)


@app.route('/teams/<team>')
def team(team):
    return TeamManager.getTeamInfos(TeamManager, team)


@app.route('/match')
def match():
    home_team = request.args.get('home')
    away_team = request.args.get('away')
    res = mm.perform_match(home_team, away_team)
    return res


@app.route('/world_cup')
def world_cup():
    selected_teams = request.args.get('selected_teams')
    """selected_teams = str(['France', 'Mali', 'Argentina', 'Brazil','Austria', 'Colombia', 'Peru', 'Bolivia',
             'Poland', 'Portugal', 'Denmark', 'Spain',
             'Senegal', 'Zambia', 'Nigeria', 'Italy',
             'Guinea', 'Cameroon', 'Morocco', 'Belgium',
             'Algeria', 'Wales', 'Israel', 'Greece',
             'Turkey', 'Malta', 'Germany', 'Mexico',
             'USA', 'Tunisia', 'Togo', 'Ghana'])"""

    res = mm.world_cup_predict_winner(selected_teams)
    return json.dumps(res)


def init_machine():
    data = np.loadtxt(CLEAN_DATASET, skiprows=1, delimiter=',')

    mlp_inputs = data[:, :-1] / 1000
    mlp_outputs = data[:, -1]

    train_inputs, test_inputs, train_outputs, test_outputs = train_test_split(mlp_inputs, mlp_outputs, test_size=0.2)

    if os.path.exists(FILE_MODEL):
        with open(FILE_MODEL, 'rb') as file:
            mlp = pickle.load(file)
    else:
        mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, alpha=0.001, learning_rate_init=0.01)
        # mlp = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, alpha=0.001, learning_rate_init=0.01)
        # mlp = LogisticRegression(fit_intercept=True, intercept_scaling=2, max_iter=2000)
        # mlp = RandomForestClassifier(n_estimators=200)
        # mlp = SVC(random_state=1, shrinking=True, tol=0.0001)

        mlp.fit(train_inputs, train_outputs)
        with open(FILE_MODEL, 'wb') as file:
            pickle.dump(mlp, file)

    print(mlp.predict(test_inputs))
    # print(r2_score(expected_y, predicted_y))

    #plt.plot(mlp.loss_curve_)
    #plt.yscale('log')
    #plt.show()

    print(f'Training Classifier score: {100 * mlp.score(train_inputs, train_outputs):.2f}%')
    print(f'Test Classifier score    : {100 * mlp.score(test_inputs, test_outputs):.2f}%')
    # print(f'Mean Squared Error:  {mean_squared_error(test_outputs, mlp.predict(test_inputs)):.2f}%')
    print(f'Accuracy: {100 * accuracy_score(test_outputs, mlp.predict(test_inputs).round()): .2f}%')
    print(confusion_matrix(test_outputs, mlp.predict(test_inputs)))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
