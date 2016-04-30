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

def check_classify():
    n0 = Node()
    n0.label = 1
    i = 0;
    if n0.classify([0, 1, 2]) == 1:
        print "Passed 1"
        i += 1
    else:
        print "Failed 1"
    n1 = Node()
    n1.label = 0
    n = Node()
    n.label = None
    n.decision_attribute = 1
    n.is_nominal = True
    n.name = "You saw the attributes what do you think?"
    n.children = {1: n0, 2: n1}
    if n.classify([0, 2]) == 0:
        print "Passed 2"
        i += 1
    else:
        print "Failed 2"
    if i == 2:
        print "All tests passed"
    else:
        print "Not all tests passed, look at classify"


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
            return self.children[instance[self.decision_attribute]].classify(instance)
        else:            #numerical 
            if instance[self.decision_attribute] < self.splitting_value and self.children[0] != None:
                print "classifying numerical, classifying children of ", self.children
                print "instance is ", instance
                return self.children[0].classify(instance)
            elif self.children[1] != None:
                print "classifying nominal"
                return self.children[1].classify(instance)
            else:
                print "classify failed, returning none"
                return None

    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here
        pass


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        pass
