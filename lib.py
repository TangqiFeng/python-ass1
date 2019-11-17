# -*- coding: utf-8 -*-
# This module contains program setup function

# import DataOperator, DataAnalyst
from dataOperator import DataOperator
from dataAnalyst import DataAnalyst
from error import InputError
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import sqlite3
import base64

def append_to_file(content):
    '''
    append analysis text result to History_Record.txt
    
    Parameters
    ----------
    content : str
        new analysis result need to store
    '''
    # the record file is definately exit, do not need exception handle
    # append a record to record analysis results
    record_file= open("History_Record.txt","a+")
    record_file.write(f"{content} \n \n")
    record_file.close()
    print("result added to record file - History_Record.txt")

def convert_img(img):
    '''
    converting img to base64 string
    
    Parameters
    ----------
    img : str
        img location
    
    Return
    ---------
    str
        base64 string converted from imput img
    '''
    # because the file definately exit, so do not need exception handle
    with open(img, "rb") as img_file:
        return base64.encodebytes(img_file.read())

def save_data_to_db(name, img_str):
    '''
    save image string to database
    
    Parameters
    ----------
    name : str
        the image name
    img_str : str
        ba64 string of the image
    '''
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        sqlite_insert_query = """INSERT INTO ana_imgs
                          ('name', 'img')  VALUES  (?,?)"""
        data_tuple = (name, img_str)
        cursor.execute(sqlite_insert_query, data_tuple)
        print(f"image: {name} store to db successfully")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def prepare_files():
    '''
    set up the files: download files needed and get 1969-2018 - 50 years
    data and save to files for cork airport and shannon airport.
    And set up database, create table - ana-imgs for storing result images.
    '''
    # initial a DataOperator instance
    operator = DataOperator()
    
    # inistial base attributes
    cork_airport_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly3904.csv'
    shannon_airport_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly518.csv'
    
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
    
    # set up database, create table - ana-imgs for storing result images.
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        sqlite_create_table_query = '''CREATE TABLE ana_imgs (
                                id INTEGER PRIMARY KEY,
                                name text NOT NULL,
                                img text NOT NULL);'''
        cursor.execute(sqlite_create_table_query)
        print("table ana_img is created.")
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")
    
    # create a record file to record analysis results
    operator.save_file("This file containers history for analysis text result.\
                      \n \n \n", "History_Record.txt")
    print("record file - History_Record.txt created.")

def linear_reg_analysis(dataset1, dataset2):
    # initial the DataAnalyst object
    ana_obj1 = DataAnalyst(dataset1)
    ana_obj2 = DataAnalyst(dataset2)
    # let user select two attrs
    while(True):
        try:
            opt7 = input('please select attr(s):\n\
            a.meant b.maxtp c.mintp d.mnmax e.mnmin \n\
            f.rain g.gmin h.wdsp i.maxgt j.sun\n')
            if len(opt7) != 2:
                raise InputError(f'you must select two attrs, please try again.')
            for opt in opt7:
                validate_input(opt, ana_obj1.attr_dic.keys())
            break
        except InputError as e:
            print('InputError: ',e)
    # add two attrs from two datasets (combine toghther)
    attr1 = ana_obj1.attr_dic[opt7[0]]
    attr2 = ana_obj1.attr_dic[opt7[1]]
    attr1_set = ana_obj1.get_attr(attr1) + ana_obj2.get_attr(attr1)
    attr2_set = ana_obj1.get_attr(attr2) + ana_obj2.get_attr(attr2)
    plot_regression_line(attr1_set, attr2_set, attr1, attr2)


def analysis_data(dataset, loc):
    '''
    the main logic to analysis the data
    
    Parameters
    ----------
    dataset : str
        the data source path
    '''
    # initial the DataAnalyst object
    ana_obj = DataAnalyst(dataset)
    # dictionary to map inpit option and attributes
    attr_dic = ana_obj.attr_dic
    while(True):
        try:
            opt2 = input('please select attr(s):\n\
            a.meant b.maxtp c.mintp d.mnmax e.mnmin \n\
            f.rain g.gmin h.wdsp i.maxgt j.sun\n')
            for opt in opt2:
                validate_input(opt, attr_dic.keys())
            break
        except InputError as e:
            print('InputError: ',e)
    # inistial attes[]
    attrs = []
    # add attrs which user input
    for ele in opt2:
        attrs.append(attr_dic[ele])
    while(True):
        try:
            opt3 = input('please select analysis method:\n\
            1. analysis attr(s) value based on year\n\
            2. analysis attr(s) value based on year with month \n')
            validate_input(opt3, ['1','2'])
            break
        except InputError as e:
            print('InputError: ',e)
    if opt3 == '1':
        while(True):
            try:
                opt4 = input('please select calculation \n 1.max  2.min 3.avg 4.med\n')
                validate_input(opt4, ['1','2','3','4'])
                break
            except InputError as e:
                print('InputError: ',e)
        if opt4 == '1':
            show_result_value_based_on_year(ana_obj,attrs,'max',loc)
        elif opt4 == '2':
            show_result_value_based_on_year(ana_obj,attrs,'min',loc)
        elif opt4 == '3':
            show_result_value_based_on_year(ana_obj,attrs,'avg',loc)
        elif opt4 == '4':
            show_result_value_based_on_year(ana_obj,attrs,'med',loc)
    elif opt3 == '2':
        
        while(True):
            try:
                opt5 = input('please select calculation \n 1.max  2.min\n')
                validate_input(opt5, ['1','2'])
                break
            except InputError as e:
                print('InputError: ',e)
        if opt5 == '1':
            show_result_value_based_on_year_with_month(ana_obj,attrs,'max',loc)
        elif opt5 == '2':
            show_result_value_based_on_year_with_month(ana_obj,attrs,'min',loc)

def show_result_value_based_on_year(ana_obj, attrs, cal, loc):
    '''
    calculate the result (with input analyst object)
    for the max/min/avg/med attributes value for each year.
    
    Parameters
    ----------
    ana_obj : DataAnalyst
        a DataAnalyst object already loaded a data source
    attrs : list
        attributes need to analysis
    cal : str
        the calculate method - max, min, avg or med (median)
    '''
    title = 'attributes: ' + str(attrs) + ' with '+cal+' value '
    result = ana_obj.get_value_based_on_year(attrs, cal)
    record=f'past 50 years (1969-2018) {title} :\n {result}'
    print(record)
    # store the record
    append_to_file(record)
    while(True):
        try:
            opt6 = input('please select polt \n 1.bar chart  2.line chart 3.box plot\n')
            validate_input(opt6, ['1','2','3'])
            break
        except InputError as e:
            print('InputError: ',e)
    if opt6 == '1':
        draw_bar_chart(result,cal,loc)
    elif opt6 == '2':
        draw_line_chart(result,cal,loc)
    elif opt6 == '3':
        draw_box_plot(result,cal,loc)
    
def show_result_value_based_on_year_with_month(ana_obj, attrs, cal, loc):
    '''
    calculate the result (with input analyst object)
    for the max/min attributes value for each year with its month init.
    Also, Analysis shows which month contains that value mostly.
    
    Parameters
    ----------
    ana_obj : DataAnalyst
        a DataAnalyst object already loaded a data source
    attrs : list
        attributes need to analysis
    cal : str
        the calculate method - max, min
    '''
    title = 'past 50 years (1969-2018) attributes: ' + str(attrs) +\
    ' with '+cal+' value '
    sub_record =[]
    attr_results = ana_obj.get_value_based_on_year_with_month(attrs, cal)
    # loop the result to generate sub_records
    for attr_result in attr_results:
        # get its month
        months = [result.split(',')[2] for result in attr_result]
        sort_month = ana_obj.get_month_frequency(months)
        attr = attr_result[0].split(",")[0]
        sub_title = f'for attribute -> {attr}'
        sub_record.append(f'{sub_title}:\n{sort_month}')
        # generate a pie chart for that
        draw_pie_chart(sort_month, attr, cal, loc)
    re = '\n'.join(sub_record)
    record=f'{title}:\n {attr_results}:\n{re}'
    print(record)
    # store the record
    append_to_file(record)
    print('>>>>pie chart(s) img has saved to the file system.<<<<')
    
def validate_input(type_in, input_opt):
    '''
    check the in put is/not valid, if not, raising a exception - InputError
    
    Parameters
    ----------
    type_in : str
        the actual input read
    input_opt : list
        the valid accptable input options
    '''
    if not type_in.lower() in input_opt:
        raise InputError(f'input: {type_in} is not valid, please try again.')

def draw_bar_chart(data=[], cal='', loc=''):
    '''
    generate a bar chat using input data.
    
    Parameters
    ----------
    data : list
        input data used to create bar chart
    cal : str
        the calculate method - max, min, avg or med (median) 
    loc : str
        dataset location
    '''
    for attr in data:
       fig,ax =plt.subplots()
       attribute, dic = generate_data_for_year_value(attr)
       y_pos = list(range(10))
       title = f'{cal} value of {attribute} in {loc}, 2009~2018'
       ax.set_title(title)
       ax.set_yticks(y_pos)
       ax.set_yticklabels(dic.keys())
       ax.barh(y_pos, dic.values())
       fig.show()
       img_name = title+'_bar_chart.png'
       fig.savefig(img_name, bbox='tight')
       # save image to db
       # convert img to base64 string
       save_data_to_db(img_name, convert_img(img_name))
       
    print('>>>>line chart img(s) has saved to the file system.<<<<')

def draw_line_chart(data=[], cal='', loc=''):
    '''
    generate a line chat using input data.
    
    Parameters
    ----------
    data : list
        input data used to create line chart
    cal : str
        the calculate method - max, min, avg or med (median) 
    loc : str
        dataset location
    '''
    for attr in data:
       fig,ax =plt.subplots()
       attribute, dic = generate_data_for_year_value(attr)
       title = f'{cal} value of {attribute} in {loc}, 2009~2018'
       ax.set_title(title)
       ax.set_xlabel('year')
       ax.set_ylabel(attribute)
       years= [year for year in dic.keys()]
       vals= [val for val in dic.values()]
       ax.plot(years,vals)
       fig.show()
       img_name = title+'_line_chart.png'
       fig.savefig(img_name, bbox='tight')
       # save image to db
       # convert img to base64 string
       save_data_to_db(img_name, convert_img(img_name))
    print('>>>>line chart img(s) has saved to the file system.<<<<')


def draw_box_plot(data=[], cal='', loc=''):
    '''
    generate a box plot using input data.
    
    Parameters
    ----------
    data : list
        input data used to create box plot
    cal : str
        the calculate method - max, min, avg or med (median) 
    loc : str
        dataset location
    '''
    for attr in data:
       fig,ax =plt.subplots()
       attribute, dic = generate_data_for_year_value(attr)
       title = f'{cal} value of {attribute} in {loc}, 2009~2018'
       ax.set_title(title)
       ax.set_ylabel(attribute)
       ax.boxplot(dic.values())
       fig.show()
       img_name = title+'_box_plot.png'
       fig.savefig(img_name, bbox='tight')
       # save image to db
       # convert img to base64 string
       save_data_to_db(img_name, convert_img(img_name))
    print('>>>>box chart img(s) has saved to the file system.<<<<')
      
def draw_pie_chart(data=[], attr='', cal='', loc=''):
    '''
    generate a pie chart using input data.
    
    Parameters
    ----------
    data : list
        input data used to create pie chart
    cal : str
        the calculate method - max, min 
    loc : str
        dataset location
    '''
    months = []
    values = []
    for item in data:
       months.append(item[0])
       values.append(item[1])
    fig,ax =plt.subplots()
    title = f'month pct with {cal} value of {attr} in {loc}, 1969~2018'
    ax.set_title(title)
    ax.pie(values, labels=months, autopct="%.0f%%")
    fig.show()
    img_name = title+'_pie_chart.png'
    fig.savefig(img_name, bbox='tight')
    # save image to db
    # convert img to base64 string
    save_data_to_db(img_name, convert_img(img_name))
    print('>>>>pie chart img has saved to the file system.<<<<')

def generate_data_for_year_value(attrs=[]):
    '''
    convert data list to dictionary, only save last ten years data for each 
    attribute set.
    
    Parameters
    ----------
    attrs : list
        the input data need to convert to dictionary
    
    Returns
    -------
    attribute : str
        name of attr handeled of data list
    dic : dictionary
        result dictionary object convert from input list data
    '''
    # initial a empty dictionary
    dic = {}
    attribute = ''
    # loop each record in the list
    for item in attrs[-10:]:
        # save data to dictionary
        atr, year, value = item.split(',')
        attribute = atr
        dic[year] = float(value)
    return attribute, dic

def estimate_coef(x, y): 
    '''
    use Least Squares technique to estimate coefficients for 
    analysising.
    
    Parameters
    ----------
    x : list
        dataset of one attribute
    y : list
        dataset of another attribute
        
    Returns
    -------
    (b_0, b_1) : tuple
        b_0 and b_1 are regression coefficients and represent 
        y-intercept and slope of regression line respectively
    '''
    # number of observations/points 
    n = len(x) 
    # mean of x and y vector 
    m_x, m_y = sum(x)/len(x), sum(y)/len(y)
    # calculating cross-deviation and deviation about x 
    sum_xy=0
    sum_xx=0
    for _x,_y in zip(x,y):
        sum_xy += _x*_y
    for _x in x:
        sum_xx += _x*_x
    SS_xy = sum_xy - n*m_y*m_x 
    SS_xx = sum_xx - n*m_x*m_x 
    # calculating regression coefficients 
    b_1 = SS_xy / SS_xx 
    b_0 = m_y - b_1*m_x 
    return(b_0, b_1) 

def plot_regression_line(x, y, attr1, attr2): 
    '''
    generate a scatter plot with a regression line using 
    input data.
    
    Parameters
    ----------
    x : list
        dataset of one attribute (attr1)
    y : list
        dataset of another attributen (attr2)
    attr1 : str
        the name of dataset x
    attr2 : str
        the name of dataset y
    '''
    fig,ax =plt.subplots()
    title = f'relationship between {attr1} and {attr2}'
    ax.set_title(title)
    # estimating coefficients 
    b = estimate_coef(x, y) 
    print("Estimated coefficients:\nb_0 = {}  \nb_1 = {}"\
          .format(b[0], b[1]))
    # plotting the actual points as scatter plot 
    ax.scatter(x, y, color = "m", marker = ".", s = 30) 
    # predicted response vector 
    y_pred = []
    for _x in x:
        y_pred.append(b[0] + b[1]*_x)  
    # plotting the regression line 
    ax.plot(x, y_pred, color = "g")
    # putting labels 
    ax.set_xlabel(attr1) 
    ax.set_ylabel(attr2)
    # function to show plot
    fig.show()
    img_name = title+'_scatter.png'
    fig.savefig(img_name, bbox='tight')
    # save image to db
    # convert img to base64 string
    save_data_to_db(img_name, convert_img(img_name))
    print('>>>>pie chart img has saved to the file system.<<<<')

if __name__ == "__main__":
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [1, 3, 2, 5, 7, 8, 8, 9, 10, 12]
    plot_regression_line(x, y, 'one', 'two')
# =============================================================================
#     data = [['meant,1969,14.9', 'meant,1970,14.8', 'meant,1971,15.1', 'meant,1972,14.7', 'meant,1973,15.0', 'meant,1974,14.0', 'meant,1975,15.5', 'meant,1976,16.4', 'meant,1977,15.4', 'meant,1978,14.2', 'meant,1979,15.2', 'meant,1980,14.7', 'meant,1981,16.0', 'meant,1982,15.3', 'meant,1983,17.7', 'meant,1984,16.2', 'meant,1985,14.1', 'meant,1986,14.6', 'meant,1987,15.3', 'meant,1988,14.5', 'meant,1989,17.6', 'meant,1990,15.9', 'meant,1991,15.5', 'meant,1992,15.2', 'meant,1993,14.2', 'meant,1994,14.1', 'meant,1995,18.3', 'meant,1996,15.0', 'meant,1997,16.0', 'meant,1998,15.5', 'meant,1999,16.1', 'meant,2000,15.6', 'meant,2001,15.2', 'meant,2002,15.1', 'meant,2003,16.2', 'meant,2004,15.2', 'meant,2005,15.8', 'meant,2006,16.4', 'meant,2007,14.8', 'meant,2008,14.6', 'meant,2009,14.2', 'meant,2010,14.9', 'meant,2011,13.9', 'meant,2012,15.0', 'meant,2013,17.3', 'meant,2014,16.3', 'meant,2015,13.8', 'meant,2016,15.2', 'meant,2017,15.3', 'meant,2018,17.4']]
#     data2=[('July', 22), ('August', 12), ('June', 10), ('September', 6)]
#     draw_bar_chart(data,'max','cork airport')
#     draw_line_chart(data,'max','cork airport')
#     draw_box_plot(data,'max','cork airport')
#     draw_pie_chart(data2,'attr','max','cork airport')
# =============================================================================
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
