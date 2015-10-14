'''
Created on Feb 8, 2015

@author: adrian
'''
import copy

class StateSpaceSearch:
    def __init__(self, s_init, s_goal, operators):
        self.s_init = s_init
        self.s_goal = s_goal
        self.operators = operators
    
    def fwSearch(self):
        state = self.s_init
        plan = []
        while True:
            if state.satisfies(self.s_goal):
                return plan
            applicables = self.getApplicableActions(state)
            if applicables.isEmpty():
                return False
            action = applicables[0]
            state = self.gamma(state, action)
            plan.append(action)
   
    def getApplicableActions(self, s):
        A = []
        for op in self.operators:
            self.addApplicables(A, op, op.precondition, Sustitution(), s) 
        return A
  
    def addApplicables(self, A, op, prec, sust, s):
        prec_plus = prec.positive()
        if len(prec_plus) == 0:
            for np in prec.negative():
                np_instan = sust.instantiate(np)
                if s.falsifies(np_instan): 
                    return
            op_instan = op.instantiate(sust)
            if op_instan not in A:
                A.append(op_instan)
        else:
            pp = prec_plus[0]
            for sp in s.all:
                if not sp.match(pp):
                    continue   #predicate doesn't match
                sust1 = sust.deepcopy()
                if sust1.extend(pp, sp):
                    prec1 = prec.deepcopy()
                    prec1.remove(0)
                    self.addApplicables(A, op, prec1, sust1, s)

   
    def bwSearch(self):
        state = self.s_init
        plan = []
        while True:
            if state.satisfies(self.s_init):
                return plan
            relevants = self.getRelevanActions(state)
            if relevants.isEmpty():
                return False
            action = relevants[0]
            state = self.gamma(state, action)
            plan.append(action)
   
    def getRelevantActions(self, s):
        A = []
        for op in self.operators:
            self.addApplicables(A, op, op.precondition, Sustitution(), s) 
        return A
  
    def addRelevants(self, A, op, prec, sust, s):
        prec_plus = prec.positive()
        if len(prec_plus) == 0:
            for np in prec.negative():
                np_instan = sust.instantiate(np)
                if s.falsifies(np_instan): 
                    return
            op_instan = op.instantiate(sust)
            if op_instan not in A:
                A.append(op_instan)
        else:
            pp = prec_plus[0]
            for sp in s.all:
                if not sp.match(pp):
                    continue   #predicate doesn't match
                sust1 = sust.deepcopy()
                if sust1.extend(pp, sp):
                    prec1 = prec.deepcopy()
                    prec1.remove(0)
                    self.addApplicables(A, op, prec1, sust1, s)


class Operator(object):
    '''
    Base class for operator
    '''
 
    def __init__(self, name, parameters, precondition, effect):

        self.name = name
        self.parameters = parameters
        self.precondition = precondition
        self.effect = effect
    
    def instantiate(self, sust):
        instance = self.name + '( '
        for p in self.parameters:
            if p not in sust.valueDict:
                instance += p + ' '
            else:
                instance += sust.valueDict[p] + ' '
        instance += ')'
        
        return instance
            

class FOLiteralList(object):
    def __init__(self):
        self.all = []
    
    def fneg(self, x): return (x.sign == '-')
    def fpos(self, x): return (x.sign == '+')
    
    def add(self, p):
        self.all.append(p)

    def negative(self):
        return filter(self.fneg, self.all)

    def positive(self):
        return filter(self.fpos, self.all)
        
    def remove(self, i):
        self.all.remove(self.all[i])     
    
    def deepcopy(self):
        return copy.deepcopy(self) 
    

# First-Order Literal
# A first-order literal is a proposition that can be positive or negative
# the preposition has a predicate and a list of operands
class FOLiteral(object):
    def __init__(self, sign, predicate, operands):

        self.sign = sign
        self.predicate = predicate
        self.operands = operands
    
    def match(self, p):
        return (self.predicate == p.predicate)
    
    def isEqual(self, p):
        return (self.predicate == p.predicate) and (self.operands == p.operands)


class Sustitution(object):
    def __init__(self):

        self.valueDict = {}

    def extend(self, pp, sp):
        for i in range(len(pp.operands)):
            a = pp.operands[i]
            if a not in self.valueDict:
                self.valueDict[a] = sp.operands[i]
            else:
                if self.valueDict[a] != sp.operands[i]:
                    return False #diff values for same var
        return True

    # makes a copy of the dict, but it does not deepcopy the object inside
    def deepcopy(self):
        new_sust = Sustitution()
        new_sust.valueDict = dict(self.valueDict)
        return new_sust
