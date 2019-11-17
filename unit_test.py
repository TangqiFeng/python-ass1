#!/usr/bin/env python3
# this module contains unit test for all functions in this program
import lib
import os.path
import pytest
from dataOperator import DataOperator
from dataAnalyst import DataAnalyst

def test_dowmload_file():
    '''
    download data from web
    '''
    Cork_Airport_data_url = 'https://cli.fusio.net/cli/climate_data/webdata/mly3904.csv'
    operator = DataOperator()
    assert len(operator.dowmload_file(Cork_Airport_data_url)) == 37238

def test_save_file():
    '''
    save_file function used to create a new file with given content
    '''
    operator = DataOperator()
    operator.save_file("This is the test file", "test.txt")
    assert os.path.isfile('test.txt')

def test_prepare_files():
    '''
    run the prepare_files function, two datasets(cork airport & shannon 
    airport) and filtered datasets should save locally. And the database 
    should be set up and a file to record results should be created.
    '''
    lib.prepare_files()
    assert os.path.isfile('cork_air.csv')
    assert os.path.isfile('shan_air.csv')
    assert os.path.isfile('cork_air_data.csv')
    assert os.path.isfile('shan_air_data.csv')
    assert os.path.isfile('SQLite_Python.db')
    assert os.path.isfile('History_Record.txt')

def test_validate_input():
    '''
    the calidate_input method will check type_in is/not valid according 
    to the input options. otherwise will raise an exception
    '''
    with pytest.raises(Exception):
        assert lib.validate_input('3',['1','2'])
        assert lib.validate_input('a',['1','2'])
        assert lib.validate_input('ab',['a','b'])
        assert lib.validate_input('.',['a','b'])
        
def test_append_to_file():
    '''
    the method append_to_file is used to add content to a existing 
    file - 
    '''
    # create a test file
    test_file= open("History_Record.txt","w+")
    test_file.write("This is the test file")
    test_file.close()
    lib.append_to_file('\nTESTING')
    with open("History_Record.txt", 'r') as file:
        assert 'TESTING' in [line.strip() for line in file.readlines()]
        
def test_draw_bar_chart():
    '''
    this method - draw_bar_chart used to draw a bar chart
    '''
    data = [['sun,2009,246.3', 'sun,2010,208.9', \
             'sun,2011,197.8', 'sun,2012,163.3', 'sun,2013,264.5', \
             'sun,2014,206.3', 'sun,2015,223.7', 'sun,2016,204.4', \
             'sun,2017,192.5', 'sun,2018,256.9']]
    lib.draw_bar_chart(data, 'max', 'cork sirport')
    img_name = 'max value of sun in cork sirport, 2009~2018_bar_chart.png'
    assert os.path.isfile(img_name)
    
def test_draw_line_chart():
    '''
    this method - draw_bar_chart used to draw a line chart
    '''
    data = [['sun,2009,246.3', 'sun,2010,208.9', \
             'sun,2011,197.8', 'sun,2012,163.3', 'sun,2013,264.5', \
             'sun,2014,206.3', 'sun,2015,223.7', 'sun,2016,204.4', \
             'sun,2017,192.5', 'sun,2018,256.9']]
    lib.draw_line_chart(data, 'max', 'cork sirport')
    img_name = 'max value of sun in cork sirport, 2009~2018_line_chart.png'
    assert os.path.isfile(img_name)
    
def test_draw_box_plot():
    '''
    this method - draw_bar_chart used to draw a box plot
    '''
    data = [['sun,2009,246.3', 'sun,2010,208.9', \
             'sun,2011,197.8', 'sun,2012,163.3', 'sun,2013,264.5', \
             'sun,2014,206.3', 'sun,2015,223.7', 'sun,2016,204.4', \
             'sun,2017,192.5', 'sun,2018,256.9']]
    lib.draw_box_plot(data, 'max', 'cork sirport')
    img_name = 'max value of sun in cork sirport, 2009~2018_box_plot.png'
    assert os.path.isfile(img_name)
    
def test_draw_pie_chart():
    '''
    this method - draw_bar_chart used to draw a pie chart
    '''
    data = [('July', 31), ('August', 16), ('June', 3)]
    lib.draw_pie_chart(data, 'meant', 'max', 'cork sirport')
    img_name = 'month pct with max value of meant in cork sirport, 1969~2018_pie_chart.png'
    assert os.path.isfile(img_name)

def test_plot_regression_line():
    '''
    the method generate a scatter plot with a regression line using 
    input data
    '''
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [1, 3, 2, 5, 7, 8, 8, 9, 10, 12]
    lib.plot_regression_line(x, y, 'one', 'two')
    img_name = 'relationship between one and two_scatter.png'
    assert os.path.isfile(img_name)
         
def test_estimate_coef():
    '''
    this method use Least Squares technique to estimate coefficients for 
    analysising.
    '''
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [1, 3, 2, 5, 7, 8, 8, 9, 10, 12] 
    assert type(lib.estimate_coef(x,y)) == tuple
    assert lib.estimate_coef(x,y) == (1.2363636363636363,1.1696969696969697)

def test_get_value_based_on_year():
    '''
    This method will calculate the max/min/meant attributes value 
        for each year.
    '''
    ana_obj = DataAnalyst('cork_air_data.csv')
    result = ana_obj.get_value_based_on_year(['sun', 'meant'], 'min')
    for re in result:
        assert len(re) == 50
        
def test_get_value_based_on_year_with_month():
    '''
    This method will calculate the max/min attributes value devided 
        by year. Fetch the walue with its month
    '''
    ana_obj = DataAnalyst('cork_air_data.csv')
    result = ana_obj.get_value_based_on_year_with_month(['sun', 'meant'], 'min')
    for re in result:
        assert len(re) == 100

def test_get_month_frequency():
    '''
    analysis the input months, analysis the frequency of occurrence 
        of its elements
    '''
    ana_obj = DataAnalyst('cork_air_data.csv')
    months = ['1','2','2','1','3','3','7','7','5']
    assert ana_obj.get_month_frequency(months) ==\
    [('March', 2), ('July', 2), ('January', 2), ('February', 2), ('May', 1)]
    
    