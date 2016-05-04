import os.path
from operator import xor
from parse import *

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    data,attributes = parse(predict, False)
    for element in data:
    	output[element] = tree.classify(element)

    with open('some.csv', 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerows(output)
