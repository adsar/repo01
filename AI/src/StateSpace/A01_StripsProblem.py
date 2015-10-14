'''
Created on Feb 8, 2015

@author: adrian
'''
import StateSpace.StripsDomain as strips

def main():

    # Planning Domain: Operator definition
    operators = []
        
    op1_precs = strips.FOLiteralList()
    op1_precs.add(strips.FOLiteral('+', 'S', ['x1', 'x2']))
    op1_precs.add(strips.FOLiteral('+', 'R', ['x3', 'x1']))
                  
    op1_effect = strips.FOLiteralList()   
    op1_effect.add(strips.FOLiteral('+', 'S', ['x2', 'x1']))
    op1_effect.add(strips.FOLiteral('+', 'S', ['x1', 'x3']))
    op1_effect.add(strips.FOLiteral('-', 'R', ['x3', 'x1']))
    
    operators.append(strips.Operator('op1', ['x1', 'x2', 'x3'], op1_precs, op1_effect))
        
    op1_precs = strips.FOLiteralList()
    op1_precs.add(strips.FOLiteral('+', 'S', ['x3', 'x1']))
    op1_precs.add(strips.FOLiteral('+', 'R', ['x2', 'x2']))
                  
    op1_effect = strips.FOLiteralList()   
    op1_effect.add(strips.FOLiteral('+', 'S', ['x1', 'x3']))
    op1_effect.add(strips.FOLiteral('-', 'S', ['x3', 'x1']))
    
    operators.append(strips.Operator('op2', ['x1', 'x2', 'x3'], op1_precs, op1_effect))
    
    # Planning Problem: State definition
    s_init = strips.FOLiteralList()
    s_goal = strips.FOLiteralList()

    s_init.add(strips.FOLiteral('+', 'S', ['B', 'B']))
    s_init.add(strips.FOLiteral('+', 'S', ['C', 'B']))
    s_init.add(strips.FOLiteral('+', 'S', ['A', 'C']))
    s_init.add(strips.FOLiteral('+', 'R', ['B', 'B']))
    s_init.add(strips.FOLiteral('+', 'R', ['C', 'B']))
    
    s_goal.add(strips.FOLiteral('+', 'S', ['A', 'A']))
        


    statSpaceSearch = strips.StateSpaceSearch(s_init, s_goal, operators)
    print 'Forward Search'
    for a in statSpaceSearch.getApplicableActions(statSpaceSearch.s_init):
        print a
   
    print
    #print 'Backwards Search'
    #for a in statSpaceSearch.getRelevantActions(statSpaceSearch.s_goal):
    #    print a
    
    return    
    
if __name__ == '__main__':
    main()