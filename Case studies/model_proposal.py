# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 10:18:14 2021

@authors: vcantarella, marigomez, alevilla
"""

import numpy as np
import pandas as pd

class River:
    """
    Optional class to input the river coordinates.
    If given, will output the rotation matrix for the coordinates with the rot_matrix method
    Inputs: x,y coordinates for two river nodes (x1,y1) and (x2,y2)
    """
    def __init__(self,x1,y1,x2,y2):
        self.m = (y2-y1)/(x2-x1)
        self.theta = np.where(np.arctan(self.m)> 0, np.pi - np.arctan(self.m),
                              -np.pi - np.arctan(self.m))
    def rot_matrix(self):
        """
        returns the rotation matrix (2d numpy array) that guarantee the river is parallel to y axis
        
        """
        t = self.theta
        return(np.array([np.cos(t), -np.sin(t)],
                        [np.sin(t), np.cos(t)]))
    
    def operator(self,x,y):
        """
        returns the rotated and translated coordinates for the river system:
        input (x, y)
        outputs: translated (x', y')
        """
        return None


class Model:
    """
    Basic AEM-RBF model Object. Inputs are the aquifer parameters and the river object
    This object contains the methods to calculate discharge potential, heads and 
    stream function from the aem objects.
    
    Currently only supports models with default river location (y-axis)
    
    Parameters
    --------------------
    k : hydraulic conductivity
    H : aquifer Height
    h0 : aquifer head at the reference location (measured from the base of the aquifer)
    river: river object (not implemented yet)
    x_ref : x-coordinate of the reference location
    y_ref : y-coordinate of the reference location
    
    """
    def __init__(self, k, H, h0, river = None, x_ref = 0, y_ref = 0):
        self.k = k
        self.H = H
        self.h0 = h0
        self.aem_elements = []
        self.well_df = pd.DataFrame({'wellid' : [],
                                     'Discharge': [],
                                     'X': [],
                                     'Y': []})
        self.Qo_x = -1  #Baseflow in the x direction
        self.p = 0 #River clogging factor
        self.x = x_ref
        self.y = y_ref
        if river is None:
            # If undeclared river line equation will be assumed to be located at the y-axis
            self.river_a = 1
            self.river_b = 0
            self.river_c = 0
        else: # river line imported from river class
            self.river_a = river.river_a
            self.river_b = river.river_b
            self.river_c = river.river_c
        if self.h0 < self.H:
            self.phi_c = 0.5 * self.k * self.h0 **2
        else:
            self.phi_c = self.k * self.H * self.h0 - 0.5 * self.k * self.H **2
        self.phi0 = self.phi_c
    
    def calc_phi(self, x, y):
        """
        Method to calculate the discharge potential at given location:
        
        Currently only supports models with default river location (y-axis)

        Parameters
        ----------
        x,y location of interest.

        Returns
        -------
        phi(x,y) float.

        """
        
        phi_well = 0
        p = self.p
        for element in self.aem_elements:
            d = np.abs(self.river_a *element.x + self.river_b*element.y + self.river_c)/np.sqrt(self.river_a**2+ self.river_b**2)
            if (np.abs(x - element.x) <= element.rw):
                phi_q = (element.Q/(4*np.pi))*np.log(((x+element.rw -element.x)**2 + (y-element.y)**2)/((x+element.rw-(element.x-2*d- 2*p))**2+(y-element.y)**2))
            elif (np.abs(y - element.y) <= element.rw):
                phi_q = (element.Q/(4*np.pi))*np.log(((x - element.x)**2 + (y+element.rw-element.y)**2)/((x-(element.x - 2*d- 2*p))**2+(y+element.rw-element.y)**2))
            else:
                phi_q = (element.Q/(4*np.pi))*np.log(((x - element.x)**2 + (y-element.y)**2)/((x-(element.x - 2*d - 2*p))**2+(y-element.y)**2))
            phi_well += phi_q
        phi_base = -self.Qo_x*x
        return self.phi0 + phi_well + phi_base
    
    def calc_head(self,x,y):
        """
        Method to calculate the head at a given location:
        
        Currently only supports models with default river location (y-axis)

        Parameters
        ----------
        x,y location of interest.

        Returns
        -------
        head at (x,y): float.

        """
        phi = self.calc_phi(x,y) # Discharge potential
        phicrit = 0.5 * self.k * self.H **2 #Method according to Haijtema, 1995
        if phi >= phicrit: # Confined conditions
            h = (phi + 0.5*self.k*self.H**2)/(self.k*self.H)
        else: # Unconfined conditions
            h = np.sqrt((2 / self.k) * (phi)) 
        return h# head
    
    def calc_psi(self, x,y):
        """
        Method to calculate the stream function for the RBF-AEM model at 
        a given location (x,y)
        
        Currently only supports models with default river location (y-axis)

        Parameters
        ----------
        x,y: coordinates of location of interest.

        Returns
        -------
        Stream function (psi) at (x,y): float.

        """
        psi_well = 0
        p = self.p
        for element in self.aem_elements:
            d = np.abs(self.river_a *element.x + self.river_b*element.y + self.river_c)/np.sqrt(self.river_a**2+ self.river_b**2)
            if (x == element.x) & (y == element.y):
                psi_q = (element.Q/(2*np.pi))*(np.arctan2((y-element.y),(x-(element.x+element.rw)))- np.arctan2((y-element.y),(x-(element.x-2*d- 2*p))))
            else:
                psi_q = (element.Q/(2*np.pi))*(np.arctan2((y-element.y),(x-element.x))- np.arctan2((y-element.y),(x-(element.x-2*d- 2*p))))
            psi_well += psi_q
        psi_base = -self.Qo_x*y
        psi = psi_well+psi_base
        
        
        return psi
    
    def calc_clogging(self, Kd,d):
        """
        Method to add the clogging effect to the AEM model

        Parameters
        ----------
        Kd: a float, with the hydraulic conductivity of the clogging layer [L/T].
        d: a float, thickness of the clogging layer [L]

        Returns
        -------
        internal value of p
        """
        self.p = d*self.k/Kd
        self.x = 0-self.p
        self.update_phi0()
        
    def update_phi0(self):
        """
        Method to calculate the discharge potential at the phi0 location
        - Used to debug and to calculate the discharge potential at any location
        
        Parameters
        ----------
        None

        Returns (internal)
        -------
        phi0, float. The reference discharge potential used in the general phi formula.

        """
        
        self.phi0 = 0
        
        phi = self.calc_phi(self.x,self.y)

        self.phi0 = self.phi_c - phi

class Well:
    """
    Element to create Well for the AEM-RBF model
    Inputs to the well object:
    --------------------------
        model : a AEM-RBF model
        Q: discharge rate
        rw: radius of the well
        x: x-location of the well
        y: y-location of the well
    """
    def __init__(self, model,Q, rw, x,y):
        self.x = x
        self.y = y
        self.Q = Q
        self.rw = rw
        model.aem_elements.append(self)
        model.update_phi0()




