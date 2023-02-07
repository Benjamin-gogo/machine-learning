from flask import Flask

class TeamManager:

    def getTeams(dataframe):

        homeColumn = "home_team"
        awayColumn = "away_team"

        if homeColumn and awayColumn not in dataframe[1:1]:  # Vérifie si le nom des colonnes existe bien
            print("Erreur sur le nom des colonnes !")
            exit(0)

        teamsColumns = dataframe[[homeColumn, awayColumn]]
        countries = {}

        for index in range(len(teamsColumns)):

            if teamsColumns[homeColumn][index] not in countries:
                countries[teamsColumns[homeColumn][index]] = {
                    "name": teamsColumns[homeColumn][index],
                    "flag": "https://flagcdn.com/16x12/fr.png"
                }

            if teamsColumns[awayColumn][index] not in countries:
                countries[teamsColumns[awayColumn][index]] = {
                    "name": teamsColumns[awayColumn][index],
                    "flag": "https://flagcdn.com/16x12/fr.png"
                }

        return countries
