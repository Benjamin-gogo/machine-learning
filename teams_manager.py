import csv
import json
import os

TEAMS_JSON = "teams.json"

# get last stats
def get_team_stats(df, team_name):
    for i in df.index[::-1]:
        row = df.iloc[i]

        if row['home_team'] == team_name:
            return (row['home_team_goalkeeper_score'],
                    row['home_team_mean_defense_score'],
                    row['home_team_mean_midfield_score'],
                    row['home_team_mean_offense_score'],
                    int(row['home_team_fifa_rank']))

        if row['away_team'] == team_name:
            return (row['away_team_goalkeeper_score'],
                    row['away_team_mean_defense_score'],
                    row['away_team_mean_midfield_score'],
                    row['away_team_mean_offense_score'],
                    int(row['away_team_fifa_rank']))


def get_code(file_name, country):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] == country:
                return row[1]
    return "mp"  # drapeau par défaut


def load_teams_from_dataframe(dataframe):
    homeColumn = "home_team"
    awayColumn = "away_team"

    if homeColumn and awayColumn not in dataframe[1:1]:  # Vérifie si le nom des colonnes existe bien
        print("Erreur sur le nom des colonnes !")
        exit(0)

    teamsColumns = dataframe[[homeColumn, awayColumn]]
    countries = {}

    for index in range(len(teamsColumns)):

        if teamsColumns[homeColumn][index] not in countries:
            h_country = teamsColumns[homeColumn][index]
            flag_url = "https://flagcdn.com/56x42/" + get_code("code_countries.csv", h_country) + ".png"
            gk, d, m, o, f = get_team_stats(dataframe, h_country)

            countries[h_country] = {
                "name": h_country,
                "flag": flag_url,
                "mean_goalkeeper": gk,
                "mean_defense": d,
                "mean_midfield": m,
                "mean_offense": o,
                "fifa_rank": f
            }

        if teamsColumns[awayColumn][index] not in countries:
            a_country = teamsColumns[awayColumn][index]
            flag_url = "https://flagcdn.com/56x42/" + get_code("code_countries.csv", a_country) + ".png"
            gk, d, m, o, f = get_team_stats(dataframe, a_country)

            countries[a_country] = {
                "name": a_country,
                "flag": flag_url,
                "mean_goalkeeper": gk,
                "mean_defense": d,
                "mean_midfield": m,
                "mean_offense": o,
                "fifa_rank": f
            }

    with open(TEAMS_JSON, "w", encoding='utf8') as file:
        json.dump(countries, file, ensure_ascii=False)


class TeamManager:

    def getTeams(initial_df):
        # Si le JSON existe déjà, pas besoin de tout reparcourir
        if os.path.exists(TEAMS_JSON):
            with open(TEAMS_JSON, 'r', encoding='utf8') as file:
                return json.load(file)

        else:
            load_teams_from_dataframe(initial_df)
            with open(TEAMS_JSON, 'r', encoding='utf8') as file:
                return json.load(file)
