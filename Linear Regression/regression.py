# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:39:29 2020

@author: Lin
"""
import csv
import numpy as np
import random
# =============================================================================
# takes a filename and returns the data as described below in an n-by-(m+1) array
# =============================================================================
def get_dataset(filename):
    array = []
    # open file with csv format
    with open(filename) as file:
        reader = csv.reader(file)
        a = 1
        for row in reader:
            # ignore the first row
            if a == 1:
                a = 0
                continue
            array.append([float(i) for i in row[1:]])
        return np.array(array)
    
# =============================================================================
# takes the dataset as produced by the previous function and prints several 
# statistics about a column of the dataset; does not return anything
# =============================================================================
def print_stats(dataset, col):
    print(len(dataset))
    ds_tr = np.transpose(dataset)
    print('%.2f' % np.mean(ds_tr[col]))
    print('%.2f' % np.std(ds_tr[col]))
    
# =============================================================================
# calculates and returns the mean squared error on the dataset given fixed betas
# =============================================================================
def regression(dataset, cols, betas):
    s = 0
    for row in dataset:
        v = betas[0]
        # get value from each row
        for i in range(len(cols)):
            v += betas[i+1]*row[cols[i]]
        v -= row[0]
        v = v*v
        # get sum of all values
        s += v
    # devide by # of datapoints
    s = s / (len(dataset))
    return s


# =============================================================================
# performs a single step of gradient descent on the MSE and returns 
# the derivative values as an 1D array
# =============================================================================
def gradient_descent(dataset, cols, betas):
    array = []
    for i in range(len(betas)):
        s = 0
        # iterate each row in dataset
        for row in dataset:
            v = betas[0]
            for j in range(len(cols)):
                v += betas[j+1]*row[cols[j]]
            v -= row[0]
            if i == 0:
                pass
            else: # multiply x(i) if it is beta(i)
                v = v*row[cols[i-1]]
            s += v
        # multiply 2 and devide by # of datapoints
        s = s*2/(len(dataset))
        array.append(s)
    return np.array(array)
        
# =============================================================================
# performs T iterations of gradient descent starting at the given betas and 
# prints the results; does not return anything
# =============================================================================
def iterate_gradient(dataset, cols, betas, T, eta):
    b_array = betas
    for t in range(T):
        print(t+1, end=' ')
        # get gradient_descent
        GRA = gradient_descent(dataset, cols, b_array)
        for i in range(len(betas)):
            b = betas[i] - eta*GRA[i]
            b_array[i] = b
        # print current MSE by func regression
        print('%.2f' % regression(dataset, cols, b_array), end=' ')
        for idx, j in enumerate(b_array):
            if idx == len(b_array)-1: # remove the last space of each print line
                print('%.2f' % j)
            else:   
                print('%.2f' % j, end=' ')

# =============================================================================
# using the closed-form solution, calculates and returns the values of betas 
# and the corresponding MSE as a tuple
# =============================================================================
def compute_betas(dataset, cols):
    first_c = np.ones((len(dataset),1))
    ds = dataset[:, cols]
    ds = np.hstack((first_c, ds))
    ds_tr = np.transpose(ds)
    ds_in = ds_tr @ ds
    ds_in = np.linalg.inv(ds_in)
    beta = ds_in @ ds_tr
    y = dataset[:, 0]
    beta = beta @ y
    MSE = regression(dataset, cols, beta)
    tup = (MSE,)
    tup += tuple(beta)
    return tup

# =============================================================================
# using the closed-form solution betas, return the predicted body fat percentage 
# of the give features.
# =============================================================================
def predict(dataset, cols, features):
    c = compute_betas(dataset, cols)
    v = c[1]
    for i in range(len(features)):
        v += c[i+2]*features[i]
    return v

# =============================================================================
# performs stochastic gradient descent, prints results as in function 5
# =============================================================================
def sgd(dataset, cols, betas, T, eta):
    b_array = betas
    random_generator = random_index_generator(0, len(dataset))
    for t in range(T):
        print(t+1, end=' ')
        # get gradient_descent
        array = []
        
        n = next(random_generator)
        for i in range(len(betas)):
            s = 0
            # iterate each row in dataset
            v = betas[0]
            for j in range(len(cols)):
                v += betas[j+1]*dataset[n][cols[j]]
            v -= dataset[n][0]
            if i == 0:
                pass
            else: # multiply x(i) if it is beta(i)
                v = v*dataset[n][cols[i-1]]
            s += v
            # multiply 2 
            s = s*2
            array.append(s)
        GRA = array
        
        for i in range(len(betas)):
            b = betas[i] - eta*GRA[i]
            b_array[i] = b
        # print current MSE by func regression
        print('%.2f' % regression(dataset, cols, b_array), end=' ')
        for idx, j in enumerate(b_array):
            if idx == len(b_array)-1: # remove the last space of each print line
                print('%.2f' % j)
            else:   
                print('%.2f' % j, end=' ')
    
    
def random_index_generator(min_val, max_val, seed=42):
    """
    DO NOT MODIFY THIS FUNCTION.
    DO NOT CHANGE THE SEED.
    This generator picks a random value between min_val and max_val,
    seeded by 42.
    """
    random.seed(seed)
    while True:
        yield random.randrange(min_val, max_val)
        
        
    
    
    