import pandas
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def selfXYZ(x,y,arr):
    """
    Simply get values from csv file and apply function on it.
    """
    return arr

def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

def tp():
    x = [1,2,3]
    y = [4,5]

    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    print(X.shape)
    print(Y.shape)
    print(Z.shape)

def exponentialXYZ(x,y,arr):
    """
    Returns exp(x,y) [Idk hwo we will map it till now?]
    """
    pass

def init():
    """
    Initial method to call on.
    """
    # path of our csv file
    path = "/home/shyam8/Sem2/DV/a1-dataset-indian-ocean-consolidated/temp1.csv"
    # csv file converted to Pandas dataframe
    df = pandas.read_csv(path)
    # pandas dataframe converted to numpy array, bcoz it is easy to work with numpy
    arr = np.asarray(df)

    outlier = arr.max()
    out = np.min(arr)
    maxi = outlier

    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if(arr[i][j]!=out):
                if(arr[i][j]<maxi):
                    maxi = arr[i][j]

    print(maxi)

    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if(arr[i][j]==out):
                arr[i][j] = np.nan

    arr_masked = np.ma.array(arr,mask=np.isnan(arr))
    cmap = plt.cm.get_cmap('rainbow')
    cmap.set_under('white',1.)

    #
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # x is no of rows, y is no of columns
    x = range(len(arr))
    y = range(len(arr[0]))

    # Make X,Y as 2D array
    X,Y = np.meshgrid(x,y)

    # Z is according to function given by user
    Z = np.transpose(arr)
    print(X.shape)
    print(Y.shape)
    print(Z.shape)
    ax.plot_surface(X,Y,Z)
    ax.set_title('surface')
    plt.show()

init()
#tp()
