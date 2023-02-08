from csv_converter import CsvConverter
from teams_manager import TeamManager

# CONSTS
FILE_MODEL = "mlp.dat"
INITIAL_DATASET = "match_world_cup.csv"
CLEAN_DATASET = "clean_match_world_cup.csv"


# GLOBAL FUNCTIONS
def get_initial_df(mode=0):
    if mode == 1:  # return np
        return CsvConverter.np_read(INITIAL_DATASET)
    return CsvConverter.pd_read(INITIAL_DATASET)


def get_clean_df(mode=0):
    if mode == 1:  # return np
        return CsvConverter.np_read(CLEAN_DATASET)
    return CsvConverter.pd_read(CLEAN_DATASET)


def get_teams():
    return TeamManager.getTeams(get_initial_df())
