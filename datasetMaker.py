import pandas as pd
from consts import get_teams, get_initial_df, CLEAN_DATASET


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
    teams = get_teams()

    data = dataframe[
        ["home_team", "away_team", "home_team_score", "away_team_score", "shoot_out", "home_team_result",
         "home_team_fifa_rank", "away_team_fifa_rank", "home_team_goalkeeper_score", "away_team_goalkeeper_score",
         "home_team_mean_defense_score", "home_team_mean_offense_score", "home_team_mean_midfield_score",
         "away_team_mean_defense_score", "away_team_mean_offense_score", "away_team_mean_midfield_score"]]

    print("Copie en cours...")

    for current_team in teams:
        res = []
        winners = []
        binary_winners = []

        temp_df = pd.DataFrame()
        for i in range(len(data)):
            ht = data.loc[i, 'home_team']
            at = data.loc[i, 'away_team']
            wt = data.loc[i, 'home_team_result']

            if ht == current_team or at == current_team:
                res.append(1)
            else:
                res.append(0)

            if wt == "Win":
                winners.append(ht)
                binary_winners.append(0)  # HT WIN
            elif wt == "Lose":
                winners.append(at)
                binary_winners.append(1)  # AT WIN
            else:
                winners.append(wt)
                binary_winners.append(2)  # DRAW

        data_temp = {current_team: res}  # faire de la nouvelle colonne un dictionnaire
        temp_df = temp_df.assign(**data_temp)  # faire un dataframe temporaore
        data = data.join(temp_df)  # ajouter le nouveau dataframe a l'existant

    # si mode=1, winning_team=name / si mode=2,winning_team = 0,1,2
    MODE = 2
    if MODE == 1:
        data = data.assign(winning_team=winners)
    else:
        data = data.assign(winning_team=binary_winners)

    data.drop(data.columns[[0, 1, 2, 3, 4, 5]], axis=1,
              inplace=True)  # Supprimer les colonnes ou il y a des caractères str + les scores

    data.to_csv(CLEAN_DATASET, index=False)
    print("Fin de la création du nouveau dataset... ")
    exit(0)
