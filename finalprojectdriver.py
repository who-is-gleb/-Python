'''
DS 2000
Spring 2019
Final Project Driver
'''

from finalprojectfunctions import read_kick_data
from finalprojectfunctions import get_categories
from finalprojectfunctions import outcome_rates_by_category
from finalprojectfunctions import outcome_rate_by_goal
from finalprojectfunctions import draw_bars
from finalprojectfunctions import avg_pledge_per_category

import matplotlib.pyplot as plt

LIST_OF_RANGES = [[0, 500], [500, 1000], [1000, 2000], \
                  [2000, 4000], [4000, 8000], [8000, 50000], [50000, 500000], [500000, 1000000]]

def main():
    kick_data_orig = read_kick_data('ks-projects-201801.csv')
    kick_data = []
    
    # creates a new list of projects that excludes "live" or "undefined" projects
    for i in range(len(kick_data_orig)):
        if kick_data_orig[i]['state'] == 'successful' or \
           kick_data_orig[i]['state'] == 'failed' or \
           kick_data_orig[i]['state'] == 'canceled':
            kick_data.append(kick_data_orig[i])
    
    # converts each goal into a float to be converted to an int as needed
    for i in range(len(kick_data)):
        kick_data[i]['usd_goal_real'] = float(kick_data[i]['usd_goal_real'])
        


    '''
    Creates graph for outcome rates by category
    '''
    # creates a list of categories, unsorted
    categories = get_categories(kick_data)

    # creates an empty dictionary to which elements
    # {..., 'category': [success%, fail%, canceled%], ...} will be added
    percentages_by_category = {}
    
    # looks at each category and calculates success, fail, and canceled %
    # adds each {'category': [success%, fail%], ...} to percentages_by_category
    for i in range(len(categories)):
        category = categories[i]
        success_result = \
                       outcome_rates_by_category(kick_data, category, 'successful')
        fail_result = \
                    outcome_rates_by_category(kick_data, category, 'failed')
        canceled_result = \
                        outcome_rates_by_category(kick_data, category, 'canceled')

        percentages_by_category[category] = \
                                          [success_result, fail_result, canceled_result]
        
    # sorts dictionaries in percentages_by_category by success percents
    # creates a new list of tuples: (category, [outcome %s])
    sorted_percentages_by_category = sorted(percentages_by_category.items(), \
                                            key=lambda x: x[1], reverse=True)


    # creates a list of categories, success%, fail%, canceled%
    # all in order of descencing success%
    sorted_categories = []
    category_success_percentages = []
    category_fail_percentages = []
    category_canceled_percentages = []
    for category in sorted_percentages_by_category:
        sorted_categories.append(category[0])
        category_success_percentages.append(category[1][0])
        category_fail_percentages.append(category[1][1])
        category_canceled_percentages.append(category[1][2])
    
    # draws bar graph using the sorted lists of outcome %s and categories
    draw_bars(category_success_percentages, category_fail_percentages, \
                      category_canceled_percentages, sorted_categories, \
                    "Outcome Rates By Category", "Outcome %")



    '''
    Creates graph for outcome rates by goal range
    '''
    # this creates a list of ranges which will be the bins of the histogram
    ranges = ['0-499', '500-999', '1,000-1,999', '2,000-3,999', '4,000-7,999', \
              '8,000-49,999', '50,000-499,999', '500,000-1,000,000']
    
    # creates an empty dictionary to which elements
    # {..., 'goal range': [success%, fail%, canceled%], ...} will be added
    percentages_per_goalrange = {}

    # looks at each range and calculates success, fail, and canceled %
    # adds each {'range': [success%, fail%], ...} to percentages_by_goalrange
    for i in range(len(ranges)):
        rng = ranges[i]
        success_percent = outcome_rate_by_goal(kick_data, LIST_OF_RANGES[i], 'successful')
        fail_percent = outcome_rate_by_goal(kick_data, LIST_OF_RANGES[i], 'failed')
        canceled_percent = outcome_rate_by_goal(kick_data, LIST_OF_RANGES[i], 'canceled')

        percentages_per_goalrange[rng] = [success_percent, fail_percent, canceled_percent]

    # creates a list of success%, fail%, canceled%
    # in order of increasing goal ranges
    range_success_percent = []
    range_fail_percent = []
    range_canceled_percent = []
    for key, value in percentages_per_goalrange.items():
        range_success_percent.append(value[0])
        range_fail_percent.append(value[1])
        range_canceled_percent.append(value[2])

    # draws histogram using the above outcome% lists
    draw_bars(range_success_percent, range_fail_percent, \
                      range_canceled_percent, ranges, "Outcome Rates By Goal Range", \
                      "Outcome %")


    '''
    Creates bar graph for average amount pledged for each category
    '''

    # creates an empty dictionary in which elements will be {..., 'category': avg_pledged, ...}
    avg_pledged_per_category = {}

    # this is a null list to be used as a placeholder
    # for un-needed params in the draw_bars function
    null_list = []

    # iterates over categories and calculates average pledge per backer for each
    # category, adds each data pair to the dictionary (avg_pledged_per_category)
    # sorts the dictionary by decreasing average pledge
    for i in range(len(categories)):
        category = categories[i]
        avg_pledged = avg_pledge_per_category(kick_data, category)

        avg_pledged_per_category[category] = [avg_pledged]

    sorted_avg_pledged_per_category = sorted(avg_pledged_per_category.items(), \
                                             key=lambda x: x[1], reverse=True)

    # pulls out average amount pledged and corresponding category
    # and adds each to respective list at the same index
    sorted_categories = []
    sorted_pledge_amounts = []
    for i in range(len(sorted_avg_pledged_per_category)):
        sorted_categories.append(sorted_avg_pledged_per_category[i][0])
        sorted_avg_pledged_per_category[i][1][0] = \
                                                 float(sorted_avg_pledged_per_category[i][1][0])
        sorted_pledge_amounts.append(sorted_avg_pledged_per_category[i][1][0])

    # draws bar graph
    draw_bars(sorted_pledge_amounts, null_list, null_list, sorted_categories, \
                      "Average Pledge Per Backer By Category", "Average Pledge (USD)")

main()

