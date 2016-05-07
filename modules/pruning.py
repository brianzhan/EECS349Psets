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
    stack = []
    stack.append(root)
    old_validation = validation_accuracy(root, validation_set) # original accuracy before pruning the sub-tree
    while stack:
        node = stack.pop(0)
        print "old tree"
        root.print_tree()
        subtree_nodes = [node] # nodes to explore for each subtree
        node_copy = deepcopy(node) # creates a copy of the original node in case the prune is not necessary
        # construct new subtree
        labels = [] # data set of all the labels under this subtree
        while subtree_nodes:
            tree_node = subtree_nodes.pop(0)
            if tree_node.label is not None: # if node is a leaf
                labels.append([tree_node.label])
            else:
                for key, child in tree_node.children.iteritems():
                    subtree_nodes.append(child)
        # prune the tree at this node
        label = mode(labels)
        # make copies of old node stuff
        old_label = deepcopy(node.label)
        old_children = deepcopy(node.children)
        old_decision_attribute = deepcopy(node.decision_attribute)
        old_is_nominal = deepcopy(node.is_nominal)
        old_splitting_value = deepcopy(node.splitting_value)
        old_name = deepcopy(node.name)
        # set current node as leaf 
        node.label  = label
        node.children = None
        node.decision_attribute = None
        node.is_nominal = None
        node.splitting_value = None
        node.name = None
        print "new tree"
        root.print_tree()
        new_validation = validation_accuracy(root, validation_set) # get the validation accuracy of the new tree
        print "old validation acc " + str(old_validation)
        print "new validation acc " + str(new_validation)
        if new_validation - old_validation >= 0.000001: # keep the prune if new validation is higher than old
            return
        else:
            print "changes reverted"
            # revert pruning
            node.label  = old_label
            node.children = old_children
            node.decision_attribute = old_decision_attribute
            node.is_nominal = old_is_nominal
            node.splitting_value = old_splitting_value
            node.name = old_name
        # then add the children of this node to the stack if it was not pruned
        if node.children is not None:
            # if node.is_nominal:
            for key, child in node.children.iteritems():
                stack.append(child)
                    # subtree_nodes.insert(0, child)
            # else:
            #     for child in node.children: # add children to stack (might have to check if nominal or not)
            #         stack.append(child)
            #         # subtree_nodes.insert(0, child)

# def reduced_error_pruning(root,training_set,validation_set):
#     '''
#     take the a node, training set, and validation set and returns the improved node.
#     You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
#     NOTE you will probably not need to use the training set for your pruning strategy, but it's passed as an argument in the starter code just in case.
#     '''
#     stack = []
#     stack.append(root)
#     num_pruned = 0 # number of nodes pruned
#     while stack:
#         subtree_nodes = [] # nodes to explore for each subtree
#         node = stack.pop(0)
#         node_copy = deepcopy(node) # creates a copy of the original node in case the prune is not necessary
#         old_validation = validation_accuracy(root, validation_set) # original accuracy before pruning the sub-tree
#         # construct new subtree
#         labels = [] # data set of all the labels under this subtree
#         while subtree_nodes:
#             tree_node = subtree_nodes.pop(0)
#             if tree_node.label is not None: # if node is a leaf
#                 labels.append([tree_node.label])
#             elif tree_node.is_nominal:
#                 for key, child in tree_node.children:
#                     subtree_nodes.insert(0, child)
#             else:
#                 for child in tree_node.children: # add children to stack (might have to check if nominal or not)
#                     subtree_nodes.insert(0, child)
#         # prune the tree at this node
#         label = mode(labels)
#         node.label  = label
#         node.children = None
#         node.decision_attribute = None
#         node.is_nominal = None
#         node.splitting_value = None
#         node.name = None
#         new_validation = validation_accuracy(root, validation_set) # get the validation accuracy of the new tree
#         if new_validation >= old_validation: # keep the prune if new validation is higher than old
#             num_pruned += 1
#         else:
#             node = node_copy # revert pruning
#         # then add the children of this node to the stack if it was not pruned
#         if node.children is not None:
#             if node.is_nominal:
#                 for key, child in node.children.iteritems():
#                     stack.append(child)
#                     subtree_nodes.insert(0, child)
#             else:
#                 for key, child in node.children.iteritems(): # add children to stack (might have to check if nominal or not)
#                     stack.append(child)
#                     subtree_nodes.insert(0, child)
#     if num_pruned > 0:
#         # since we didn't start pruning from a leaf, this is a work around
#         root = reduced_error_pruning(root, training_set, validation_set) # calls the pruning function again if a node was pruned
#     return root

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    wrong_count = 0 # wrongly classified
    correct_count = 0 # correctly classified
    total = 0
    for data in validation_set:
        # print "data is: " + str(data)
        classification = tree.classify(data)
        if classification == data[0]: # if correctly classified
            correct_count += 1
        else: 
            wrong_count += 1 
        total += 1
    return float(correct_count)/float(total)
