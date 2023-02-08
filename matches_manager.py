import json
import os
import pickle

from flask import abort

from consts import get_empty_input
from csv_converter import CsvConverter
from datasetMaker import getIndexOfTeam
from teams_manager import TeamManager, get_team_stats
from consts import *


def getIndexOfTeams(home, away):
    teams = TeamManager.getTeams()
    ind1 = 0
    ind2 = 0
    i = 0

    for t in teams:
        if t == home:
            ind1 = i
        if t == away:
            ind2 = i
        i = i + 1

    return ind1, ind2


def create_input(home, away):
    formatted_input = get_empty_input()
    home_gk, home_d, home_m, home_o, home_f = get_team_stats(get_initial_df(), home)
    away_gk, away_d, away_m, away_o, away_f = get_team_stats(get_initial_df(), away)

    formatted_input[0] = home_f
    formatted_input[1] = away_f
    formatted_input[2] = home_gk
    formatted_input[3] = away_gk
    formatted_input[4] = home_d
    formatted_input[5] = home_o
    formatted_input[6] = home_m
    formatted_input[7] = away_d
    formatted_input[8] = away_o
    formatted_input[9] = away_m

    ind_home, ind_away = getIndexOfTeams(home, away)

    formatted_input[ind_home + 10] = 1
    formatted_input[ind_away + 10] = 1

    return formatted_input / 100


def perform_match(home, away):
    TEAMS = TeamManager.getTeams()

    if home not in TEAMS or away not in TEAMS:
        abort(404, "Team not found")

    if os.path.exists(FILE_MODEL):
        with open(FILE_MODEL, 'rb') as file:
            mlp = pickle.load(file)

        inp = create_input(home, away) #fonction qui permet de créer un input
        return json.dumps(mlp.predict([inp])[0])

    else:
        abort(405, "Please, train again the model to predict the match")

    # return json.dumps("cool")

    # winner = None
    # return winner


if __name__ == '__main__':
    #my_input = create_input("Bolivia", "Uruguay")
    perform_match("Bolivia", "Uruguay")

