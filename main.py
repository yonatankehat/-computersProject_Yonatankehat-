# Project 2018-9 Tel-Aviv University
# The code is divided into 2 parts. The First part has all the function that appear in the main function which is 'linear fit'.
# The second part is the main function 'linear fit'. That function uses all the functions from the first part.

# Part 1:
################################################################################# project functions


# This function organizes the data points in a dictionary in which the keys are the axis headers and their
# values are the suitable measures - takes place in the linear_fit function
def data_organizer(data_points):
    data_table = [line.lower().strip().split(" ") for line in data_points]
    data_dict = {}
    if data_points_is_rows(data_table):
        for row in range(len(data_table)):
            data_dict[data_table[row][0]] = data_table[row][1:]
        organized_data = data_dict
    else:
        for col in range(len(data_table[0])):
            col_data = []
            for row in range(1, len(data_table)):
                try:
                    col_data.append(data_table[row][col])
                except IndexError:
                    pass
            data_dict[data_table[0][col]] = col_data
        organized_data = data_dict
    return organized_data


# this function accepts the data points and determines if the data points appears as rows or columns - takes
# place in the data_organizer function
def data_points_is_rows(data_points):
    list_of_items_in_first_row = data_points[0]
    for item in list_of_items_in_first_row:
        if item.isalpha():
             continue
        else:
            return 'values are organized in rows'
    return None


# This function accepts a dictionary of the data and determines whether the data is valid. takes place in the
# linear_fit function
def data_validation(organized_data):
    if arrays_have_different_length(organized_data):
        return True, 'Input file error: Data lists are not the same length.'

# Now I'll check that all the uncertainties are greater than 0. in order to do that I'll
# turn the measures into float numbers
    measures_into_floats(organized_data)
    if uncertainties_are_not_valid(organized_data):
        return True, 'Input file error: Not all uncertainties are positive.'

    return False, 'OK'


# This function checks whether the arrays of the data have the same length - takes place in the
# data_validation function
def arrays_have_different_length(organized_data):
    if len(organized_data['dx']) == len(organized_data['dy']) == len(organized_data['x']) == len(organized_data['y']):
        return False
    else:
        return True


# This function checks whether all the uncertainties are greater than 0 - takes place in the
# data_validation function
def uncertainties_are_not_valid(organized_data):
    dx = organized_data['dx']
    dy = organized_data['dy']
    for measure in dx:
        if measure <= 0:
            return True
    for measure in dy:
        if measure <= 0:
            return True


# This function turns all the measures from strings to numbers - takes place in the
# data_validation function - takes place in the data_validation function
def measures_into_floats(organized_data):
    keys_list = list(organized_data.keys())
    for key in keys_list:
        for number in range(len(organized_data[key])):
            if organized_data[key][number] == ' ':
                organized_data[key].remove(organized_data[key][number])
            organized_data[key][number]= float(organized_data[key][number])
    return organized_data


import math
# This function accepts the the data points arraign in a dictionary and will calculate the match parameters
# and chi min square - takes place in the linear_fit function
def match_parameters(x,dx,y,dy):

    N = len(x)
    x_weighted_avg = weighted_average_calc(x,dy)
    y_weighted_avg = weighted_average_calc(y,dy)
    x_squared_weighted_avg = weighted_average_calc(squared_para(x), dy)
    xy_weighted_avg = weighted_average_calc(parameters_multip(x, y), dy)
    dy_squared = weighted_average_calc(squared_para(dy), dy)

    a = (xy_weighted_avg - x_weighted_avg* y_weighted_avg)/(x_squared_weighted_avg - x_weighted_avg ** 2)
    b = y_weighted_avg - a * x_weighted_avg
    da = math.sqrt(dy_squared / (N * (x_squared_weighted_avg - x_weighted_avg ** 2)))
    db = math.sqrt((dy_squared * x_squared_weighted_avg) / (N * (x_squared_weighted_avg - x_weighted_avg ** 2)))

    chi_squared = chi_calc(x, y, a, b, dy)
    chi_squared_reduced = chi_squared/(N-2)

    return a, da, b, db, chi_squared, chi_squared_reduced


# This function accepts a list of measures and a list of dy return it's weighted average
# - takes place in the match_parameters function
def weighted_average_calc(parameter,dy):
    sum_weighted_average = 0
    sum_dy = 0
    for i in range(0, len(parameter)):
        sum_weighted_average += (parameter[i]/dy[i]**2)
        sum_dy = (1/dy[i]**2) + sum_dy
    return sum_weighted_average/sum_dy


# This function accepts a list of a parameter and returns a list of squares of each part of the original list
# - takes place in the match_parameters function
def squared_para(parameter):
    Square_Parameter = []
    for squared in parameter:
        Square_Parameter.append(squared**2)
    return Square_Parameter


# This function accepts 2 lists and returns a weighted average of their multiplication - takes place in the
# match parameters function
def parameters_multip(parameter_a,parameter_b):
    parameters_multiplication = []
    for i in range(len(parameter_a)):
        parameters_multiplication.append(parameter_a[i]*parameter_b[i])
    return parameters_multiplication


# This function accepts the lists of the parameters x, y, dy, a and b. The function
# calculates chi square and returns it - takes place in the match parameters function
def chi_calc(x,y,a,b,dy):
    count = 0
    for i in range(len(x)):
        count = (((y[i]) - (a * x[i] + b)) / dy[i])**2 + count
    return count


# This function accepts the data of the headers axis, organizes it and returns the x and y headers.
# - takes place in the linear fit function
def headers_axis_organizer(axis_titles):
    x_title_axis = ''
    y_title_axis = ''

    for line in axis_titles:
        for i in range(len(axis_titles)):

            line = line.lower().strip()
            if line.startswith('x axis:'):
                x_title_axis= axis_titles[i][6:].strip()
            if line.startswith('y axis:'):
                y_title_axis= axis_titles[i][6:].strip()
    return x_title_axis, y_title_axis


import matplotlib.pyplot as plt


# This function plot the linear graph using the parameters calculated earlier
# - takes place in the linear fit function
def make_linear_min_chi2_plot(organized_data, a, b, x_title_axis, y_title_axis):
    y_list = []
    for x_var in organized_data ["x"]:
        y_function = a * x_var + b
        y_list.append(y_function)
    plt.plot(organized_data['x'], y_list, 'r')
    plt.errorbar(organized_data['x'],
                 organized_data['y'],
                 xerr=organized_data['dx'],
                 yerr=organized_data['dy'],
                 fmt='b,')
    plt.title("Linear Plot Min Chi^2 ")
    plt.xlabel(x_title_axis)
    plt.ylabel(y_title_axis)
    plt.savefig("linear_fit.svg")
    #plt.show()
    
# Part 2:
######################################################################## project main function

def linear_fit(file_name):

    file_pointer = open(file_name, 'r')
    data = file_pointer.readlines()
    file_pointer.close()

# Now I'll divide the data to a list of data points and a list of the axis titles.
    empty_separation_line_index = data.index('\n')
    data_points = data[:empty_separation_line_index]
    axis_titles_data = data[empty_separation_line_index:]

# Then I'll organize the data in a dictionary in which every key is an axis and the values are it's measures.
    organized_data = data_organizer(data_points)

# After organizing the data I'll check the validity of the input.
    is_valid, msg = data_validation(organized_data)
    if is_valid:
        print(msg)
        return
# The next function calculates the match parameters from the organized data.
    a, da, b, db, chi_squared, chi_squared_reduced = match_parameters(x=organized_data['x'],
                                                                      dx=organized_data['dx'],
                                                                      y=organized_data['y'],
                                                                      dy=organized_data['dy'])
    x_title_axis, y_title_axis = headers_axis_organizer(axis_titles_data)

# At last I'll print the output as requested and use plot_linear_fit function to plot the requested graph
    final_output = "a = {0} +- {1} \nb = {2} +- {3} \nchi2 = {4} \nchi2_reduced = {5}\n"\
            .format(a, da, b, db, chi_squared, chi_squared_reduced)

    make_linear_min_chi2_plot(organized_data,a,b,x_title_axis,y_title_axis)
    print(final_output)
   


