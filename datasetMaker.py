import json

import numpy as np
import pandas as pd
from consts import get_initial_df, CLEAN_DATASET
from teams_manager import TeamManager, TEAMS_JSON


# Récupérer l'indice des équipes
def getIndexOfTeam(teams, team1, team2):
    ind1 = 0
    ind2 = 0

    for i in range(len(teams)):
        if teams[i] == team1:
            ind1 = i
        if teams[i] == team2:
            ind2 = i

    return ind1, ind2


# Mettre des 0 ou des 1 en fonction de si l'équipe à jouer ou non
def fill_blank_line(teams, playingTeam1, playingTeam2):
    size_of_blank_data = len(teams)
    res = []
    index1, index2 = getIndexOfTeam(teams, playingTeam1, playingTeam2)
    for index in range(size_of_blank_data):
        if index == index1 or index == index2:
            res.append(1)
        else:
            res.append(0)
    return res


# Retourner le nom de l'équipe gagnante
def getWinningTeam(home_team, away_team, win):
    if win == "Win":
        return [home_team]
    if win == "Lose":
        return [away_team]

    return ["Draw"]


# Programme principal
if __name__ == '__main__':

    dataframe = get_initial_df()
    teams = TeamManager.getTeams()

    data = dataframe[
        ["home_team", "away_team", "home_team_score", "away_team_score", "shoot_out", "home_team_result",
         "home_team_fifa_rank", "away_team_fifa_rank", "home_team_goalkeeper_score", "away_team_goalkeeper_score",
         "home_team_mean_defense_score", "home_team_mean_offense_score", "home_team_mean_midfield_score",
         "away_team_mean_defense_score", "away_team_mean_offense_score", "away_team_mean_midfield_score"]]

    print("Copie en cours...")

    data = data.assign(home_team_total_wins=np.zeros(len(data)),
                       home_team_total_lose=np.zeros(len(data)),
                       home_team_total_draw=np.zeros(len(data)),
                       away_team_total_wins=np.zeros(len(data)),
                       away_team_total_lose=np.zeros(len(data)),
                       away_team_total_draw=np.zeros(len(data)),
                       home_team_total_goals_scored=np.zeros(len(data)),
                       home_team_total_goals_conceded=np.zeros(len(data)),
                       away_team_total_goals_scored=np.zeros(len(data)),
                       away_team_total_goals_conceded=np.zeros(len(data)))

    #AJOUTER AU DATASET, les new colonnes pour améliorer l'apprentissage de la machine####
    for index, row in data.iterrows():
        ht = row["home_team"]
        at = row["away_team"]

        data.at[index, "home_team_total_wins"] = teams[ht]["nb_wins"]
        data.at[index, "home_team_total_lose"] = teams[ht]["nb_lose"]
        data.at[index, "home_team_total_draw"] = teams[ht]["nb_draw"]

        data.at[index, "away_team_total_wins"] = teams[at]["nb_wins"]
        data.at[index, "away_team_total_lose"] = teams[at]["nb_lose"]
        data.at[index, "away_team_total_draw"] = teams[at]["nb_draw"]

        data.at[index, "home_team_total_goals_scored"] = teams[ht]["nb_goals_scored"]
        data.at[index, "home_team_total_goals_conceded"] = teams[ht]["nb_goals_conceded"]

        data.at[index, "away_team_total_goals_scored"] = teams[at]["nb_goals_scored"]
        data.at[index, "away_team_total_goals_conceded"] = teams[at]["nb_goals_conceded"]

    for current_team in teams:
        nb_wins = 0
        nb_lose = 0

        res = []
        binary_winners = []

        temp_df = pd.DataFrame()
        for i in range(len(data)):
            ht = data.loc[i, 'home_team']
            at = data.loc[i, 'away_team']
            wt = data.loc[i, 'home_team_result']

            if ht == current_team or at == current_team:
                ### add data in json - 1 here ###
                res.append(1)
            else:
                res.append(0)

            if wt == "Win":
                binary_winners.append(0)  # HT WIN

            elif wt == "Lose":
                binary_winners.append(1)  # AT WIN

            else:
                binary_winners.append(2)  # DRAW

        data_temp = {current_team: res}  # faire de la nouvelle colonne un dictionnaire
        temp_df = temp_df.assign(**data_temp)  # faire un dataframe temporaore
        data = data.join(temp_df)  # ajouter le nouveau dataframe a l'existant

    ###add data in json - 2 here ###
    data = data.assign(winning_team=binary_winners)
    data.drop(data.columns[[0, 1, 2, 3, 4, 5]], axis=1, inplace=True)  # Supprimer les colonnes ou il y a des caractères str + les scores

    data.to_csv(CLEAN_DATASET, index=False)
    print("Fin de la création du nouveau dataset... ")
    exit(0)

### data in json - 1####

# if ht == current_team:
#    teams[current_team]["nb_goals_scored"] = teams[current_team]["nb_goals_scored"] + int(data.loc[i, 'home_team_score'])
#    teams[current_team]["nb_goals_conceded"] = teams[current_team]["nb_goals_conceded"] + int(data.loc[i,'away_team_score'])

# if at == current_team:
#    teams[current_team]["nb_goals_conceded"] = teams[current_team]["nb_goals_conceded"] + int(data.loc[i, 'home_team_score'])
#    teams[current_team]["nb_goals_scored"] = teams[current_team]["nb_goals_scored"] + int(data.loc[i, 'away_team_score'])


# if (ht == current_team and wt == "Win") or (at == current_team and wt == "Lose"):
#    teams[current_team]["nb_wins"] = teams[current_team]["nb_wins"] + 1
# elif (ht == current_team and wt == "Lose") or (at == current_team and wt == "Win"):
#    teams[current_team]["nb_lose"] = teams[current_team]["nb_lose"] + 1
# else:
#    teams[current_team]["nb_draw"] = teams[current_team]["nb_draw"] + 1


   ########### data in json - 2 ##########"
    #with open(TEAMS_JSON, "w", encoding='utf8') as file:
    #    json.dump(teams, file, ensure_ascii=False)