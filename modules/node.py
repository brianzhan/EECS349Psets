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

def check_dnf():
    n0 = Node()
    n0.children = {1: n2, 2: n3}

    n1 = Node()
    n1.label = 1

    n2 = Node()
    n2.label = 2

    n3 = Node()
    n3.label = 3

    n = Node()
    n.label = 5
    n.decision_attribute = 1
    n.is_nominal = True
    n.children = {0: n0, 1: n1}
    n0.children = {0: n2, 1: n3}
    n.print_dnf_tree()
"""
                n
               / \ 
              n0  n1
             / \  
            n2 n3

            5 AND 0 AND 2
            5 AND 0 AND 3
            5 AND 1
"""    

def dnf_helper(child):
    for c in child:
        print "child: ", c
        print " OR "

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
                return 0 # WILL NEED TO CHANGE THIS
        else:            #numerical 
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
        current = self
        s = []
        s.append(current)
        s.append(str(current.label))
        while s and s != []: # s is empty
            path = s.pop()
            current = s.pop()

            # find out whether childs exist
            leftChild=1
            rightChild=1
            try:
                current.children[0]
            except KeyError:
                leftChild = 0
            try:
                current.children[1]
            except KeyError:
                rightChild = 0

            if leftChild is 0 and rightChild is 0:
                print path, " OR "
            if leftChild is 1:
                rightStr = path + " AND " +str(current.children[0].label)
                s.append(current.children[0])
                s.append(rightStr)
            if rightChild is 1:
                leftStr = path + " AND " + str(current.children[1].label)
                s.append(current.children[1])
                s.append(leftStr)

    def old_print_dnf(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        # handle tree end exceptions
        leftChild=1
        rightChild=1
        try:
            self.children[0]
        except KeyError:
            leftChild = 0
        try:
            self.children[1]
        except KeyError:
            rightChild = 0
        # print trees
        if leftChild is 0 and rightChild is 0:
            print self.label, " OR "
        else:
            print self.label, " AND ",

        if leftChild is 1 and self.children[0] != {}:
            newChild = self.children[0]
            newChild.print_dnf_tree()
        if rightChild is 1 and self.children[1] != {}:
            newChild = self.children[1]
            newChild.print_dnf_tree()

def main():
    check_dnf()

if __name__ == "__main__":
    main()




