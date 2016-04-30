from node import Node
from ID3 import *
from operator import xor

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    This function uses a dfs type of iteration to iterate through all nodes to check if replacing them
    with a leaf node would increase validation accuracy
    '''
    old_validation = validation_accuracy(root, validation_set)
    
    # old_validation = validation_accuracy(root,validation_set)
    # stack = []
    # stack.append(root)
    # node_pruned = -1
    # counter = 0
    # while len(stack) != 0:
    #     tree = stack.pop(0)
    #     for subtree in tree.children:
    #         stack.insert(0,subtree)
    #     #### need to figure out how to set the value of this current node to its most popular value below it 
    #     #make the change
    #     new_validation = validation_accuracy(root,validation_set)
    #     if (new_validation > old_validation):
    #         node_pruned = counter
    #     #restore the tree back to its old shape
    #     counter += 1

    # counter = 0
    # stack.append(root)
    # while len(stack) != 0:
    #     tree = stack.pop(0)
    #     for subtree in tree.children:
    #         stack.insert(0,subtree)
    #     if node_pruned == counter:
    #         #prune the node here
    #         print prune 
    #         return   #return out of the function
    #     counter += 1

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    wrong_count = 0 # wrongly classified
    correct_count = 0 # correctly classified
    total = 0
    for data in validation_set:
        classification = tree.classify(data)
        if classification == data[0]: # if correctly classified
            correct_count += 1
        else: 
            wrong_count += 1 
        total += 1
    return float(correct_count)/float(total)
