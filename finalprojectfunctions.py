'''
DS 2000
Spring 2019
Final Project: Functions
'''

import csv
import numpy as np
import matplotlib.pyplot as plt


def convert_to_dictionary(header, row):
    return {header[i]:row[i] for i in range(len(header))}

def read_kick_data(filename):
    with open(filename) as csv_file:
        header = csv_file.readline().strip().split(',')
        kickdata = []
        for line in csv.reader(csv_file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL):
            if line != []:
                d = convert_to_dictionary(header, line)
                kickdata.append(d)
    return kickdata


def get_categories(data):
    # creates a list of project categories
    # params: list of dictionaries of all projects
    # returns: a list of project categories
    categories = []
    for project in data:
        if project['main_category'] in categories:
            pass
        else:
            categories.append(project['main_category'])
    return categories

            
def outcome_rates_by_category(data, category, outcome):
    # calculates the %outcome of a given category
    # params: list of dictionaries of all projects, a category (string),
        # desired outcome (string)
    # returns: %outcome for a category (float)
    total_projects = 0
    total_outcome = 0
    for project in data:
        if project['main_category'] == str(category):
            total_projects += 1
            if project['state'] == outcome:
                total_outcome += 1
    return (100 * total_outcome / total_projects)
                

def outcome_rate_by_goal(data, goal_range, outcome):
    # calculates the %outcome for projects in a goal amount range
    # params: data (list of dictionaries),
        # range of goal (tuple), outcome (string)
    # returns: %outcome for a category (float)
    total_projects = 0
    total_outcome = 0
    for project in data:
        if (((int(project["usd_goal_real"])) > goal_range[0]) \
           and ((int(project["usd_goal_real"])) < goal_range[1])):
            total_projects += 1
            if project['state'] == outcome:
                total_outcome += 1
    if total_projects == 0:
        return 0
    return (100 * total_outcome / total_projects)


def avg_pledge_per_category(data, category):
    # calculates the average amount pledged by person in a given
        # category
    # params: data (list of dictionaries), category (string)
    # returns: avg pledged by person (float)
    total_pledged = 0
    backers = 0
    for project in data:
        if project['main_category'] == str(category):
            total_pledged += float(project['pledged'])
            backers += float(project['backers'])
    if backers == 0:
        return 0
    return total_pledged / backers


def draw_bars(success_means, fail_means, canceled_means, \
                      xaxis_values, title, ylabel):
    # draws bars using matplotlib
    # params: success means (list), fail means (list), canceled means (list),
        # x axis labels (list), title (string), ylabel (string)
    # returns: void (draws a bar chart or histogram)
    y_pos = np.arange(len(xaxis_values))

    p1 = plt.bar(y_pos, success_means)
    if fail_means != [] and canceled_means != []:
        p2 = plt.bar(y_pos, fail_means, bottom=success_means)
        p3 = plt.bar(y_pos, canceled_means, bottom=\
                     [success_means[j] + fail_means[j] for j in range(len(success_means))])
        plt.legend((p1[0], p2[0], p3[0]), ('Success', 'Fail', 'Canceled'))

    plt.xticks(y_pos, xaxis_values, fontsize=7)
    plt.ylabel(str(ylabel))
    plt.title(str(title))

    plt.show()

