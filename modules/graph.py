import random 
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
from copy import *
import numpy as np
from modules.pruning import *

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    total_data = len(train_set)
    train_num = float(total_data)*pct # amount of data to train on
    pct_train_set = random.sample(train_set, int(train_num))
    tree = ID3(pct_train_set, attribute_metadata, numerical_splits_count, 20)
    reduced_error_pruning(tree, pct_train_set, validate_set)
    # tree.print_tree()
    accuracy = validation_accuracy(tree, validate_set)
    print str(pct) + ": " + str(accuracy)
    return accuracy


def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    accuracies = [] # accuracies is a dictionary of lists (key = pct, value = list of accuracies for that pct)
    for pct in pcts:
        for i in xrange(0, iterations):
            splits = deepcopy(numerical_splits_count)
            # print "splits is : " + str(splits) 
            accuracy = get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, splits, pct)
            accuracies.append(accuracy)
    #         if pct not in accuracies: 
    #             accuracies[pct] = [accuracy]
    #         else:
    #             accuracies[pct].append(accuracy)
    # for key, value in accuracies.iteritems():
    #     value.sort()
    return accuracies

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    pcts = np.linspace(lower,upper)
    pcts = pct.tolist()
    print pcts
    avg_data = []
    accuracies = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts)
    for accuracy in accuracies:
        curr_accuracies = []
        for i in range(0, iterations):
            curr_accuracies = accuracies.pop(0)
        average = sum(curr_accuracies) / float(len(curr_accuracies))
        avg_data.append(average)
    plt.plot(pcts, data)
    plt.xlabel('Percentage Trained')
    plt.ylabel('Accuracy With Crossfold')
    plot.show()
