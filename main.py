# -*- coding: utf-8 -*-
'''
This is the main program for the assisment.
an interactable program  to analys weather data from cork & shannon airports 
'''
from lib import prepare_files, analysis_data, validate_input, linear_reg_analysis
from error import InputError

# initial data path
cork_air_data = 'cork_air_data.csv'
shan_air_data = 'shan_air_data.csv'

print('prepare required files:')
prepare_files()
print()
print('Welcome to the system, Here you can analysis weather attributes(see \
headers above) from last 50 years (1969 -2018) in cork & shannon airports.')

while (True):
    # initial a DataAnalyst instance
    ana_obj = None
    # loop fot the main program
    while(True):
        try:
            # choose which data set for analysising
            opt = input('please choose which airport(s) to analysis:\n\
            1. cork airport  2. shannon airport  3. compare attrs \n')
            validate_input(opt, ['1', '2', '3'])
            break
        except InputError as e:
            print('InputError: ',e)
    if opt == '1':
        analysis_data(cork_air_data, 'cork airport')
    elif opt == '2':
        analysis_data(shan_air_data, 'shannon airport')
    elif opt == '3':
        linear_reg_analysis(cork_air_data, shan_air_data)
    # handle exception if type wrong option
    while(True):
        try:
            # continue?
            flag = input('do you want to aontinue analysis ? (y/n)\n')
            validate_input(flag, ['y', 'yes', 'n', 'no'])
            break
        except InputError as e:
            print('InputError: ',e)
    if flag.lower() in ['y', 'yes']:
        print()
    elif flag.lower() in ['n', 'no']:
        print('bye - bye !')
        break
            
    

    


