import numpy as np
import pandas as pd

class River: #Optional class to input river coordinates
    def __init__(self, x1, y1, x2, y2):
        self.m = (y2-y1)/(x2-x1)
        self.theta = np.where(np.arctan(self.m)> 0, np.pi - np.arctan(self.m), -np.pi - np.arctan(self.m))
    
    def rot_matrix(self):
        t = self.theta
        return(np.array([np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]))

    def operator(self,x,y):
        return None

class Model: #Model class to calculate discharge potential, head and stream function
    def __init__(self, k, H, h0, Qo_x, river = None, x_ref = 0, y_ref = 0):
        self.k = k
        self.H = H
        self.h0 = h0
        self.aem_elements = []
        self.well_df = pd.DataFrame({'wellid' : [], 'Discharge' : [], 'X' : [], 'Y' : []})
        self.Qo_x = -Qo_x #Baseflow in the x-direction
        self.p = 0 #River clogging factor
        self.x = x_ref
        self.y = y_ref

        if river is None: #if not defined in river class then river is assumed at Y-axis
            self.river_a = 1
            self.river_b = 0
            self.river_c = 0
        
        else: #River line imported from river class
            self.river_a = river.river_a
            self.river_b = river.river_b
            self.river_c = river.river_c
        if self.h0 < self.H:
            self.phi_c = 0.5 * self.k * self.h0**2
        else:
            self.phi_c = self.k * self.H * self.h0 - 0.5 * self.k * self.H**2
        self.phi0 = self.phi_c

    def calc_phi(self, x, y): #Function to calculate the discharge potential
        phi_well = 0
        p = self.p
        for element in self.aem_elements:
            d = np.abs(self.river_a * element.x + self.river_b * element.y + self.river_c) / np.sqrt(self.river_a**2 + self.river_b**2)
            if (np.abs(x == element.x) <= element.rw):
                phi_q = (element.Q/(4*np.pi)) * np.log(((x+element.rw - element.x)**2 + (y-element.y)**2)/((x+element.rw-(element.x-2*d-2*p))**2+(y-element.y)**2))
            elif (np.abs(y == element.y) <= element.rw):
                phi_q = (element.Q/(4*np.pi)) * np.log(((x-element.x)**2 + (y+element.rw-element.y)**2)/((x-(element.x - 2*d-2*p))**2+(y+element.rw-element.y)**2))
            else:
                phi_q = (element.Q/(4*np.pi))*np.log(((x-element.x)**2 + (y-element.y)**2)/((x-(element.x - 2*d-2*p))**2+(y-element.y)**2))
             
            phi_well += phi_q
        phi_base = -self.Qo_x*x
        return self.phi0 + phi_well + phi_base

    def calc_head(self, x, y): #Function to calculate head
        phi = self.calc_phi(x,y)
        phicrit = 0.5 * self.k * self.H ** 2
        if phi >= phicrit:
            h = (phi + 0.5*self.k*self.H**2)/(self.k*self.H)
        else:
            h = np.sqrt((2 / self.k) * (phi))
        return h

    def calc_psi(self, x, y): #Function to calculate stream function
        psi_well = 0
        p = self.p
        for element in self.aem_elements:
            d = np.abs(self.river_a*element.x + self.river_b*element.y + self.river_c)/np.sqrt(self.river_a**2 + self.river_b**2)
            if (x == element.x) & (y == element.y):
                psi_q = (element.Q/(2*np.pi))*(np.arctan2((y-element.y), (x-(element.x+element.rw))) - np.arctan2((y-element.y), (x-(element.x-2*d-2*p))))
            else:
                psi_q = (element.Q/(2*np.pi)) * (np.arctan2((y-element.y), (x-element.x)) - np.arctan2((y-element.y), (x-(element.x-2*d-2*p))))
            psi_well += psi_q
        psi_base = -self.Qo_x*y
        psi = psi_well+psi_base

        return psi

    def calc_clogging(self, kd, d): #Calculation of clogging factor
        self.p = d*self.k/kd
        self.x = 0-self.p
        self.update_phi0()

    def update_phi0(self): #Method to calculate the discharge potential at the phi0 location
        self.phi0 = 0
        phi = self.calc_phi(self.x, self.y)
        self.phi0 = self.phi_c - phi

class Well: #Well creation class
    def __init__(self, model, Q, rw, x, y):
        self.x = x
        self.y = y
        self.Q = Q
        self.rw = rw
        model.aem_elements.append(self)
        model.update_phi0()


