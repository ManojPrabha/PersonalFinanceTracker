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
    pandaDf = pd.read_csv(Inputfile)
    #removed unnecessary whitespace from python
    pandaDf.columns = pandaDf.columns.str.replace(' ', '')
    return pandaDf

