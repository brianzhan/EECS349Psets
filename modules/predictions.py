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
    data, attr = parse(predict, False)
    output = []
    dict = [] # for storing the nodes
    eNode = None
    for eData in data:
    	# create the node
    	eNode = Node()
    	eNode[element].data = tree.classify(eData)
    for eAttr in attr:
    	print "attribute is ", eAttr
    	print "name is ", eAttr['name']
    	eNode.name = eAttr['name']
    	eNode.is_nominal = eAttr['is_nominal']
    dict.append(eNode)