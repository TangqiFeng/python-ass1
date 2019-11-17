import matplotlib.pyplot as plt 
  
def estimate_coef(x, y): 
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

def plot_regression_line(x, y, b): 
    # plotting the actual points as scatter plot 
    plt.scatter(x, y, color = "m", marker = "o", s = 30) 
    # predicted response vector 
    y_pred = []
    for _x in x:
        y_pred.append(b[0] + b[1]*_x)  
    # plotting the regression line 
    plt.plot(x, y_pred, color = "g")  
    # putting labels 
    plt.xlabel('x') 
    plt.ylabel('y')  
    # function to show plot 
    plt.show() 
 
def main(): 
    # observations 
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [1, 3, 2, 5, 7, 8, 8, 9, 10, 12] 
    # estimating coefficients 
    b = estimate_coef(x, y) 
    print("Estimated coefficients:\nb_0 = {}  \nb_1 = {}"\
          .format(b[0], b[1]))  
    # plotting regression line 
    plot_regression_line(x, y, b) 
  
if __name__ == "__main__": 
    main() 


# ref: https://www.geeksforgeeks.org/linear-regression-python-implementation/