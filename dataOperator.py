# -*- coding: utf-8 -*-
'''
This file defines a data operator class
contains data operation functions
1. download file
2. save file
3. separate data
'''

# import module requests
import requests
from error import DownloadError
import sys

class DataOperator:
    '''
    This class contains a set of basic functions used for data operation:
        1. download data file from web.
        2. save data to local file system
        3. get desc data (headers) of a data file
        4. get srpcific data with provided start/end signals. 
        ... ...
    '''
    def dowmload_file(self, url):
        '''
        Download data files from web
        
        Parameters
        ----------
        url : str
            the web link of the web which contains resource data
        
        Returns
        -------
        str
            the content of the file downloaded
        '''
        # decode method here converts bytes to string
        content=requests.get(url).content.decode("utf-8", "ignore")
        if content.startswith('<!'):
            raise DownloadError(url)
        return content
    
    def save_file(self, content, path):
        '''
        save data to a file locally
        
        Parameters
        ----------
        content : str
            the data content need write to a file
        path : str
            specify the location where to save the file
        '''
        try:
            open(path, 'w').write(content)
        except FileNotFoundError:
            print('Error:', path, 'does not exist')
            sys.exit(0)
        except IsADirectoryError:
            print('Error', path, 'is a directory')
            sys.exit(0)
        except PermissionError:
            print('Error: No permissions to read file', path)
            sys.exit(0)
    
    def get_description(self, file, end=''):
        '''
        get description data (headers) from a csv file
        
        Parameters
        ----------
        file : str
            the file path where the target file are
        end : str
            the start-data of end line of desc data (headers)
        
        Returns
        -------
        str
            the content of the description part of the file
        '''
        # initial a list to store description data
        desc_data = []
        try:
            # read the file
            with open(file, 'r') as file_data:
                # loop each line to feed the desc_data
                for line in file_data:
                    # check the line is/not end line
                    if not line.startswith(end):
                        # append desc data to list desc_data
                        desc_data.append(line)   
                    else:
                        # append the last line to desc_data
                        desc_data.append(line)
                        # terminate the loop
                        break
        except FileNotFoundError:
            print('Error:', file, 'does not exist')
            sys.exit(0)
        except IsADirectoryError:
            print('Error', file, 'is a directory')
            sys.exit(0)
        except PermissionError:
            print('Error: No permissions to read file', file)
            sys.exit(0)
        print(f'{len(desc_data)} lines description data in the file')
        # return desx data as a string
        return ''.join(desc_data)
    
    def get_data(self, file, start='', end=''):
        '''
        get partial data from a file
        
        Parameters
        ----------
        file : str
            the file path where the target file are
        start : str
            the start-data of the start line
        end : str
            the start-data of the end line
        
        Returns
        -------
        str
            the content of the partial data of the file
        '''
        # initial a list to store valid data
        data = []
        try:
            # read the file
            with open(file, 'r') as file_data:
                # set a flag to indicate whether the line is needed 
                # (between the start and the end line)
                flag = False
                # loop each line of the file
                for line in file_data:
                    # check the line is/not start line
                    if line.startswith(start):
                        # chenge flag to True, cause data is neede from this line
                        flag = True
                    # check the line is/not end line
                    if line.startswith(end):
                        # append the last line to data[]
                        data.append(line)
                        # chenge flag to False
                        flag = False
                    if flag:
                        # append the line to data[]
                        data.append(line)
        except FileNotFoundError:
            print('Error:', file, 'does not exist')
            sys.exit(0)
        except IsADirectoryError:
            print('Error', file, 'is a directory')
            sys.exit(0)
        except PermissionError:
            print('Error: No permissions to read file', file)
            sys.exit(0)
        print(f'get {len(data)} lines data from the file -> {file}')
        # return data as a string
        return ''.join(data)






# =============================================================================
# if __name__ == "__main__":
#     # inistial a instance of DataOperator
#     obj = DataOperator()
#     dub_air = 'dublin_air.csv'
#     dub_air_data = 'dublin_air_data.csv'
#     start = '1969,1'
#     end = '2018,12'
#     # fetch partial data
#     obj.save_file(obj.get_data(dub_air, start, end), dub_air_data)
# =============================================================================
    
if __name__ == "__main__":
    # set up the urls and file locations
    cork_air_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly3904.csv'
    cork_air = 'cork_air.csv'
    cork_air_desc = 'cork_air_desc.csv'
    # as is known, the last desc line start with 'years,'
    validHead = 'year,'
    # inistial a instance of DataOperator
    obj = DataOperator()
    # download the file and save locally
    try:   
        obj.save_file(obj.dowmload_file(cork_air_url), cork_air)
    except DownloadError as e:
        print('DownloadError: nothing dowmloaded, please check the url:',e)

# =============================================================================
#     # fetch desc data and save locally
#     cork_air_desc_str = obj.get_description(cork_air, validHead)
#     print(cork_air_desc_str)
#     obj.save_file(cork_air_desc_str, cork_air_desc)
# =============================================================================


# =============================================================================
# # simple step to download data
# # define data file web locations
# Cork_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly3904.csv'
# Shannon_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly518.csv'
# 
# # fetching csv files
# Cork_Airport_data_url = requests.get(Cork_Airport_data_url)
# Shannon_Airport_data_url = requests.get(Shannon_Airport_data_url)
# 
# # store files
# open('Cork_Airport_data_url.csv', 'w').write(Cork_Airport_data_url.content.decode('ASCII'))
# open('Shannon_Airport_data_url.csv', 'w').write(Shannon_Airport_data_url.content.decode('ASCII'))    
# =============================================================================


# simple step to get description data
# =============================================================================
# # open one source file
# with open('Cork_Airport_data.csv', 'r') as cork_air:
#     # remove the description lines up in the file
#     # two list to store desc data and valid data
#     desc_data = []
#     valid_data = []
#     # loop each line to feed the index
#     for line in cork_air:
#         if not line.startswith('year,'):
#             # append desc data to list desc_data
#             desc_data.append(line)   
#         else:
#             # save the header line
#             header = line
#             # append rest data to list calid_data
#             valid_data.extend(cork_air.readlines())
#             
#     print(f'{len(desc_data)} lines description data in the file')
#     desc_data_str = ''.join(desc_data)
#     valid_data_str = ''.join(valid_data)
#     print('description: \n',desc_data_str)
#     print('header : \n', header)
#     print(type(valid_data))
#     # write valid data to a new file called t.csv
#     open('t.csv', 'w').write(valid_data_str)
# =============================================================================
    
    
    
    