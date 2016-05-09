# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on  
from copy import *

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
        if self.label != None:
            #print "returning" + str(self.label)
            return self.label
        if self.is_nominal == True: 
            #print 'here'
            #print instance
            #print self.decision_attribute
            #print instance[self.decision_attribute]
            #print 'i am here'
            #print instance[self.decision_attribute]
            try:
                return self.children[instance[self.decision_attribute]].classify(instance)
            except KeyError:
                # print "\n\n\n threw key error \n\n\n"
                # if children is not found in children, use mode of the examples at this node instead
                for key in self.children:
                    return self.children[key].classify(instance) # STILL NEED TO RETURN MODE INSTEAD OF FIRST CHILD
        else:
            if self.decision_attribute is None:
                # print "decision attribute was none"
                return None
                    #numerical 
            if instance[self.decision_attribute] < self.splitting_value and self.children[0] != None:
                # print "classifying numerical, classifying children of ", self.children
                # print "instance is ", instance
                return self.children[0].classify(instance)
            elif self.children[1] != None:
                # print "classifying nominal"
                return self.children[1].classify(instance)
            else:
                # print "classify failed, returning none"
                return None

    def print_tree(self):
        thislevel = [self]
        while thislevel:
            nextlevel = []
            for n in thislevel:
                if n.label is not None:
                    print n.label,
                else:
                    print n.name, # prints decision attribute
                    for key, child in n.children.iteritems():
                        nextlevel.append(child)
            print
            thislevel = nextlevel

    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        self.print_dnf_tree_recurse(self)

    def print_dnf_tree_recurse(self, node, lineage=[]):
        new_lineage = deepcopy(lineage)
        if node.label is not None:
            if node.label == 1:
                print "(",
                for name in new_lineage[:-1]:
                    print str(name) + " AND",
                print new_lineage[-1] + " )"
                print "OR"
        else:
            if not node.is_nominal:
                new_lineage1 = deepcopy(lineage)
                new_lineage1.append(str(node.name) + " < " + str(node.splitting_value))
                if new_lineage1 is not None:
                    self.print_dnf_tree_recurse(node.children[0], new_lineage1)
                new_lineage2 = deepcopy(lineage)
                new_lineage2.append(str(node.name) + " >= " + str(node.splitting_value))
                if new_lineage2 is not None:
                    self.print_dnf_tree_recurse(node.children[1], new_lineage2)
            else:
                for key, child in node.children.iteritems():
                    new_lineage = deepcopy(lineage)
                    if new_lineage is not None:
                        new_lineage.append(str(node.name) + "=" + str(key))
                    self.print_dnf_tree_recurse(child, new_lineage)
        
