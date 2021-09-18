# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/
# Like we specify in the IMPORTANT NOTE.txt: 
# Note that parsing HTML or XML with regular expressions is painful.
# Quick-and-dirty patterns will handle common cases, but HTML and XML have 
# special cases that will break the obvious regular expression; by the time 
# you’ve written a regular expression that handles all of the possible cases, 
# the patterns will be very complicated. Use an HTML or XML parser module for 
# such tasks.

# STATISTICAL ANALYSIS OF NAMES OF BABIES IN THE US FROM 1990 TO 2019
# WHAT'S NEXT: ADD SOME TRY/EXCEPT BLOCKS


import re
import json
import matplotlib.pyplot as plt
import os 
import numpy as np

def extract_names(filename):
    """
    Given a file name for baby.html, returns a list of tuples with the 
    rank of the corresponding boy and girl name for the given year
    """
    with open(filename) as f_obj:
        contents = f_obj.readlines()

    p = re.compile(r"""\s<td>        # We are going to use named groups 
                   (?P<rank>\d+)       # Parse the number rank
                   </td>\s<td> 
                   (?P<boy_name>\w+)   # Parse the boy name
                   </td>\s<td>
                   (?P<girl_name>\w+) # Parse the girl name
                   </td>               # Closing the cell html tag
                   """, re.VERBOSE) # Compiling the regex
    
    output = []
    for line in contents:
        if re.match('\s<td>.*',line): # So we skip the non-important stuff 
            m = p.search(line)
            temp_output = m.group('rank'), m.group('boy_name'), m.group('girl_name')
        else:
            continue 
        output.append(temp_output)
        
    return output 

# ----------------------------------------------------------------------------

def extract_years(year_span, directory):
    """
    Takes a list of years and parses the data for the given years from the
    html files in the given directory and saves them in a dictionary in a
    json formatted file
    """
    data = dict()
    for year in year_span:
        temp_data = extract_names(directory+f'\\baby{str(year)}.html')
        data[str(year)] = temp_data
    
    with open('data.json', 'w') as f_obj:
        json.dump(data, f_obj, sort_keys=True, indent=4)

# ----------------------------------------------------------------------------
    
def create_data_plot(name, gender, data, year_span):
    """
    Takes the desired user input and creates a matplotlib plot for the
    given baby name's flunctuation in popularity in the given year span
    by using the input json data
    """
    x_values = year_span; y_values = []
    gender_flag = 1 if gender == 'boy' else 2
    
    for year in year_span:
        found_flag = False
        for i,info in enumerate(data[str(year)]):
            if name == info[gender_flag]:
                y_values.append(int(data[str(year)][i][0]))
                found_flag = True
                break
        if not found_flag: y_values.append(0)
    
    # Creating the figure plot using object oriented matplotlib
    fig = plt.figure(figsize=(12, 4))

    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # Remember is OO Matplotlib

    axes.plot(x_values, y_values, 'b')
    axes.set_ylim([0, max(y_values)])
    axes.set_xlim([x_values[0], x_values[-1]])
# Using here the reverse_axis methods, found in this very detailed article 
# https://www.delftstack.com/howto/matplotlib/how-to-revert-axes-in-matplotlib/
    axes.invert_yaxis()

# Incrementing the y_tick labels by 1, as shown by these SO questions, IF OFCOURSE WE DONT HAVE CRAZY FLUNCTUATIONS IN POPULARITY (SO WE DONT HAVE UGLY PLOTS IN THE END)
# https://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib
# https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks
    
    if max(y_values)-min(y_values) <= 30: plt.yticks(np.arange(min(y_values), max(y_values)+1, 1.0))
    axes.set_xlabel('Years')
    axes.set_ylabel('Rank')
    axes.set_title(fr"Ranks of {name} ({gender}) in the year span {str(year_span[0])}-{str(year_span[-1])}")
    axes.grid(True)              
    fig.savefig(f"{name}_{year_span[0]}_{year_span[-1]}.svg")

# ----------------------------------------------------------------------------
# Here we could make our program more robust by having try/except blocks due to
# the fact that we depend user input to provide the desired output. In a next
# version we will add some try/except blocks. For now we trust our users
# completely! 

print("Welcome to the baby names analysis machine. Please provide the following")
print("PLEASE RUN THIS .PY FILE IN THE DIRECTORY WHERE YOU HAVE THE NECESSARY FILES!!!")

year_in = input("Specify the desired year span (1990-2019) (seperated by a comma or a dash): ")
years = (re.search(r"(\d+)[,-]\s*(\d+)",year_in).group(1),
         re.search(r"(\d+)[,-]\s*(\d+)",year_in).group(2))
name = input("Please provide the name of the baby (using title case): ").title()
gender = input("Is it a boy's name or a girl's name? Please write 'boy' or 'girl': ").lower()
directory = os.path.dirname(os.path.realpath(__file__))

year_span = range(int(years[0]),int(years[1])+1)
extract_years(year_span, directory)

with open('data.json', 'r') as f_obj:
    data = json.load(f_obj)

create_data_plot(name, gender, data, year_span)
   
# END OF FILE
