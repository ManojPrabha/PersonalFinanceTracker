###############################################################################
###############################################################################
# Manoj's Personal Finance Tracker
# Created: January 15, 2023
# Last Updated: January 15, 2023
# Version: 1.0
# Changes:
# v1.0 - added multi-page support
###############################################################################
import pandas as pd
import numpy as np
import time


def ReadCsvMontlyReport(Inputfile):
    pandaDf = pd.read_csv(Inputfile, on_bad_lines='skip')
    # Remove rows with inconsistent number of columns4
    print(f"Number of columns in the DataFrame: {len(pandaDf.columns)}")
    print(f"Number of rows in the DataFrame: {len(pandaDf)}")
    #removed unnecessary whitespace from python
    pandaDf.columns = pandaDf.columns.str.replace(' ', '')
    return pandaDf

