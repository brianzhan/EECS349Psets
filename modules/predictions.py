import os.path
from node import Node
from operator import xor
from parse import *
import csv


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
    print "print tree"
    tree.print_tree()
    winners = []
    # read 13 columns
    with open(predict, 'rb') as f:
    	reader = csv.reader(f)
    	for row in reader:
    		data = []
    		for item in row[:-1]:
    			try:
    				data.append(float(item))
    			except:
    				data.append(item)
    		data.insert(0, "?") # inserting ? in beginning of each data (place-holder for winner)
    		# print data
    		winner = tree.classify(data)
    		winners.append(winner)
	with open("predictions.csv",'wb') as wf:
   	# Using dictionary keys as fieldnames for the CSV file header
	   writer = csv.writer(wf, dialect='excel')
	   for winner in winners:
	   		writer.writerow([winner])
	# print winners






