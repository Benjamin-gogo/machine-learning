import os
from cmath import sqrt
import numpy as np
from flask import Flask, request, abort
import pickle
from sklearn.metrics import confusion_matrix, mean_squared_error, accuracy_score, r2_score, mean_squared_log_error
from sklearn.preprocessing import LabelEncoder

import teams_manager
from csv_converter import CsvConverter
import matches_manager as mm
from teams_manager import TeamManager
import json
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
from consts import *

app = Flask(__name__)


@app.route('/')
def index():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    data = np.loadtxt(CLEAN_DATASET, skiprows=1, delimiter=',')

    mlp_inputs = data[:, :-4] / 100
    mlp_outputs = data[:, -1]

    train_inputs, test_inputs, train_outputs, test_outputs = train_test_split(mlp_inputs, mlp_outputs, test_size=0.2)

    mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=10000, alpha=0.0001)

    mlp.fit(train_inputs, train_outputs)
    with open(FILE_MODEL, 'wb') as file:
        pickle.dump(mlp, file)

    print(f'Training Classifier score: {100 * mlp.score(train_inputs, train_outputs):.2f}%')
    print(f'Test Classifier score    : {100 * mlp.score(test_inputs, test_outputs):.2f}%')
    print(f'Mean Squared Error:  {mean_squared_error(test_outputs, mlp.predict(test_inputs)):.2f}%')
    print(f'Accuracy: , {100 * accuracy_score(test_outputs, mlp.predict(test_inputs).round()): .2f}%')
    print(confusion_matrix(test_outputs, mlp.predict(test_inputs)))
