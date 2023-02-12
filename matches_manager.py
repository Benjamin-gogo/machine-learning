import ast
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

def default_teams():
    return ['France', 'Mali', 'Argentina', 'Brazil',
             'Austria', 'Colombia', 'Peru', 'Bolivia',
             'Poland', 'Portugal', 'Denmark', 'Spain',
             'Senegal', 'Zambia', 'Nigeria', 'Italy',
             'Guinea', 'Cameroon', 'Morocco', 'Belgium',
             'Algeria', 'Wales', 'Israel', 'Greece',
             'Turkey', 'Malta', 'Germany', 'Mexico',
             'USA', 'Tunisia', 'Togo', 'Ghana']
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


def perform_match(home, away, option_draw=True):
    TEAMS = TeamManager.getTeams()

    if home not in TEAMS or away not in TEAMS:
        abort(404, "Team not found")

    if os.path.exists(FILE_MODEL):
        with open(FILE_MODEL, 'rb') as file:
            mlp = pickle.load(file)

        inp = create_input(home, away)  # fonction qui permet de créer un input

        if option_draw:
            if 45 < round(100 * mlp.predict_proba([inp])[0][0], 2) < 55:
                win_info = 2
            else:
                win_info = int(mlp.predict([inp])[0])
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

def init_tab_points(teams):
    points = {}
    for team in teams:
        points[team] = 0

    return points
def calculating_points(team1, team2, result, tab_points):
    if result == 0:
        tab_points[team1] = tab_points[team1] + 3
    elif result == 1:
        tab_points[team2] = tab_points[team2] + 3
    else:
        tab_points[team1] = tab_points[team1] + 1
        tab_points[team2] = tab_points[team2] + 1

def get_selected_teams(tab):
    #fonction qui converti le tableau passé en param vers un tab
    return tab

def world_cup_predict_winner(param_teams):
    teams = ast.literal_eval(param_teams)

    pools = get_pools(teams)
    qualified_teams_16 = get_16_teams_qualified(pools, teams)
    qualified_teams_8 = get_teams_qualified(qualified_teams_16, option_shuffle=True)
    qualified_teams_4 = get_teams_qualified(qualified_teams_8)
    qualified_teams_2 = get_teams_qualified(qualified_teams_4)
    winner = get_teams_qualified(qualified_teams_2)

    return winner


def get_pools(teams):
    random.shuffle(teams)
    pools = [teams[i:i + 4] for i in range(0, len(teams), 4)]
    return pools

def get_16_teams_qualified(pools, teams):
    points = init_tab_points(teams)

    # Boucle pour jouer les matchs de qualification et donner des points
    for poule in pools:
        for i in range(len(poule)):
            for j in range(i + 1, len(poule)):
                team1 = poule[i]
                team2 = poule[j]
                result = perform_match(team1, team2)
                calculating_points(team1, team2, json.loads(result)["win_info"], points)

    #trier les équipes par ordre décroissant dans chaque poule
    teams_dicts = [dict(sorted(list(points.items())[i:i + 4], key=lambda x: x[1], reverse=True)) for i
                   in range(0, len(points), 4)]

    #garder les deux meilleures équipes de chaque poule
    for i in range(len(teams_dicts)):
        teams_dicts[i].popitem()
        teams_dicts[i].popitem()

    #creer un tableau de 16 équipes
    res = []

    for td in teams_dicts:
        res += list(td.keys())

    return res

def get_teams_qualified(teams, option_shuffle = False):
    if option_shuffle:
        random.shuffle(teams)

    groups = [teams[i:i + 2] for i in range(0, len(teams), 2)]

    for group in groups:
        team1 = group[0]
        team2 = group[1]

        result = perform_match(team1, team2, option_draw=False)
        if result == 0:
            eliminated_team = team2
        else:
            eliminated_team = team1

        try:
            teams.remove(eliminated_team)
        except ValueError:
            print(f"{eliminated_team} n'existe pas.")

    return teams

if __name__ == '__main__':
    p = str(['France', 'Mali', 'Argentina', 'Brazil','Austria', 'Colombia', 'Peru', 'Bolivia',
             'Poland', 'Portugal', 'Denmark', 'Spain',
             'Senegal', 'Zambia', 'Nigeria', 'Italy',
             'Guinea', 'Cameroon', 'Morocco', 'Belgium',
             'Algeria', 'Wales', 'Israel', 'Greece',
             'Turkey', 'Malta', 'Germany', 'Mexico',
             'USA', 'Tunisia', 'Togo', 'Ghana'])

    print(p)
    winner = world_cup_predict_winner(p)
    print(winner)
