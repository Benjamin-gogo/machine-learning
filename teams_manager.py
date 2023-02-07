import csv
import json
import os

from flask import Flask
TEAMS_JSON = 'teams.json'

def get_code(file_name, country):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[0] == country:
                return row[1]
    return "mp" #drapeau par défaut

class TeamManager:

    def getTeams(dataframe):
        #Si le JSON existe déjà, pas besoin de tout reparcourir
        if os.path.exists(TEAMS_JSON):
            with open(TEAMS_JSON, 'r') as file:
                return json.load(file)


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
                flag_url = "https://flagcdn.com/16x12/"+get_code("code_countries.csv", h_country)+".png"

                countries[h_country] = {
                    "name": h_country,
                    "flag": flag_url
                }


            if teamsColumns[awayColumn][index] not in countries:
                a_country = teamsColumns[awayColumn][index]
                flag_url = "https://flagcdn.com/16x12/"+get_code("code_countries.csv", a_country)+".png"

                countries[a_country] = {
                    "name": a_country,
                    "flag": flag_url
                }

        with open(TEAMS_JSON, "w") as file:
            json.dump(countries, file)

        return json.dumps(countries, ensure_ascii=False).encode('utf8')
