from node import Node
from ID3 import *
from operator import xor
from copy import *

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
    '''
    # NEED TO START FROM THE LEAF
    stack = []
    stack.append(root)
    num_pruned = 0 # number of nodes pruned
    while stack:
        subtree_nodes = [] # nodes to explore for each subtree
        node = stack.pop(0)
        node_copy = deepcopy(node)
        old_validation = validation_accuracy(root, validation_set) # original accuracy before pruning the sub-tree
        # construct new subtree
        labels = [] # data set of all the labels under this subtree
        while subtree_nodes:
            tree_node = subtree_nodes.pop(0)
            if tree_node.label is not None: # if node is a leaf
                labels.append([tree_node.label])
            elif tree_node.is_nominal:
                for key, child in tree_node.children:
                    subtree_nodes.insert(0, child)
            else:
                for child in tree_node.children: # add children to stack (might have to check if nominal or not)
                    subtree_nodes.insert(0, child)
        # prune the tree at this node
        label = mode(labels)
        node.label  = label
        node.children = None
        node.decision_attribute = None
        node.is_nominal = None
        node.splitting_value = None
        node.name = None
        new_validation = validation_accuracy(root, validation_set) # get the validation accuracy of the new tree
        if new_validation >= old_validation: # keep the prune if new validation is higher than old
            num_pruned += 1
        else:
            node = node_copy # revert pruning
        # then add the children of this node to the stack if it was not pruned
        if node.children is not None:
            if node.is_nominal:
                for key, child in node.children:
                    stack.insert(0, child)
                    subtree_nodes.insert(0, child)
            else:
                for child in node.children: # add children to stack (might have to check if nominal or not)
                    stack.insert(0, child)
                    subtree_nodes.insert(0, child)
    if num_pruned > 0:
        root = reduced_error_pruning(root, training_set, validation_set) # calls the pruning function again if a node was pruned
    return root

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
