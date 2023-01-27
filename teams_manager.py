from flask import Flask

class TeamManager:

    def getTeams(dataframe):

        homeColumn = "home_team"
        awayColumn = "away_team"

        if homeColumn and awayColumn not in dataframe[1:1]:  # Vérifie si le nom des colonnes existe bien
            print("Erreur sur le nom des colonnes !")
            exit(0)

        teamsColumns = dataframe[[homeColumn, awayColumn]]
        teams = []

        for index in range(len(teamsColumns)):
            if teamsColumns[homeColumn][index] not in teams:
                teams.append(teamsColumns[homeColumn][index])

            if teamsColumns[awayColumn][index] not in teams:
                teams.append(teamsColumns[awayColumn][index])

        return teams
