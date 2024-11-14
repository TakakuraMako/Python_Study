import requests
import re
import pandas as pd
from ftplib import FTP
ftp = FTP('ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/')
years = list(range(2000, 2004, 1))
url = 'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/isd-lite/'
# 545110-99999-2023
for y in years:
    url = url + str(y) + '/' + '545110-99999-' + str(y)

    break
