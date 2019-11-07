# -*- coding: utf-8 -*-
# This file defines a data analyst class, each object stores all data from file
class DataAnalyst:
    '''
    This class represent a ata object stores all data separate by columns from
    the source file. Also contains several data operation functions.
    '''
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
   
    def get_value_based_on_year(self, attrs=[], cal=''):
        '''
        This method will calculate the max/min/meant attributes value 
        for each year.
        
        Parameters
        ----------
        attrs : list
            the list of attributes which want to get max value based on year
        cal : str
            the calculate method - max, min, avg or med (median)
        
        Returns
        -------
        result : list
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
                value = ''
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
                    value = (sum(vals_for_corrent_year)[5:7])/2
                # contruct the element of result and add it to list
                result_attr.append(attr+","+current_year+","+\
                                   str(round(value,2)))
            # append attr result to RESULT list
            result.append(result_attr)
        return result
    
    def get_value_based_on_year_with_month(self, attrs=[], cal=''):
        '''
        This method will calculate the max/min attributes value devided 
        by year. Fetch the walue with its month
        
        Parameters
        ----------
        attrs : list
            the list of attributes which want to get max value based on year
        cal : str
            the calculate method - max or min
        
        Returns
        -------
        result : list
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
            
                
        
if __name__ == "__main__":
    ana = DataAnalyst('cork_air_data.csv')
    attr = ['sun']
    re = ana.get_value_based_on_year_with_month(attr,'min')
    print(re)
