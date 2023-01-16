# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 14:21:24 2020

@author: Lin
"""

import csv
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

# =============================================================================
# takes in a string with a path to a CSV file formatted as in the link above, 
# and returns the first 20 data points (without the Generation and Legendary columns 
# but retaining all other columns) in a single structure.
# =============================================================================
def load_data(filepath):

    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 20
        reader2  = []
        for row in reader:
            del row['Generation']
            del row['Legendary']
            reader2.append(row)
            counter -= 1
            if counter==0:
                break
        return reader2
           
# =============================================================================
# takes in one row from the data loaded from the previous function, 
# calculates the corresponding x, y values for that Pokemon as specified above,
# and returns them in a single structure.
# =============================================================================
def calculate_x_y(stats):
    x = int(stats['Attack']) + int(stats['Sp. Atk']) + int(stats['Speed'])
    y = int(stats['Defense']) + int(stats['Sp. Def']) + int(stats['HP'])
    
    return (x,y)
    
    
    

# =============================================================================
# performs single linkage hierarchical agglomerative clustering on the Pokemon 
# with the (x,y) feature representation, and returns a data structure 
# representing the clustering.
# =============================================================================
def hac(dataset):
    dataset = getset(dataset)
    matrix1 = []
    
    num_cluster = 20
    while (num_cluster>1):
        # initialization of distance, new cluster, A, B
        least_d = float('inf')
        new_cluster = []
        A = -1
        B = -1
        # find the closest A, B, minimize d(A,B)
        for idx1, c1 in enumerate(dataset):
            if c1 == None:
                continue
            for idx2, c2 in enumerate(dataset):
                if c2 == None:
                    continue
                d = euclideanD2(c1, c2)
                if idx1 == idx2:
                    continue
                if d < least_d:
                    least_d = d
                    A = idx1
                    B = idx2
                    new_cluster = c1+c2
        # set the combined data to none
        dataset[A] = None
        dataset[B] = None
        n = len(new_cluster)
        # add useful data to the matrix
        matrix1.append([A, B, least_d, n])
        dataset.append(new_cluster)
        num_cluster -= 1
    matrix1 = np.matrix(matrix1)
    return matrix1

# =============================================================================
# find the euclidean distance of two datapoints
# =============================================================================
def euclideanD(x1, x2):
    a = (x1[0]-x2[0])**2
    b = (x1[1]-x2[1])**2
    return (a+b)**0.5


# =============================================================================
# find the euclidean distance of two clusters
# =============================================================================
def euclideanD2(A, B):
    least = float('inf')
    for x in A:
        for y in B:
            d = euclideanD(x, y)
            if d < least:
                least = d
    return least

# =============================================================================
# get 20*1 arrays
# =============================================================================
def getset(dataset):
    dataset2 = []
    for row in dataset:
        stat = calculate_x_y(row)
        dataset2.append([stat])
    return dataset2














