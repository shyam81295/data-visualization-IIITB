import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as col
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
#import string

file_path = input('Enter dataset file path:')
interpolation_num = input('Choose an interpolation method:\n0.bilinear\n1.bicubic')
color_spectrum_num = input('Choose a color spectrum:\n0.rainbow\n1.gray\n2.BuGn')

INTP_METHODS = ["bilinear", "bicubic"]
COLOR_SPECTRUMS = ["rainbow", "gray", "BuGn"]
FILE_NAMES = [ "aug_6_temp","Aug-2016-meridional-current-181x189", "Aug-2016-potential-temperature-180x188", "Aug-2016-salinity-180x188", "Aug-2016-tropical-heat-potential-180x188", "Aug-2016-zonal-current-181x189" ]

interpolation_num = int(interpolation_num)
color_spectrum_num = int(color_spectrum_num)

intp_method = INTP_METHODS[interpolation_num]
color_spectrum = COLOR_SPECTRUMS[color_spectrum_num]

cdict_gray = {'red':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                  (1.0, 1.0, 1.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }

cdict_BuGn = {'green':   ((0.0, 0.0, 1.0),
                   (1.0, 0.0, 0.0)),

         'red': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (1.0, 1.0, 1.0))
        }

cdict_rainbow = {'red':   ((0.0, 0.0, 1.0),
                   (0.2, 1.0, 1.0),
				   (0.4, 0.0, 0.0),
				   (0.6, 0.0, 0.0),
				   (0.8, 0.0, 0.0),
                   (1.0, 1.0, 0.0)),

         'green': ((0.0, 0.0, 0.0),
                   (0.2, 1.0, 1.0),
				   (0.4, 1.0, 1.0),
				   (0.6, 1.0, 1.0),
				   (0.8, 0.0, 0.0),
                   (1.0, 0.0, 1.0)),

         'blue':  ((0.0, 0.0, 0.0),
                   (0.2, 0.0, 0.0),
				   (0.4, 0.0, 0.0),
				   (0.6, 1.0, 1.0),
				   (0.8, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),
        }

if(color_spectrum_num == 0):
    cdict = cdict_rainbow
elif(color_spectrum_num == 1):
    cdict = cdict_gray
elif(color_spectrum_num == 2):
    cdict = cdict_BuGn

BAD_FLAG_KEY = "BAD FLAG"
#folder_path = '../dataset'
#file_name = FILE_NAMES[0]
#file_path = folder_path + "/" + file_name + ".txt"

def get_bad_flag( BAD_FLAG_KEY, file_path ):
	bad_flag = "NA"
	file = open( file_path )
	for line in file:
		if BAD_FLAG_KEY in line:
			flag = line.split(":")[1]
			bad_flag = flag.strip()
			break
	file.close()
	return bad_flag

def get_lines_to_skip( file_path ):
	bad_flag = "NA"
	i=0
	file = open( file_path )
	for line in file:
		split = line.split(":")
		if len(split) < 2 :
			break
		i = i + 1
	file.close()
	return i

def read_file( file_path, lines_to_skip, bad_flag ) :
    return pd.read_csv (file_path, skiprows=lines_to_skip, sep='\t', na_values=[bad_flag])

def mask_array( array, mask_value ):
	return np.ma.masked_equal(data, mask_value )

def format_latitudes( latitudes ):
    for i in range(len(latitudes)):
        if 'N' in latitudes[i]:
            latitudes[i] = float( str(latitudes[i]).replace("N", "" ) )
        elif 'S' in latitudes[i] :
            latitudes[i] = float( "-" + str(latitudes[i]).replace("S","") )

def format_longitudes( longitudes ):
    for i in range(len(longitudes)):
        if 'E' in longitudes[i]:
            longitudes[i] = float( str(longitudes[i]).replace("E","")  )
        elif 'W' in longitudes[i]:
            longitudes[i] = float( "-" + str(longitudes[i]).replace("W","") )

def perforn_bilinear_interpolation( array ):
	bint_arr = []
	for i in range( len(array) - 1 ):
		bint_arr.append([])
		for j in range( len(array[0]) - 1 ):
			x1 = i
			y1 = j
			x2 = i
			y2 = j+1
			x3 = i+1
			y3 = j
			x4 = i+1
			y4 = j+1
			f1 = data[x1][y1]
			f2 = data[x2][y2]
			f3 = data[x3][y3]
			f4 = data[x4][y4]
			x = i + 0.5
			y = j + 0.5
			if np.isnan(f1) or np.isnan(f2) or np.isnan(f3) or np.isnan(f4) :
				val = np.nan
			else:
				points = [ [x1,y1,f1], [x2,y2,f2], [x3,y3,f3], [x4,y4,f4] ]
				val = bili_intp_util( points, x, y )
			bint_arr[i].append( val )
	return np.array(bint_arr)

def bili_intp_util( points, x, y ):
    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)

def perform_task1( array, intp_method, cmap  ):

	#array = np.transpose(array)
	array = np.flipud(array)
	plt.imshow( array, cmap=cmap )
	plt.show()

def normalize_values( array ):
	min = np.nanmin(array)
	max = np.nanmax(array)
	if max == min :
		return
	for i in range( len(array) ):
		for j in range( len(array[0]) ):
			array[i][j] = (array[i][j] - min) / ( max - min )

def custom_color_map( c_name,c_dict ):
	#https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html
	return col.LinearSegmentedColormap( c_name, c_dict)


bad_flag = get_bad_flag( BAD_FLAG_KEY, file_path )
num_lines_to_skip = get_lines_to_skip( file_path )
data = read_file( file_path, num_lines_to_skip, bad_flag )

#extract longitudes
longitudes = np.array(data.columns.values)
#get firts column key to extract latitudes
first_cloumn_key = longitudes[0]
#remove first element
longitudes = longitudes[1:]
#extract latitudes
latitudes = np.array( data[first_cloumn_key]  )
#delete first clumn
data = data.drop(columns=first_cloumn_key)
#convert data to numpy 2D array
data = np.array(data)
#normalize data(all values between 0-1)
normalize_values( data )
#do interpolation
data = perforn_bilinear_interpolation(data)
#mask bad values
data = np.ma.masked_invalid( data )
#format_latitudes
format_latitudes(latitudes)
format_longitudes(longitudes)

perform_task1( data, intp_method ,custom_color_map( "MyColorMap" ,cdict) )
with open('your_file.txt', 'w') as f:
    for item in data:
        f.write("%s\n" % item)
