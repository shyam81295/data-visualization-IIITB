'''
======================
Author	: Shyam Singh
Roll no	: MT2017143
======================

	Steps:
	1. In python, preprocess the dataset file ->  any data array or data frame.
	2. Convert data frame -> RGB image acc to user's Color spectrum
	3. Interpolate the image acc to user's Interpolation method
	4. Make command-line interface like python-prompt-toolkit
	5. Finish all ma'am requests on assign1.

	Tasks Remaining:
	1. Parse Bad flags for each column
	2. Store lat, long
'''

import pprint as pp
import numpy as np
import re
import matplotlib.pyplot as plt

latitude = []
longitude = []
values = []
longitude_header = []
latitude_header = []
bad_flag_value = ''

def preprocess_dataset(file_path):
    '''
    Reads filename.
    Parses meaningful data into data array or data frame.
    Returns data frame.
    '''

    try:
        f = open(file_path, 'r')
        dataset_content = f.readlines()
        f.close()
        dataset_array = [] # to store main content of file
        starting_line_number = 0 # to store starting line of actual content
        global bad_flag_value

        '''assumption : given file has actual content starting next with string
        'TIME' '''
        for lines in dataset_content:
            lines = lines.strip() # trim the start & end spaces
            if(lines.startswith('TIME')):
                print(starting_line_number)
                break
            starting_line_number += 1

        '''assumption : given file has BAD FLAG starting with 'BAD FLAG'
                        and its value is at the line end '''
        for lines in dataset_content:
            lines = lines.strip() # trim the start & end spaces
            if(lines.startswith('BAD FLAG')):
                words = lines.split(':')
                bad_flag_value = words[-1].strip()
                print(bad_flag_value)

        '''starting_line_number has to be incremented by 1 to take next line
        after 'TIME' '''
        print(starting_line_number)
        starting_line_number += 1

        for lines in dataset_content[starting_line_number:]:
            words = re.split('\t| |\n',lines) # split by '\t' , ' ' , '\n'
            #words = words.remove('')
            dataset_array_line = []
            for word in words:
                if word is not '':
                    dataset_array_line.append(word)
            dataset_array.append(dataset_array_line)
        # pp.pprint(dataset_array[:3])

        # to get min/max long & min/max lat
        global values
        global longitude
        global latitude
        global longitude_header
        global latitude_header

        longitude_header = dataset_array[0]

        # to convert into -X.y or X.y format from X.yS or X.yN
        for lon in longitude_header:
            longi = float(lon[:-1]) # start to end-1, i.e. get X.y
            if lon.endswith('W'):
                longi = longi * (-1.0)
            longitude.append(longi)

        latitude_header = []

        # get first element from each row, except the column header
        for row in dataset_array[1:]:
            if bool(row): # row is not empty
                first_element = row[0] # first element of row
                latitude_header.append(first_element)
                for other_elements in row[1:]:
                    values.append(other_elements)

        for lat in latitude_header:
            if len(lat) is 1:
                lati = float(0)
            else:
                lati = float(lat[:-1])
                if lat.endswith('N'):
                    lati = lati * (-1.0)
            latitude.append(lati)

        #return dataset_array
        #print(longitude_header)
        print(len(longitude_header))
        #print(latitude_header)
        print(len(latitude_header))
        #print(values)
        print(len(values))
        print(longitude)
        print(latitude)
        print(bad_flag_value)

    except IOError:
        raise SystemExit('Dataset is not accessible')

    # Check what data is needed, like matrix dimensions, etc.
    # Parse rest of the data
    # Store it in data frame or array or list
    # Return this data structure

def convert_to_RGB():
    nrows, ncols = len(latitude), len(longitude)
    print(nrows)
    print(ncols)

    xmin, xmax = min(longitude), max(longitude)
    ymin, ymax = min(latitude), max(latitude)

    dx = (xmax - xmin) / (ncols - 1)
    dy = (ymax - ymin) / (ncols - 1)

    x = np.array(longitude)
    y = np.array(latitude)
    x, y = np.meshgrid(x, y)

    z = np.array(values)
    x, y, z = [item.flatten() for item in (x,y,z)]

    print(x[:10])
    print(y[:10])
    print(z[:10])
    # Scramble the order of the points so that we can't just simply reshape z
    #indicies = np.arange(x.size)
    #np.random.shuffle(indicies)
    #x, y, z = [item[indicies] for item in (x, y, z)]

    # Up until now we've just been generating data...
    # Now, x, y, and z probably represent something like you have.

    # We need to make a regular grid out of our shuffled x, y, z indicies.
    # To do this, we have to know the cellsize (dx & dy) that the grid is on
    # and
    # the number of rows and columns in the grid.

    # First we convert our x and y positions to indicies...
    idx = np.round((x - x.min()) / dx).astype(np.int)
    idy = np.round((y - y.min()) / dy).astype(np.int)

    # Then we make an empty 2D grid...
    grid = np.zeros((nrows, ncols), dtype=np.float)

    # Then we fill the grid with our values:
    grid[idy, idx] = z

    # And now we plot it:
    plt.imshow(grid, interpolation='hermite',
                       extent=(x.min(), x.max(), y.max(), y.min()))
    plt.colorbar()
    plt.show()


def interpolate(RGBimage):
    pass

def cli_inteface():
    pass

preprocess_dataset('/home/shyam8/Sem2/DV/a1-dataset-indian-ocean-consolidated/Aug-06-2016-potential-temperature-180x188.txt')
convert_to_RGB()
