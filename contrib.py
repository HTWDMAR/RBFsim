import numpy as np
import streamlit as st
import sympy
from scipy.optimize import fsolve
import itertools


class river_length(): #Class to calculate river capture length, location and capture fraction.
    def __init__(self, model):
        self.model = model
    
    def solve_river_length(self):
        if (len(self.model.aem_elements) > 1) | (len(self.model.aem_elements) == 0):
            st.write("Failed to drive solution")
        else:
            y = sympy.symbols('y')
            elem = self.model.aem_elements[0]
            Q = elem.Q
            xw = elem.x
            yw = elem.y
            d = np.abs(self.model.river_a*xw + self.model.river_b*yw + self.model.river_c) / np.sqrt(self.model.river_a**2 + self.model.river_b**2)
            Qx = -self.model.Qo_x
            p = self.model.p
            #st.write(Q,Qx)
            ex_st_points = Q /(np.pi*d*Qx)

            if ex_st_points <= 1: #Checking existing stagnation points
                #st.write(Q,Qx,d)
                st.write("There is no staganation Point")
            else:
                equation = sympy.Eq(-(d+p)**2 + (d+p)*Q/(np.pi*Qx)-y**2,0) #Equation assumes the well is at y=0, it is corrected later
                sols = sympy.solveset(equation, y, domain = sympy.S.Reals)
                sol_el = []
                for i in sols: #Putting solution in a list
                    sol_el.append(np.float64(i+yw)) #Correcting the solution to the well y position
                length = np.abs(sol_el[0]-sol_el[1]) #River capture length
                Q_river = self.model.calc_psi(0, sol_el[0]) - self.model.calc_psi(0, sol_el[1]) + Q #Bank filtrate portion
                contrib = Q_river/Q #Bank filtrate ratio

                return length, sol_el, contrib #Return 3 solution

    def time_travel(self, ne, delta_s = 0.1, calculate_trajectory=False, min_dist_est=0.1): #Function to calulcate time of travel

        length, sol_el, contrib = self.solve_river_length()

        ys = np.linspace(sol_el[0]+min_dist_est, sol_el[1]-min_dist_est, 20)
        xs = np.repeat(0.1, ys.shape[0])
        tt = []
        
        if calculate_trajectory:
            traj_array = []


        #Intial paramters to model
        elem = self.model.aem_elements[0]
        Q = elem.Q
        xw = elem.x
        yw = elem.y
        d = np.abs(self.model.river_a*xw + self.model.river_b*yw + self.model.river_c)/np.sqrt(self.model.river_a**2 + self.model.river_b**2)
        Qx = self.model.Qo_x
        rw = elem.rw
        p = self.model.p


        #general potential qx, qy formulae 
        def qx(x, y, Q, Qx, xw, yw, d, p):
            head = self.model.calc_head(x,y)
            #Checking if confined or unconfined
            if head > self.model.H:
                z = self.model.H
            else:
                z = head
            #Specific discharge calculation
            return -1*(-Qx + Q/(4*np.pi)*((2*(x-xw)/((x-xw)**2+(y-yw)**2))-(2*(x-(xw-2*d-2*p)))/((x-(xw-2*d-2*p))**2+(y-yw)**2)))/z

        def qy(x, y, Q, Qx, xw, yw, d, p):
            head = self.model.calc_head(x,y)
            #Checking if confined or unconfined
            if head > self.model.H:
                z = self.model.H
            else:
                z = head
            #Specific discharge calculation
            return -1*(Q/(4*np.pi)*((2*(y-yw)/((x-xw)**2+(y-yw)**2))-(2*(y-yw))/((x-(xw-2*d-2*p))**2+(y-yw)**2)))/z
            
        #Formulae for correction of the trajectory (Stream function)

        def equation_x(x_a, psi, y_2, Q, Qx, xw, yw, d, p):
            return -Qx*y_2 + (Q/(2*np.pi))*(np.arctan2((y_2-yw), (x_a-xw)) - np.arctan2((y_2-yw), (x_a-(xw-2*d-2*p))))-psi
        
        def equation_y(y_a, psi, x_2, Q, Qx, xw, yw, d, p):
            return -Qx*y_a + (Q/(2*np.pi))*(np.arctan2((y_a-yw), (x_2-xw)) - np.arctan2((y_a-yw), (x_2-(xw-2*d-2*p))))-psi

        #Calculation of streamline and time of travel

        for x,y in zip(xs, ys):
            
            #Starting the trajectory arrays if necessary
            if calculate_trajectory:
                xss = []
                xss.append(x)
                yss = []
                yss.append(y)

            t_arr = []
            x1 = x
            y1 = y
            psi = self.model.calc_psi(x,y)
            breakin_dists = []

            while np.sqrt((x1-xw)**2+(y1-yw)**2) > 5*rw:
                #1.Calculating velocity
                dista1 = np.sqrt((x1-xw)**2+(y1-yw)**2)
                qx1 = qx(x1, y1, Q, Qx, xw, yw, d, p)
                qy1 = qy(x1, y1, Q, Qx, xw, yw, d, p)
                vx = qx1/ne
                vy = qy1/ne
                v_i = np.sqrt(vx**2+vy**2)

                #2.Estimating second point
                y_2 = np.float64(y1 + delta_s*vy/v_i)
                x_2 = np.float64(x1 + delta_s*vx/v_i)

                if np.sqrt((x_2-xw)**2+(y_2-yw)**2) < rw:
                    break

                #Correcting the point location based on the psi value
                if vx > vy:
                    sols_y = fsolve(equation_y, y_2, (psi, x_2, Q, Qx, xw, yw, d, p), xtol=1e-1)
                    sol_el_y = sols_y[0]
                    y_2 = sol_el_y

                else:
                    sols = fsolve(equation_x, x_2, (psi, y_2, Q, Qx, xw, yw, d, p), xtol=1e-1)
                    sol_el_x = sols[0]
                    x_2 = sol_el_x

                #Calculating distance
                dist = np.sqrt((x_2-x1)**2 + (y_2-y1)**2)

                qx2 = qx(x_2, y_2, Q, Qx, xw, yw, d, p)
                qy2 = qy(x_2, y_2, Q, Qx, xw, yw, d, p)
                vx2 = qx2/ne
                vy2 = qy2/ne

                #Calculating mean velocity
                vxm = np.mean([vx, vx2])
                vym = np.mean([vy, vy2])

                vm = np.sqrt(vxm**2+vym**2)

                #Calculating time of travel of particle and appending the array
                t_arr.append(dist/vm)

                #Looping
                x1 = x_2
                y1 = y_2

                if calculate_trajectory:
                    xss.append(x1)
                    yss.append(y1)

            #Adding time of travel estimate
            tt.append(np.nansum(np.array(t_arr))) #using nansum instead of np.sum to handle Nan values in array

            #Saving the particle trajectory in a numpy array
            if calculate_trajectory:
                traj_arr = np.vstack((np.array(xss), np.array(yss)))
                traj_array.append(traj_arr)

        #Return the average travel time

        #Calculate qxs (Specific Discharge)
        qs = []
        for x,y in zip(xs,ys):
            qx1 = qx(x, y, Q, Qx, xw, yw, d, p)
            qy1 = qy(x, y, Q, Qx, xw, yw, d, p)
            q = np.sqrt(qx1**2+qy1**2)
            qs.append(q)

        qs = np.array(qs)
        tt = np.array(tt)
        qs[qs<0]=0
        tt[tt<0]=0
        ys[ys<0]=0
        for i in range(len(traj_array)):
            traj_array[i][traj_array[i] < 0] = 0

       
        
        #st.write('trajectory array',traj_array)
        #Calculate the average travel time
        avgtt = np.sum(qs*tt)/np.sum(qs)

        #Calculate min travel time
        mintt = np.min(tt)

        if calculate_trajectory:
            return tt, ys, avgtt, mintt, traj_array

        else:

            return tt, ys, avgtt, mintt       



       



