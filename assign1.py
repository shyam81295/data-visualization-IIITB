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


'''

import pprint as pp

def preprocess_dataset(file_path):
    '''
    Reads filename.
    Parses meaningful data into data array or data frame.
    Returns data frame.
    '''

    # Check if file exists or not    
    # If yes, then Reads filename
    # Else, provides feedback 'file do not exist' and exits

    try:
        f = open(file_path, 'r')
        dataset_content = f.readlines()
        f.close()
        dataset_array = [] # to store main content of file
        for lines in dataset_content:
            lines = lines.split(',')
            dataset_array_line = []
            for word in lines:
                word = word.replace('"','').replace(' ','').replace('\n','')
                dataset_array_line.append(word)
            dataset_array.append(dataset_array_line)
        pp.pprint(dataset_array[:20])
        return dataset_array
    except IOError:
        raise SystemExit('Dataset is not accessible')

    # Check what data is needed, like matrix dimensions, etc.
    # Parse rest of the data
    # Store it in data frame or array or list
    
    # Return this data structure
    



def convert_to_RGB(dataframe):
    pass

def interpolate(RGBimage):
    pass

def cli_inteface():
    pass

preprocess_dataset('/home/shyam8/Sem2/DV/a1-dataset-indian-ocean-consolidated/December24-2016-potential-temperature.csv')
