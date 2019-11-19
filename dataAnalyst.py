# -*- coding: utf-8 -*-
'''
This file defines a data analyst class, each object stores all data from file
and functions for calculation
'''

import sys
class DataAnalyst:
    '''
    This class represent a ata object stores all data separate by columns from
    the source file. Also contains several data operation functions.
    '''
    # initial a dictionary to store attributes
    attr_dic = {'a':'meant', 'b':'maxtp', 'c':'mintp', 'd':'mnmax',\
                'e':'mnmin', 'f':'rain', 'g':'gmin', 'h':'wdsp',\
                'i':'maxgt', 'j':'sun'}
    # initial a list to store headers
    attributes = ["year", "month", "meant", "maxtp", "mintp", "mnmax", \
             "mnmin", "rain", "gmin", "wdsp", "maxgt", "sun"]
    # initial lists
    year=[]
    month=[]
    meant=[]
    maxtp=[]
    mintp=[]
    mnmax=[]
    mnmin=[]
    rain=[]
    gmin=[]
    wdsp=[]
    maxgt=[]
    sun=[]
    # constructor
    def __init__(self, file=''):
        '''
        This is the constructor, reading data frpm the input file
        
        Parameters
        ----------
        file : str
            the file path where the target file are
        '''
        try:
            # read file and store data to lists
            with open (file, 'r') as file_data:
                for line in file_data:
                    _year,_month,_meant,_maxtp,_mintp,_mnmax,_mnmin,_rain,\
                    _gmin,_wdsp,_maxgt,_sun = line.split(',')
                    self.year.append(_year)
                    self.month.append(_month)
                    self.meant.append(float(_meant))
                    self.maxtp.append(float(_maxtp))
                    self.mintp.append(float(_mintp))
                    self.mnmax.append(float(_mnmax))
                    self.mnmin.append(float(_mnmin))
                    self.rain.append(float(_rain))
                    self.gmin.append(float(_gmin))
                    self.wdsp.append(float(_wdsp))
                    self.maxgt.append(float(_maxgt))
                    self.sun.append(float(_sun))
        except FileNotFoundError:
            print('Error:', file, 'does not exist')
            sys.exit(0)
        except IsADirectoryError:
            print('Error', file, 'is a directory')
            sys.exit(0)
        except PermissionError:
            print('Error: No permissions to read file', file)
            sys.exit(0)
   
    def get_value_based_on_year(self, attrs=[], cal=''):
        '''
        This method will calculate the max/min/avg/med (median) attributes value 
        for each year.
        
        Parameters
        ----------
        attrs : list
            the list of attributes which want to get max value based on year
        cal : str
            the calculate method - max, min, avg or med (median)
        
        Returns
        -------
        list
            the result in format:
            "attr, year, value"
        
        '''
        # initial return list (stores result)
        result = []
        # loop for each input attr
        for attr in attrs:
            # a list to store result for such attribute
            result_attr = []
            # get total number of years
            year_total = int(len(self.month)/12)
            # iterate each year
            for year in range(year_total):
                # get current year
                current_year = self.year[year*12]
                # calculate max value of such attribute
                # method getattr() used to get attr from object
                # reference: https://www.journaldev.com/16146/python-getattr
                vals_for_corrent_year = getattr(self,attr)[year*12:(year+1)*12]
                # apply different calculations based on 'cal'
                if cal.lower() == 'max':
                    value = max(vals_for_corrent_year)
                elif cal.lower() == 'min':
                    value = min(vals_for_corrent_year)
                elif cal.lower() == 'avg':
                    value = sum(vals_for_corrent_year)/12
                elif cal.lower() == 'med':
                    vals_for_corrent_year.sort()
                    # alreadly know there are 12 months in a year
                    # so, middle numbers locates index=5 and index=6
                    value = sum(vals_for_corrent_year[5:7])/2
                # contruct the element of result and add it to list
                result_attr.append(attr+","+current_year+","+\
                                   str(round(value,2)))
            # append attr result to RESULT list
            result.append(result_attr)
        return result
    
    def get_value_based_on_year_with_month(self, attrs=[], cal=''):
        '''
        This method will calculate the max/min attributes value divided by 
        year. Fetch the value with its month
        
        Parameters
        ----------
        attrs : list
            the list of attributes which want to get max value based on year
        cal : str
            the calculate method - max or min
        
        Returns
        -------
        list
            the result in format:
            "attr, year, month, value"
        
        '''
        # initial return list (stores result)
        result = []
        # loop for each input attr
        for attr in attrs:
            # a list to store result for such attribute
            result_attr = []
            # get total number of years
            year_total = int(len(self.month)/12)
            # iterate each year
            for year in range(year_total):
                # get current year
                current_year = self.year[year*12]
                # calculate max value of such attribute
                # method getattr() used to get attr from object
                # reference: https://www.journaldev.com/16146/python-getattr
                vals_for_corrent_year = getattr(self,attr)[year*12:(year+1)*12]
                # apply different calculations based on 'cal'
                if cal.lower() == 'max':
                    value = max(vals_for_corrent_year)
                elif cal.lower() == 'min':
                    value = min(vals_for_corrent_year)
                # fetch the index in order to get its month
                index = getattr(self,attr).index(value)
                # contruct the element of result and add it to list
                result_attr.append(attr+","+current_year+","+self.month[index]+\
                              ','+str(value))
            # append attr result to RESULT list
            result.append(result_attr)
        return result
    
    def get_month_frequency(self, months=[]):
        '''
        analysis the input months, analysis the frequency of occurrence 
        of its elements
        
        Parameters
        ----------
        data : list
            months need to calculate the element frequency of occurrence
        
        Returns
        -------
        list
            a sorted list, (month, the number such month appears)
            e.g. [('July', 22), ('August', 12), ('September', 6)
        
        '''
        # dictionary to store month and its appear times
        dic={}
        # a dictionary converts number to month
        number_to_month = {'1':'January', '2':'February', '3':'March', \
                           '4':'April', '5': 'May', '6':'June', '7':'July', \
                           '8':'August', '9':'September', '10':'October', \
                           '11':'November', '12':'December'}
        # loop for each input data
        for ele in months:
            # get current month (the key in dictionary)
            month = number_to_month.get(ele)
            # add month to result list, id exist then increase its value by 1
            if not month in dic.keys():
                dic[month] = 1
            else:
                dic[month] += 1
        # sort the disctionary by its calue
        return sorted(dic.items(), key= lambda kv: (kv[1], kv[0]), reverse=True)
    
    def get_attr(self, attr=''):
        '''
        get attribute list which attr name equal to attr
        
        Parameters
        ----------
        attr : str
            name of attribute
        
        Returns
        --------
        list
            required attr list
        '''
        return getattr(self, attr)
    
    
if __name__ == "__main__":
    ana = DataAnalyst('cork_air_data.csv')
    attr = ['sun']
    cal = 'med'
    attr_results = ana.get_value_based_on_year(attr, cal)
    print(attr_results)
# =============================================================================
#     for attr_result in attr_results:
#         # get its month
#         months = [result.split(',')[2] for result in attr_result]
#         print(f'for attribute: {attr_result[0].split(",")[0]}')
#         print(f'the soted frequency months: (with {cal} values)\
#               \n {ana.get_month_frequency(months)}')
# =============================================================================
