import pandas as pd
import numpy as np


class CsvConverter:
    def pd_read(file):
        try:
            data = pd.read_csv(file)
            print("Lecture du fichier CSV en cours...")
            return data

        except Exception as err:
            print(f"Le dataset {file} n'existe pas \n"
                  f"{err=}, {type(err)=}")
            exit(0)

    def np_read(file):
        try:
            data = np.loadtxt(file)
            print("Lecture du fichier CSV en cours...")
            return data

        except Exception as err:
            print(f"Le dataset {file} n'existe pas \n"
                  f"{err=}, {type(err)=}")
            exit(0)