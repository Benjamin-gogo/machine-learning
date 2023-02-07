import json
import os
import pickle

from flask import abort

import main
from csv_converter import CsvConverter
from main import FILE_MODEL
from teams_manager import TeamManager

#TEAMS = TeamManager.getTeams(CsvConverter.CLEAN_DATASET)
#def match(home, away):#
#    if home not in TEAMS or away not in TEAMS:
#        abort(404, "Team not found")

#    if os.path.exists(main.FILE_MODEL):
#        with open(main.FILE_MODEL, 'rb') as file:
#            mlp = pickle.load(file)#

    #else:
     #   abort(405, "Please, train again the model to predict the match")

    #return json.dumps("cool")

    #winner = None
    #return winner

if __name__ == '__main__':
    print("hello")