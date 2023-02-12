import json
import os
import pickle
import random
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
    home_gk, home_d, home_m, home_o, home_f, home_tw, home_tl, home_td, home_tgs, home_tgc = get_team_stats(
        get_initial_df(), home)
    away_gk, away_d, away_m, away_o, away_f, away_tw, away_tl, away_td, away_tgs, away_tgc = get_team_stats(
        get_initial_df(), away)

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
    formatted_input[10] = home_tw
    formatted_input[11] = home_tl
    formatted_input[12] = home_td
    formatted_input[13] = away_tw
    formatted_input[14] = away_tl
    formatted_input[15] = away_td
    formatted_input[16] = home_tgs
    formatted_input[17] = home_tgc
    formatted_input[18] = away_tgs
    formatted_input[19] = away_tgc

    ind_home, ind_away = getIndexOfTeams(home, away)

    formatted_input[ind_home + 20] = 1
    formatted_input[ind_away + 20] = 1

    return formatted_input / 1000


def perform_match(home, away):
    TEAMS = TeamManager.getTeams()

    if home not in TEAMS or away not in TEAMS:
        abort(404, "Team not found")

    if os.path.exists(FILE_MODEL):
        with open(FILE_MODEL, 'rb') as file:
            mlp = pickle.load(file)

        inp = create_input(home, away)  # fonction qui permet de créer un input

        if 45 < round(100 * mlp.predict_proba([inp])[0][0], 2) < 55:
            win_info = 2
        else:
            win_info = int(mlp.predict([inp])[0])

        res = {"win_info": win_info,
               "home_percentage": round(100 * mlp.predict_proba([inp])[0][0], 2),
               "away_percentage": round(100 * (1 - mlp.predict_proba([inp])[0][0]), 2)}

        # print(json.dumps(res))
        return json.dumps(res)

    else:
        abort(405, "Please, train again the model to predict the match")


def perform_match_regressor(home, away):
    TEAMS = TeamManager.getTeams()

    if home not in TEAMS or away not in TEAMS:
        abort(404, "Team not found")

    if os.path.exists(REGRESSOR_MODEL):
        with open(REGRESSOR_MODEL, 'rb') as file:
            regressor = pickle.load(file)

        inp = create_input(home, away)  # fonction qui permet de créer un input
        print(regressor.predict([inp]))
        return json.dumps(regressor.predict([inp])[0])

    else:
        abort(405, "Please, train again the model to predict the match")

def calculating_points(team1, team2, result, tab_points):
    if result == 0:
        tab_points[team1] = tab_points[team1] + 3
    elif result == 1:
        tab_points[team2] = tab_points[team2] + 3
    else:
        tab_points[team1] = tab_points[team1] + 1
        tab_points[team2] = tab_points[team2] + 1

def world_cup_predict_winner():
    selected_teams = random.sample(TeamManager.getTeams(), 48)
    print(selected_teams)


def init_tab_points(teams):
    points = {}
    for team in teams:
        points[team] = 0

    return points

if __name__ == '__main__':
    # Liste des 32 équipes
    teams = ['France', 'Mali', 'Argentina', 'Brazil',
             'Austria', 'Colombia', 'Peru', 'Bolivia',
             'Poland', 'Portugal', 'Denmark', 'Spain',
             'Senegal', 'Zambia', 'Nigeria', 'Italy',
             'Guinea', 'Cameroon', 'Morocco', 'Belgium',
             'Algeria', 'Wales', 'Israel', 'Greece',
             'Turkey', 'Malta', 'Germany', 'Mexico',
             'USA', 'Tunisia', 'Togo', 'Ghana']
    # Mélanger les équipes aléatoirement
    random.shuffle(teams)

    poules = [teams[i:i + 4] for i in range(0, len(teams), 4)]
    results = []

    points = init_tab_points(teams)

    # Boucle pour jouer les matchs de qualification
    for poule in poules:
        for i in range(len(poule)):
            for j in range(i + 1, len(poule)):
                team1 = poule[i]
                team2 = poule[j]
                result = perform_match(team1, team2)
                calculating_points(team1, team2, json.loads(result)["win_info"], points)

                #print(team1, " vs ", team2, ": ", json.loads(result))

    print(points)

    teams_dicts = [dict(sorted(list(points.items())[i:i + 4], key=lambda x: x[1], reverse=True)) for i
                   in range(0, len(points), 4)]
    for i in range(len(teams_dicts)):
        teams_dicts[i].popitem()
        teams_dicts[i].popitem()

    print(teams_dicts)
    exit(0)

    # print(result)
    # print(f"{team1} vs. {team2}: ")
    print(points)
    exit(0)

    # Classer les équipes en fonction de leur nombre de points
    sorted_teams = sorted(points, key=points.get, reverse=True)
    print(sorted_teams)
    exit(0)
    # Les 8 premières équipes se qualifient pour les huitièmes de finale
    qualifying_teams = sorted_teams[:16]

    # Afficher les équipes qualifiées pour les huitièmes de finale
    print("Les équipes qualifiées pour les huitièmes de finale sont:")
    for team in qualifying_teams:
        print(team)


