# Downloader
import os
import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm


class Visualizer:
    '''
    '''

    def __init__(self, files=[], verbose=False):

        self.verbose = verbose
        self.data = self.uploadData(files)

        if self.verbose:
            print("Visualizer successfully initialized.")

    def uploadData(self, files):
        '''
        '''
        if not files:
            raise Exception("Empty list passed.")

        data = pd.DataFrame()

        for file in files:
            df = pd.read_csv(file, sep=",")

            data = pd.concat([data, df], ignore_index=True)

            if self.verbose:
                print("Data from %s successfully uploaded." % file)

        return data
