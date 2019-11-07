# -*- coding: utf-8 -*-
# This is the main program of the asignment 1

# import DataOperator, DataAnalyst
from dataOperator import DataOperator
from dataAnalyst import DataAnalyst

# initial a DataOperator instance
operator = DataOperator()

# inistial base attributes
cork_airport_url = 'https://cli.fusio.net/cli/climate_data/webdata/ml04.csv'
shannon_airport_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly518.csv'
description = 'desc.csv'

# fetch full data for two airports and save to local file system
cork_air = 'cork_air.csv'
shan_air = 'shan_air.csv'
operator.save_file(operator.dowmload_file(cork_airport_url), cork_air)
operator.save_file(operator.dowmload_file(shannon_airport_url), shan_air)

# These two files contains data among different times.
# For the analysis purpose, I need the same time period data 
# ( from Jan, 1969 to Dec, 2018 ) 50 years data 
cork_air_data = 'cork_air_data.csv'
shan_air_data = 'shan_air_data.csv'
start = '1969,1'
end = '2018,12'
# fetch related data and sve it correctly
operator.save_file(operator.get_data(cork_air, start, end), cork_air_data)
operator.save_file(operator.get_data(shan_air, start, end), shan_air_data)

# fetch the header info
# (because two dataset have the same description data, and a header line,
#  here I just grep one of them) 
header = operator.get_description(cork_air, 'year,').split('\n')[-2]
print('header: \n'+header)

# =============================================================================
# year:  -  Year
# month: -  Month
# rain:  -  Precipitation Amount (mm)
# meant: -  Mean Air Temperature (C)
# maxtp: -  Maximum Air Temperature (C)	  
# mintp: -  Minimum  Air Temperature (C)	
# mnmax: -  Mean Maximum Temperature (C)
# mnmin: -  Mean Minimum Temperature (C)
# gmin:  -  Grass Minimum Temperature (C)
# wdsp:  -  Mean Wind Speed (knot)
# mxgt:  -  Highest Gust (knot)
# sun:   -  Sunshine duration (hours)
# ind:   -  Indicator
# header: year,month,meant,maxtp,mintp,mnmax,mnmin,rain,gmin,wdsp,maxgt,sun
# =============================================================================

# 
