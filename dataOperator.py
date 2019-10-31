# -*- coding: utf-8 -*-
# import module requests
import requests

# =============================================================================
# # define data file web locations
# Dublin_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly532.csv'
# Cork_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly3904.csv'
# Shannon_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly518.csv'
# Knock_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly4935.csv'
# 
# # fetching csv files
# Dublin_Airport_data = requests.get(Dublin_Airport_data_url)
# Cork_Airport_data_url = requests.get(Cork_Airport_data_url)
# Shannon_Airport_data_url = requests.get(Shannon_Airport_data_url)
# Knock_Airport_data_url = requests.get(Knock_Airport_data_url)
# 
# # store files
# open('Dublin_Airport_data.csv', 'wb').write(Dublin_Airport_data.content)
# open('Cork_Airport_data_url.csv', 'wb').write(Cork_Airport_data_url.content)
# open('Shannon_Airport_data_url.csv', 'wb').write(Shannon_Airport_data_url.content)
# open('Knock_Airport_data_url.csv', 'wb').write(Knock_Airport_data_url.content)
# =============================================================================
    


# =============================================================================
# class DataOperator:
#     '''
#     This class contains a set of basic functions used for data operation:
#         1. download data file from web.
#         2. save data to local file system
#         ... ...
#     '''
#     def dowmloadFile(self, url):
#         '''
#         Download data files from web
#         
#         Parameters
#         ----------
#         url : str
#             the web link of the web which contains resource data
#         
#         Returns
#         -------
#         str
#             the content of the file downloaded
#         '''
#         return requests.get(url).content
#     
#     def saveFile(self, content, path):
#         '''
#         save data to a file locally
#         
#         Parameters
#         ----------
#         content : str
#             the data content need write to a file
#         path : str
#             specify the location where to save the file
#         '''
#         open(path, 'w').write(content)
#     
# 
# 
# if __name__ == "__main__":
#     url = 'https://cli.fusio.net/cli/climate_data/webdata/mly532.csv'
#     path = 'dublin_test.csv'
#     obj = DataOperator()
#     obj.saveFile(obj.dowmloadFile(url), path)
# =============================================================================


with open('Dublin_Airport_data.csv', 'r') as dub_air:
    desc = dub_air.readlines()[19:]
    print(desc)
    print()
    print(type(''.join(desc)))
    open('t.csv', 'w').write(''.join(desc))
    
# =============================================================================
#     for line in dub_air.readlines()[20:]:
#         print(line.strip())
# =============================================================================
    
    