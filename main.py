from flask import Flask
import datasetMaker
from csv_converter import CsvConverter
from teams_manager import TeamManager
import json


app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps('hello, world')


@app.route('/countries')
def countries():
    dataframe = CsvConverter.pd_read(CsvConverter.INITIAL_DATASET)
    return json.dumps(TeamManager.getTeams(dataframe), ensure_ascii=False).encode('utf8')
