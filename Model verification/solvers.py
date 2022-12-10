# -*- coding: utf-8 -*-
"""
Script with the solvers implemented in the RBF model.
This initial implementation is based on automatic root finding from the sympy package.

Current implementations:
    
    - River intercepted length:
        This is the length of the river intercepted by the rbf well
    - Stream flow contribution:
        This is the percentage of the pumping discharge that comes from river water.
    - Travel time:
        Calculate the travel time of particles that infiltrate from the river to the well.
        
Limitations:
    - Streams must be located in the y-axis
    - Only one well allowed, located in the positive x,y quadrant

@author: vcant
"""
import numpy as np
import sympy
import itertools
from scipy.optimize import fsolve

#For the time of travel calculation using ttcrpy package:


class river_length():
    """
    Class to solve the river_length and base flow calculations in the RBF model.
    
    Current implementations:
        
        - River intercepted length:
            This is the length of the river intercepted by the rbf well
        - Stream flow contribution:
            This is the percentage of the pumping discharge that comes from river water.
        
    Limitations:
        - Streams must be located in the y-axis
        - Only one well allowed, located in the positive x,y quadrant
        
    Inputs:
        Model: The RBF model class, already set up with the aquifer characteristics and the well placement.
    
    """
    def __init__(self, model):
        self.model = model
    
    def solve_river_length(self):
        """
        Method to calculate intercepted river length and river-flow contribution to well discharge.
        
        Currently checks whether the model well element inputs are correct.
        Inputs
        -------
        None

        Returns
        -------
        length: river length intercepted by the well
        sol_el: location of the river legnth (y-coordinates of the intercepted river length)
        contrib: contribution of river-water to discharge: the percentage of the pumping-rate that comes from river water (the rest is aquifer water)

        """
        if (len(self.model.aem_elements) > 1) | (len(self.model.aem_elements) == 0):
            return "Failed to derive solution. Check current implementation limitiations or model mistakes./nHave you added exactly one well to your model?"
        else:
            
            y = sympy.symbols('y')
            elem = self.model.aem_elements[0]
            Q = elem.Q
            xw = elem.x
            yw = elem.y
            d = np.abs(self.model.river_a *xw + self.model.river_b*yw + self.model.river_c)/np.sqrt(self.model.river_a**2+ self.model.river_b**2)
            Qx = -self.model.Qo_x
            p = self.model.p
      
            ## Checking if stagnation points exists for the solution:
            ex_st_points = Q/(np.pi*d*Qx)
            
            if ex_st_points <= 1:
                return print("There are no stagnation points, check model inputs")
            else:
                equation = sympy.Eq(-(d+p)**2 + (d+p)*Q/(np.pi*Qx)-y**2,0) # Equation assumes the well is at y = 0, it is corrected later below.
                sols = sympy.solveset(equation, y, domain = sympy.S.Reals)
                sol_el = []
                for i in sols: #Transforming solution that is in a set to a list
                    sol_el.append(np.float64(i+yw)) # Correcting the solution to the well y position
                length = np.abs(sol_el[0]-sol_el[1]) # River capture  length
                Q_river = self.model.calc_psi(0,sol_el[0]) - self.model.calc_psi(0,sol_el[1])+ Q
                contrib = Q_river/Q
            
                return length,sol_el, contrib
    
    def time_travel(self, ne, delta_s = 0.1, calculate_trajectory = False, min_dist_est = 0.1):
        """
        Method to derive the time of travel of selected paths from the river to the well.
        The algorithm is a numerical integration of the travel paths of 20 sampled particles
        located at the river intersection.
        It calculate the travel time of each particle, the flux average travel time and the 
        minimum travel time.
        
        Optionally it calculates the particle trajectories, although that is not an efficient algorithm
        
        Requires:
        Successful run of the solve river length method

        Returns
        -------
        tt: time of travel array : numpy array, dimensions: (length of river capture length,1)
        ys: y position array: numpy array with the river y position of the start of the particle
        avgtt (float): flux averaged time of travel calculated as: sum(t_x*qx)/sum(qx)
        mintt (float): minimum time of travel (min(tt))
        traj_array (list[particle index] of numpy array [2xn]: x[0] and y[1] position of particle in time): trajectory of each particle used for plotting.

        """
        
        length, sol_el, contrib = self.solve_river_length()
        
        ys = np.linspace(sol_el[0]+min_dist_est,sol_el[1]-min_dist_est,20)
        #print(ys.shape)
        xs = np.repeat(0.1,ys.shape[0])
        tt = []
        if calculate_trajectory:
            traj_array = []
        
        '''
        initial parameters from the model:
            
        '''
        elem = self.model.aem_elements[0]
        Q = elem.Q
        xw = elem.x
        yw = elem.y
        d = np.abs(self.model.river_a *xw + self.model.river_b*yw + self.model.river_c)/np.sqrt(self.model.river_a**2+ self.model.river_b**2)
        Qx = self.model.Qo_x
        rw = elem.rw
        p = self.model.p
        
        '''
        general qx, qy formulas (general potential)
        '''
        def qx(x,y, Q, Qx, xw, yw, d, p):
            head = self.model.calc_head(x,y)
            
            #Checking if confined or unconfined: (improv. possible)
            if head > self.model.H:
                z = self.model.H
            else:
                z = head
            
            #Specific discharge calculation
            return -1*(-Qx + Q/(4*np.pi)*((2*(x-xw)/((x-xw)**2+(y-yw)**2))-(2*(x-(xw-2*d-2*p)))/((x-(xw-2*d-2*p))**2+(y-yw)**2)))/z
        
        def qy(x,y, Q, Qx, xw, yw, d, p):
            head = self.model.calc_head(x,y)
            
            #Checking if confined or unconfined:
            if head > self.model.H:
                z = self.model.H
            else:
                z = head
            
            #Specific discharge calculation
            return -1*(Q/(4*np.pi)*((2*(y-yw)/((x-xw)**2+(y-yw)**2))-(2*(y-yw))/((x-(xw-2*d-2*p))**2+(y-yw)**2)))/z
        
        '''
        Formulas for correction of the trajectory (stream function)
        (This has to be improved to a more general case...)
        '''
        def equation_x(x_a, psi, y_2, Q, Qx, xw, yw, d, p):
                    return -Qx*y_2 + (Q/(2*np.pi))*(np.arctan2((y_2-yw),(x_a-xw))- np.arctan2((y_2-yw),(x_a-(xw-2*d-2*p))))-psi
        
        def equation_y(y_a, psi, x_2, Q, Qx, xw, yw, d, p) :
                    return -Qx*y_a + (Q/(2*np.pi))*(np.arctan2((y_a-yw),(x_2-xw))- np.arctan2((y_a-yw),(x_2-(xw-2*d-2*p))))-psi
        ''' 
        calculation of streamline and time of travel
        '''
        for x,y in zip(xs,ys):
            
            # Starting the trajectory arrays if necessary:
            if calculate_trajectory:
                xss = []
                xss.append(x)
                yss = []
                yss.append(y)
            
            #dis_arr = [] #error checking
            #v_arr = [] #error checking
            t_arr = []
            x1 = x
            y1 = y
            psi = self.model.calc_psi(x,y)
            breakin_dists = []
            while np.sqrt((x1-xw)**2+(y1-yw)**2) > 5*rw :
                #Part 1 calculating velocity:
                dista1 = np.sqrt((x1-xw)**2+(y1-yw)**2)
                #print(x1)
                #print(y1)
                qx1 = qx(x1,y1, Q, Qx, xw, yw, d, p)
                qy1 = qy(x1,y1, Q, Qx, xw, yw, d, p)
                vx = qx1/ne
                vy = qy1/ne
                v_i = np.sqrt(vx**2+vy**2)
                
                
                #Part 2: estimating second point
                
                
                y_2 = np.float(y1 + delta_s*vy/v_i)
                x_2 = np.float(x1 + delta_s*vx/v_i)
                
                if np.sqrt((x_2-xw)**2+(y_2-yw)**2) < rw:
                    break
                
                ## correcting the point location based on the psi value:
                
                if vx > vy :
                    sols_y = fsolve(equation_y, y_2, (psi, x_2, Q, Qx, xw, yw, d, p), xtol = 1e-4)
                    sol_el_y = sols_y[0]
                    y_2 = sol_el_y
                else:
                    sols = fsolve(equation_x, x_2, (psi, y_2, Q, Qx, xw, yw, d, p), xtol = 1e-4)
                    sol_el_x = sols[0]
                    x_2 = sol_el_x
                
                ## Calculating distance:
                dist = np.sqrt((x_2-x1)**2+(y_2-y1)**2)
                
                # Calculating velocities for the second point:
                
                qx2 = qx(x_2,y_2, Q, Qx, xw, yw, d, p)
                qy2 = qy(x_2,y_2, Q, Qx, xw, yw, d, p)
                vx2 = qx2/ne
                vy2 = qy2/ne
                
                # Calculating mean velocity: 
                
                vxm = np.mean([vx,vx2])
                vym = np.mean([vy,vy2])
                
                vm = np.sqrt(vxm**2+vym**2)
                
                #Calculating time of travel of the particle (deltaS/deltaV) and appending to array:
                t_arr.append(dist/vm)
                #dis_arr.append(dist) #error checking
                #v_arr.append(vm)
                
                #Looping
                x1 = x_2
                y1 = y_2
                
                if calculate_trajectory:
                    xss.append(x1)
                    yss.append(y1)

            
            #Adding time of travel estimate
            #dis_arr = np.array(dis_arr)
            #v_arr = np.array(v_arr)
            tt.append(np.sum(np.array(t_arr)))
            
            # Saving the particle trajectory in a numpy array:
            if calculate_trajectory:
                traj_arr = np.vstack((np.array(xss),np.array(yss)))
                traj_array.append(traj_arr)
            
        
        #Return the average travel time:
        
        ## Calculate qxs (specific discharges):
        qs = []
        for x,y in zip(xs,ys):
            qx1 = qx(x,y, Q, Qx, xw, yw, d, p)
            qy1 = qy(x,y, Q, Qx, xw, yw, d, p)
            q = np.sqrt(qx1**2+qy1**2)
            qs.append(q)
        
        qs = np.array(qs)
        tt = np.array(tt)
        ## Calulcate average traveltime:
        avgtt = np.sum(qs*tt)/np.sum(qs)
        
        ## Calculate the minimum travel time:
        mintt = np.min(tt)
        
        # If necessary exporto the trajectory also:
        
        if calculate_trajectory:
            
            return tt, ys, avgtt, mintt, traj_array
        
        else:
            
            return tt, ys, avgtt, mintt
        

            
            
            
            
            
            
            
            
        
        



