# Downloader
import os
import pandas as pd
import re
from datetime import datetime
from tqdm import tqdm


class Visualizer:
    '''
        Helper class for data visualization, handles the data upload
    '''

    def __init__(self, files=[], verbose=False):

        self.verbose = verbose
        self.data = self.uploadData(files)

        if self.verbose:
            print("Visualizer successfully initialized.")

    def uploadData(self, files):
        '''
            Handles data upload from the given files list
        '''
        if not files:
            raise Exception("Empty list passed.")
        
        if not isinstance(files, list):
            raise Exception("Variable files is not a list, it is %s." % type(files))

        data = pd.DataFrame()

        for file in tqdm(files):
            df = pd.read_csv(file, sep=",")

            data = pd.concat([data, df], ignore_index=True)

            if self.verbose:
                print("Data from %s successfully uploaded." % file)

        return data
