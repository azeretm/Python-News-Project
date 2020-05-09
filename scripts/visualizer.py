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

    def __init__(self, files=[], verbose=False, dropna=False):

        self.verbose = verbose
        self.dropna = dropna
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
            df = pd.read_csv(file[1], sep=",")
            df["source"] = file[0]
            
            data = pd.concat([data, df], ignore_index=True)

            if self.verbose:
                print("Data from %s successfully uploaded." % file[1])
        
        if self.dropna:
            data = data.dropna().copy()

        return data


    def visualizerDateRange(self, get_range=True, set_range=False):
        '''
            Gets/sets the range of records for which the dates overlap
        '''
        
        data = self.data
        grouped = data[["source", "date"]].groupby(["source"])
    
        # Gets min common date
        min_dates = grouped.min()
        date_from = max(min_dates["date"])
        
        # Gets max common date
        max_dates = grouped.max()
        date_to = min(max_dates["date"])
        
        # Crops data to fit only the range of dates which overlap
        if set_range is True:
            data = data[(data["date"] >= date_from) & (data["date"] <= date_to)]    
            
            if self.verbose:
                print("Data were successfully cropped and range from %s to %s." % (date_from, date_to))
        
        # Returns the range if requested
        if get_range is True:
            return (date_from, date_to)
