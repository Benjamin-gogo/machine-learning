import os
from cmath import sqrt

import numpy as np
from flask import Flask
import pickle
from sklearn.metrics import confusion_matrix, mean_squared_error, accuracy_score

import datasetMaker
from csv_converter import CsvConverter
from teams_manager import TeamManager
import json
from sklearn import datasets
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

FILE_MODEL = "mlp.dat"
app = Flask(__name__)


@app.route('/')
def index():
    return json.dumps('hello, world')


@app.route('/countries')
def countries():
    dataframe = CsvConverter.pd_read(CsvConverter.INITIAL_DATASET)
    return TeamManager.getTeams(dataframe)


if __name__ == '__main__':

    app.run(host='0.0.0.0')

    data = np.loadtxt(CsvConverter.CLEAN_DATASET, skiprows=1, delimiter=',')

    inputs = data[:, :-1]
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
