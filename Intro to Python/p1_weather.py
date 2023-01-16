# -*- coding: utf-8 -*-
"""
CS 540 2020 Fall HW1 - weather
@author: Yucheng Lin
"""

def manhattan_distance(data_point1, data_point2):
    # get the absolute value
    d1 = abs(float(data_point1['TMAX']) - float(data_point2['TMAX']))
    d2 = abs(float(data_point1['TMIN']) - float(data_point2['TMIN']))
    d3 = abs(float(data_point1['PRCP']) - float(data_point2['PRCP']))
    #add them together
    return d1+d2+d3

def read_dataset(filename):
    #open file
    fopen = open(filename, 'r')
    lines = fopen.readlines()
    data_dict = []
    #deal with each line 
    for line in lines:
        line = line.strip('\n')
        data_array = line.split(' ')
        if len(data_array) == 5: #as long as format is correct            
            sample_dict = {'DATE': '0000-01-01', 'TMAX': 1.0, \
                           'PRCP': 0.1, 'TMIN': 1.0, 'RAIN': 'TRUE'}
            sample_dict['DATE'] = data_array[0]
            sample_dict['TMAX'] = data_array[1]
            sample_dict['PRCP'] = data_array[2]
            sample_dict['TMIN'] = data_array[3]
            sample_dict['RAIN'] = data_array[4]
            # for each data, add them to the data_dict
            data_dict.append(sample_dict)
    return data_dict

def majority_vote(nearest_neighbors):
    countT = 0
    countF = 0    
    #count true and false
    for neighbor in nearest_neighbors:
        if neighbor['RAIN'] == 'TRUE':
            countT += 1
        else:
            countF += 1
    #if true are more than or equal to false
    if countT >= countF:
        return 'TRUE'
    else:
        return 'FALSE'
    
def k_nearest_neighbors(filename, test_point, k, year_interval):
    dataset = read_dataset(filename)
    nearest_neighbors = []
    year_testpoint = test_point['DATE'][0:4]
    distance_collection = []
    if year_interval == 0:
        return 'TRUE'
    
    for data in dataset: #filter by interval
        year = data['DATE'][0:4]
        if abs(int(year)- int(year_testpoint)) < year_interval:
            nearest_neighbors.append(data)
    if len(nearest_neighbors) > k:
        
        for index, neighbor in enumerate(nearest_neighbors): #filter by k
            distance = manhattan_distance(test_point, neighbor)
            distance_collection.append([index, distance])
        #sort by the distance
        distance_collection.sort(key=lambda x:x[1])
        k_nearest_neighbors = []
        #append each value to the list
        while (k != 0):
            i = distance_collection[k-1][0]
            k_nearest_neighbors.append(nearest_neighbors[i])
            k -= 1
        return majority_vote(k_nearest_neighbors)
    else:
        return majority_vote(nearest_neighbors)
        
    
        