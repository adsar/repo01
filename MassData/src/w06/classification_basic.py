'''
Created on Nov 11, 2014

@author: adrian
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def q1_classif_svm_hard():
    '''
1. Find the lines through the two positive points and through the two negative points. Put these lines in slope-intercept form, as v=c+au.
2. Find the parallel line through the closer of the points on the other side (same slope; different intercept c)
3. Find the line midway between the two parallels by averaging their intercepts (the c values).
   Write the equation of this line as w.x+b=0.
4. Scale the constants w=(w1,w2) and b, so that:
   w.x+b is at least 1 for positive x, and exactly 1 for the closest (to the boundary) of the positive points. 
   w.x+b must be at most -1 for negative points, but must be exactly -1 for the closest of them.

    To choose the classifier that maximizes the margin, 
    choose the line that minimizes the length of the vector w 
    when you put the separating line in the form w.x+b=0

    '''
    
    x = np.array([5, 4, 8, 3, 7, 2, 3, 3]).reshape([4, 2])
    y = np.array([1, 1, -1, -1])
    
    # 1
    pa = -0.33
    pc = 4.0 + 5.0/3
    
    na = -0.25
    nc = 3.0 + 3.0/4
    
    # 2
    closest_neg = np.array(x[2,:])
    closest_pos = np.array(x[1,:])

    parallel_pc = calc_c_par(pa, pc, closest_neg) 
    parallel_nc = calc_c_par(na, nc, closest_pos) 
    
    #3
    mean_pc = (pc + parallel_pc) / 2.0
    mean_nc = (nc + parallel_nc) / 2.0

    
    #4
    # Alternative 1: Positive points 
    # first condition (equality)
    b = -mean_pc
    pw = np.array([-pa, 1])
    scaling_factor = - (np.dot(pw, x[2,:]) + b)
    # the sign inversion is because if the value is positive we want to turn it into a -1, 
    # and if the value is negative we want to the scaling factor to become a positive number 
    # so it wont invert the sign when applied to the equation
      
    b_scaled = b / scaling_factor
    pw_scaled = pw / scaling_factor
    scaled_value = np.dot(pw_scaled, x[2,:]) + b_scaled   
  
    pw_scaled_norm = np.linalg.norm(pw_scaled) 
        
    print
    print "Positive points (support vectors): (%d, %d)  (%d, %d)" % (x[0,0], x[0,1], x[1,0], x[1,1])
    print "  - Line x2 = a * x1 + c : %5.3f x + %5.3f" % (pa, pc)
    print "  - Closest negative point (support vector): (%d, %d) " % (x[2,0], x[2,1])
    print "  - Line parallel to x2 = a * x1 + c that contains point (%d, %d) : x2 = %5.3f x1 + %5.3f" % (x[2,0], x[2,1], pa, parallel_pc)
    print "  - Line average of the two above : x2 = %5.3f x1 + %5.3f" % (pa, mean_pc)
    print "For the above line (average of the two parallels) convert its equation"      
    print "    from its explicit form :  x2 = a * x1 + c"      
    print "    to its implicit form :  -a * x1 + 1 * x2 - c  = 0    - note that b turns out to be (-c)"      
    print "Average of the two parallels (same gradient, average b) :"      
    print "    w.x + b = 0  :  -a * x1 + 1 * x2 - (c1 + c2)/2  = 0 :  %5.3f * x1 + 1 * x2  %5.3f  =  %5.3f " % (-pa, -mean_pc, 0)
    print "Express the boundary conditions:"
    print "    1) w.x + b = -1 for negative points that are support vectors (X3):  %5.3f * %5.3f + 1 * %5.3f + (%5.3f)  =  %5.3f " % (-pa, x[2,0], x[2,1], -mean_pc, -1)
    print "    2) w.x + b <= -1 for all other negative points (X4):  %5.3f * %5.3f + 1 * %5.3f + (%5.3f)  <=  %5.3f " % (-pa, x[3,0], x[3,1], -mean_pc, -1)
    print "Scale w and b (shrink or expand proportionally) so that verifies the above conditions"
    print "    b = %5.3f" % (b)
    print "    w = [%5.3f, %5.3f]" % (pw[0], pw[1])
    print "    scaling_factor = - (w.x + b) = %5.2f" % (scaling_factor)
    print "    scaled b = b / scaling_factor = %5.3f" % (b_scaled)
    print "    scaled w = w / scaling_factor = [%5.3f, %5.3f]" % (pw_scaled[0], pw_scaled[1])
    print "    for x=(%d, %d), the scaled w.x + b = %5.2f  => meets condition (1)" % (x[2,0], x[2,1], scaled_value)  
    print "    for x=(%d, %d), the scaled w.x + b = %5.2f  => meets condition (2)" % (x[3,0], x[3,1], np.dot(pw_scaled, x[3,:]) + b_scaled)  
    print "    |scaled w| = %5.3f" % (pw_scaled_norm)
    hyperplanes = {}
    hyperplanes["x2=a*x1+c"] = calc_hyperplane(pa, pc)
    hyperplanes["x2=a*x1+c_par"] = calc_hyperplane(pa, parallel_pc)     
    hyperplanes["w.x + b = 0"] = calc_hyperplane(-pw_scaled[0]/pw_scaled[1], -b_scaled/pw_scaled[1])   
    plot_SVM('SVM - Positive Points', x, y, hyperplanes, pw_scaled)
    
    # Alternative 2: Negative points 
    # first condition (equality)
    b = -mean_nc
    nw = np.array([-na, 1])
    scaling_factor = (np.dot(nw, x[1,:]) + b)
      
    b_scaled = b / scaling_factor
    nw_scaled = nw / scaling_factor
    scaled_value = np.dot(nw_scaled, x[1,:]) + b_scaled  
    
    nw_scaled_norm = np.linalg.norm(nw_scaled) 
    
    print
    print "Negative points (support vectors): (%d, %d)  (%d, %d)" % (x[0,0], x[0,1], x[1,0], x[1,1])
    print "  - Line x2 = a * x1 + c : %5.3f x + %5.3f" % (na, nc)
    print "  - Closest positive point (support vector): (%d, %d) " % (x[1,0], x[1,1])
    print "  - Line parallel to x2 = a * x1 + c that contains point (%d, %d) : x2 = %5.3f x1 + %5.3f" % (x[1,0], x[1,1], na, parallel_nc)
    print "  - Line average of the two above : x2 = %5.3f x1 + %5.3f" % (na, mean_nc)
    print "For the above line (average of the two parallels) convert its equation"      
    print "    from its explicit form :  x2 = a * x1 + c"      
    print "    to its implicit form :  -a * x1 + 1 * x2 - c  = 0    - note that b turns out to be (-c)"      
    print "Average of the two parallels (same gradient, average b) :"      
    print "    w.x + b = 0  :  -a * x1 + 1 * x2 - (c1 + c2)/2  = 0 :  %5.3f * x1 + 1 * x2  %5.3f  =  %5.3f " % (-na, -mean_nc, 0)
    print "Express the boundary conditions:"
    print "    1) w.x + b = 1 for positive points that are support vectors :  %5.3f * %5.3f + 1 * %5.3f + (%5.3f)  =  %5.3f " % (-na, x[1,0], x[1,1], -mean_nc, -1)
    print "    2) w.x + b >= 1 for all other positive points :  %5.3f * %5.3f + 1 * %5.3f + (%5.3f)  <=  %5.3f " % (-na, x[2,0], x[2,1], -mean_nc, -1)
    print "Scale w and b (shrink or expand proportionally) so that verifies the above conditions"
    print "    b = %5.3f" % (b)
    print "    w = [%5.3f, %5.3f]" % (nw[0], nw[1])
    print "    scaling_factor = - (w.x + b) = %5.2f" % (scaling_factor)
    print "    scaled b = b / scaling_factor = %5.3f" % (b_scaled)
    print "    scaled w = w / scaling_factor = [%5.3f, %5.3f]" % (nw_scaled[0], nw_scaled[1])
    print "    for x=(%d, %d), the scaled w.x + b = %5.2f  => meets condition (1)" % (x[1,0], x[1,1], scaled_value)  
    print "    for x=(%d, %d), the scaled w.x + b = %5.2f  => meets condition (2)" % (x[0,0], x[0,1], np.dot(nw_scaled, x[0,:]) + b_scaled)  
    print "    |scaled w| = %5.3f" % (nw_scaled_norm)
    hyperplanes = {}
    hyperplanes["x2=a*x1+c"] = calc_hyperplane(na, nc)
    hyperplanes["x2=a*x1+c_par"] = calc_hyperplane(na, parallel_nc)     
    hyperplanes["w.x + b = 0"] = calc_hyperplane(-nw_scaled[0]/nw_scaled[1], -b_scaled/nw_scaled[1])   
    plot_SVM('SVM - Negative Points', x, y, hyperplanes, nw_scaled)
    
    print "Conclusion:"
    print "the optimum is alternative 1 (positive points) because it minimizes |w| => maximizes sigma"
    


def calc_c_par(a, c, x_opposite):
    x2 = a * x_opposite[0] + c
    d = x_opposite[1] - x2
    c_par = c + d
    
    return c_par

def calc_hyperplane(a, c):
    hyper_plane = np.array([np.zeros(20)]).reshape([10, 2])
    for x in range(10):
        hyper_plane[x,0] = x
        hyper_plane[x,1] = a * x + c
    
    return hyper_plane

def plot_SVM(plot_title, x, y, hyperplanes, w):
    plt.clf()

    plt.title(plot_title)
        
    # Plot the Points 
    for i in range(len(x)):
        c = 'r' if y[i] > 0 else 'b'
        plt.plot(x[i,0], x[i,1], marker='o', linestyle='None', color=c)
    
    # Plot the hyperplanes (candidate classifiers)
    for hyp_name in hyperplanes.keys():
        hp = hyperplanes[hyp_name]
        c = 'k' if 'w.x' in hyp_name else 'y' if 'f1' in hyp_name else  'g'        
        plt.plot(hp[:,0], hp[:,1], marker='None', linestyle='--', color=c, label=hyp_name)
    
    plt.plot(w[0], w[1], marker='s', linestyle='None', color='y')
    
    #plt.legend(hyperplanes.keys())
    
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.grid(True)
    
    plt.xlim(-4,10)
    plt.ylim(-4,10)
    plt.axvline(x=0, color='k', alpha=1.0)   
    plt.axhline(y=0, color='k', alpha=1.0) 
                        
    #Output                
    plt.savefig(plot_title, format="pdf")
    print "Plot : %s saved." % (plot_title)
    
    plt.show()
        
def q2_classif_svm_soft():
    training = np.array([5, 10, 7, 10, 1, 8, 3, 8, 5, 8, 7, 8, 1, 6, 3, 6, 5, 6, 7, 6, 1, 4, 3, 4, 5, 4, 7, 4, 1, 2, 3, 2]).reshape([16, 2])
    y = np.array([1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1])
    e = np.zeros(len(y))
    
    w = np.array([-1, 1])
    b = -2
    g = lambda x : np.dot(w, x) + b
    
    for i in range(len(training)):
        x = training[i,:]
        if y[i] == 1 and g(x) < 1:
            e[i] = np.abs(y[i] - g(x))
        elif y[i] == -1 and g(x) > -1:
            e[i] = np.abs(y[i] - g(x))
            
        print "the slack of (%d, %d) is %d" % (x[0], x[1], e[i])
    
def q3_classif_dec_tree():
    points = np.array([(28, 145, "y", 0, 0.0), (65, 140, "y", 0, 0.0), (50, 130, "y", 0, 0.0), (25, 125, "g", 0, 0.0),\
                       (55, 118, "y", 0, 0.0), (38, 115, "y", 0, 0.0), (44, 105, "g", 0, 0.0), (29, 97, "g", 0, 0.0),\
                       (50, 90, "y", 0, 0.0), (63, 88, "y", 0, 0.0), (43, 83, "y", 0, 0.0), (35, 63, "g", 0, 0.0),\
                       (55, 63, "g", 0, 0.0), (50, 60, "y", 0, 0.0), (42, 57, "g", 0, 0.0), (23, 40, "g", 0, 0.0),\
                       (64, 37, "g", 0, 0.0), (50, 30, "y", 0, 0.0), (33, 22, "g", 0, 0.0), (55, 20, "g", 0, 0.0)], 
                       dtype=[('age', 'i8'), ('salary', 'i8'), ('color', '|S1'), ('class', 'i4'), ('slack', 'f8.1')])

    for i in range(0, len(points)):
        if points['color'][i] == 'y':
            points['class'][i] = 1
        else:
            points['class'][i] = -1
        
        c = dec_tree_classifier(points['age'][i], points['salary'][i])
        miss = "*" if c != points['class'][i] else ""
        print "(%d, %d)  %s  %d  %d    %s" % (points['age'][i], points['salary'][i], points['color'][i], points['class'][i], c, miss)
    
    
    
def dec_tree_classifier(A, S):
    result = 0
    
    if A < 45:
        if S < 110:
            result = -1
        else:
            result = 1
    else:
        if S < 75:
            result = -1
        else:
            result = 1
    
    return result




def main():
    q1_classif_svm_hard()
    q2_classif_svm_soft()
    q3_classif_dec_tree()

if __name__ == '__main__':
    main()