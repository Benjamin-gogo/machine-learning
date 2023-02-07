import os
from cmath import sqrt
import numpy as np
from flask import Flask, request, abort
import pickle
from sklearn.metrics import confusion_matrix, mean_squared_error, accuracy_score

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

TEAMS_JSON = "teams.json"
FILE_MODEL = "mlp.dat"

app = Flask(__name__)


@app.route('/')
def index():
    return json.dumps('hello, world')


@app.route('/countries')
def countries():
    dataframe = CsvConverter.pd_read(CsvConverter.INITIAL_DATASET)
    return TeamManager.getTeams(dataframe)

@app.route('/reload-teams')
def loadTeams():
    dataframe = CsvConverter.pd_read(CsvConverter.INITIAL_DATASET)
    teams_manager.load_teams_from_dataset(dataframe)
    if os.path.exists(TEAMS_JSON):
        abort(405, "An error when the program try to reload the teams.json")
    abort(200, "Les données ont bien été rechargées")


@app.route('/match')
def match():
    home_team = request.args.get('home')
    away_team = request.args.get('away')

    return mm.match(home_team, away_team)


if __name__ == '__main__':

    #app.run(host='0.0.0.0')

    data = np.loadtxt(CsvConverter.CLEAN_DATASET, skiprows=1, delimiter=',')

    inputs = data[:, :-1] / 100
    outputs = data[:, -1]

    train_inputs, test_inputs, train_outputs, test_outputs = train_test_split(inputs, outputs, test_size=0.3)

    if os.path.exists(FILE_MODEL):
        with open(FILE_MODEL, 'rb') as file:
            mlp = pickle.load(file)

        error = 0
        for i in range(len(inputs)):
            out = mlp.predict([inputs[i]])[0]
            error += (outputs[i] - out) * (outputs[i] - out)

        error = sqrt(error / len(inputs))
        print(f'RMS Error: {error}')

        #for i in range(5):
        #    showSample(inputs[i], round(n.apply(inputs[i])))

    else:
        mlp = MLPClassifier(hidden_layer_sizes=(5,), max_iter=10000)
        mlp.fit(train_inputs, train_outputs)

        plt.plot(mlp.loss_curve_)
        plt.yscale('log')
        plt.show()

        with open(FILE_MODEL, 'wb') as file:
            pickle.dump(mlp, file)

        print(f'Training score: {100 * mlp.score(train_inputs, train_outputs):.2f}%')
        print(f'Test score    : {100 * mlp.score(test_inputs, test_outputs):.2f}%')

        print(confusion_matrix(test_outputs, mlp.predict(test_inputs)))

        # Effectuer des prédictions sur les données de test
        y_pred = mlp.predict(test_inputs)


        # Évaluer la performance du modèle
        mse = mean_squared_error(test_outputs, y_pred)
        print("Mean Squared Error:", mse)
        acc = accuracy_score(test_outputs, y_pred.round())
        print("Accuracy:", acc)
