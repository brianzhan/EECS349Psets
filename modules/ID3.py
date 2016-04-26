import math
from node import Node
import sys

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
    maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''
    entropy_bound = 0.15 # entropy of data_set must be below bound to become a leaf
    if entropy(data_set) < entropy_bound or depth == 0:
        node = Node() # create a new node leaf
        node.label = mode(data_set)
        return node
    pick_best = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) # tuple
    best_attribute = pick_best[0] # best attribute to split on
    split_value = pick_best[1] # best value to split on
    if split_value is not False: # if there is a split value (best_attribute is numeric)
        split_data = split_on_numerical(data_set, best_attribute, split_value) # splitting data by split value (lesser, greater)
        node = Node()
        node.is_nominal = False # node is numeric
        node.splitting_value = split_value # best value to split on
        node.children[1] = ID3(split_data[0], attribute_metadata, numerical_splits_count, depth - 1) # less than split value
        node.children[2] = ID3(split_data[1], attribute_metadata, numerical_splits_count, depth - 1) # greater than split value
        node.name = attribute_metadata[best_attribute]['name']
        node.decision_attribute = best_attribute # best attribute to split on
    else: # best_attribute is nominal
        split_data = split_on_nominal(data_set, best_attribute) # returns a dictionary with nominal attributes as keys
        node = Node()
        node.is_nominal = True # node is nominal
        i = 1
        for key in split_data: # add a children for each nominal attribute
            node.children[i] = ID3(split_data[key], attribute_metadata, numerical_splits_count, depth - 1)
            i += 1
        node.name = attribute_metadata[best_attribute]['name']
        node.decision_attribute = best_attribute

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    value = data_set[0][0]
    for data in data_set: 
        if data[0] is not value:
            return None
    return value
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    num_attributes = len(data_set[0]) # number of attributes in total
    gain_ratios = {} # dictionary to map attributes to their (gain ratio, best split value)
    highest_ratio = 0 # used to keep track of highest value
    best_attribute = 0 # used to keep track of attributes index with highest gain ratio
    # find the gain ratios for each attribute
    for i in range(1, num_attributes):
        is_nominal = attribute_metadata[i]['is_nominal']
        if is_nominal:
            gain_ratio = gain_ratio_nominal(data_set, i)
            gain_ratios[i] = (gain_ratio, False)
        else:
            gain_ratio = gain_ratio_numeric(data_set, i, 1)
            gain_ratios[i] = gain_ratio
    # go through each attribute's gain ratio and find the highest one
    for key, value in gain_ratios.iteritems(): 
        if value[0] > highest_ratio:
            highest_ratio = value[0]
            best_attribute = key
    if best_attribute == 0 or numerical_splits_count[best_attribute] == 0:
        return (False, False)
    numerical_splits_count[best_attribute] -= 1
    return (best_attribute, gain_ratios[best_attribute][1])
    # STILL NEED TO USE NUMERICAL_SPLITS_COUNT

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    value_freq = {} # tracks frequency of each value
    most_frequent = 0; # tracks the most frequent number
    mode = None
    for data in data_set:
        value = data[0]
        if value not in value_freq:
            value_freq[value] = 1
        else:
            value_freq[value] += 1
    for key, frequency in value_freq.iteritems():
        if frequency > most_frequent:
            most_frequent = frequency
            mode = key
    return mode
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. Number between 0-1. See Textbook for formula
    ========================================================================================================
    '''
    entropy = 0
    value_freq = {} # tracks frequency of each value
    total_values = 0 # total amount of values
    for data in data_set:
        value = data[0]
        if value not in value_freq: # if value is not a key in value_freq
            value_freq[value] = 1
        else:
            value_freq[value] += 1
        total_values += 1
    for key, frequency in value_freq.iteritems():
        fraction = float(frequency)/float(total_values)
        entropy -= fraction * math.log(fraction, 2)
    return entropy


# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, attribute index
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See Textbook for formula
    ========================================================================================================
    '''
    gain = entropy(data_set) # information gain
    intrinsic = 0
    attributes = {} # tracks the number of classified 1's and 0's for each attribute (dictionary of dictionaries)
    total_variables = 0
    for data in data_set:
        variable = data[0] # the classification
        nominal_attribute = data[attribute] # the nominal attribute
        # tracking the amount of 0 and 1 classifications for each nominal attribute
        if nominal_attribute not in attributes:
            if variable == 1:
                attributes[nominal_attribute] = [[1]]
            else:
                attributes[nominal_attribute] = [[0]]
        else:
            if variable == 1:
                attributes[nominal_attribute].append([1])
            else:
                attributes[nominal_attribute].append([0])
        total_variables += 1 
    for key, frequency in attributes.iteritems():
        entropy_attribute = entropy(attributes[key]) 
        attribute_count = len(attributes[key]) 
        fraction = float(attribute_count)/float(total_variables)
        gain -= fraction * entropy_attribute
        intrinsic -= fraction * math.log(fraction, 2)
    return gain/intrinsic

# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

# def gain_ratio_numeric(data_set, attribute, steps):
#     '''
#     ========================================================================================================
#     Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
#     ========================================================================================================
#     Job:    Calculate the gain_ratio_numeric and find the best single threshold value
#             The threshold will be used to split examples into two sets
#                  those with attribute value GREATER THAN OR EQUAL TO threshold
#                  those with attribute value LESS THAN threshold
#             Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
#             And restrict your search for possible thresholds to examples with array index mod(step) == 0
#     ========================================================================================================
#     Output: This function returns the gain ratio and threshold value
#     ========================================================================================================
#     '''
#     data_len = len(data_set)
#     iterations = (data_len / steps) 
#     if iterations == 0: #CHECK IF THIS IS CORRECT
#         iterations = 1
#     most_gain = 0 # keeps track of which split gives the least entropy
#     split_index = None
#     intrinsic = 0
#     for i in range(iterations): # iterations of splitting data_set at indices i*step
#         split_data = split_on_numerical(data_set, attribute, data_set[i*steps][attribute]) # splits data on i*step'th attribute
#         entropy_1 = entropy(split_data[0])
#         entropy_2 = entropy(split_data[1])
#         fraction_1 = float(len(split_data[0]))/float(data_len)
#         fraction_2 = float(len(split_data[1]))/float(data_len)
#         gain = entropy(data_set) - fraction_1 * entropy_1 - fraction_2 * entropy_2
#         if gain > most_gain:
#             most_gain = gain
#             split_index = i
#             intrinsic = 0 - fraction_1 * math.log(fraction_1, 2) - fraction_2 * math.log(fraction_2, 2)
#     return (most_gain/intrinsic, data_set[split_index*steps][attribute])

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    possible_thresholds = []
    best_information_gain_ratio = -10000
    best_threshold = 0
    information_gain_ratio = -10000
    for i in range(0,len(data_set)):
        if i % steps == 0:
            possible_thresholds.append(data_set[i][attribute])
    #print possible_thresholds
    for threshold in possible_thresholds:
        mag_total = len(data_set)
        split = split_on_numerical(data_set,attribute,threshold)
        num_subsets = len(split)
        gain_sum = 0
        intrinsic_value = 0
        for x in range(0,2):
            mag_subset = len(split[x])
            if mag_subset != 0:
                gain_sum += float(mag_subset)/float(mag_total)* entropy(split[x])
                intrinsic_value += float(mag_subset)/float(mag_total)*math.log(float(mag_subset)/float(mag_total),2)

        information_gain = entropy(data_set) - gain_sum
        intrinsic_value = -intrinsic_value
        if intrinsic_value != 0:
            information_gain_ratio = information_gain/intrinsic_value
        if information_gain_ratio > best_information_gain_ratio:
            best_threshold = threshold
            best_information_gain_ratio = information_gain_ratio
    #print (best_information_gain_ratio,best_threshold)
    return (best_information_gain_ratio,best_threshold)
    
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.21744375685031775, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Takes in a data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    output = {}
    for data in data_set:
        nominal_attribute = data[attribute]
        if nominal_attribute not in output: # if key does not exist in dictionary
            output[nominal_attribute] = [data] # initializes a new list with data
        else:
            output[nominal_attribute].append(data) # appends the data to the already existing list
    return output
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Takes in a data set, the index for a numeric attribute, splitting value from gain_ratio
    ========================================================================================================
    Job:    Categorizes data_set into a list that is greater than or equal to the splitting value and lower.
    ========================================================================================================
    Output: Data less than splitting value and data that is equal to or greater than the splitting value
    ========================================================================================================
    '''
    less = []
    greater = []
    for data in data_set:
        if data[attribute] < splitting_value:
            less.append(data)
        else:
            greater.append(data)
    return less, greater
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])
