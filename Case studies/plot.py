# -*- coding: utf-8 -*-
"""
@authors: mgome, vcantarella

Class and methods for plotting AEM model results:

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter


class plotting:
    """
    Class to assist in plotting of the AEM model
    Input:
    xmin,xmax
    river coordinates = [riv y-min, riv y-max],
    steps
    """
    def __init__(self,xmin, xmax, ymin, ymax, steps, riv_coords = None):
        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.steps=steps
        self.riv_coords=riv_coords
        
    def mesh(self):
        
        # Method to create the plot grid:
        
        xvec=np.linspace(self.xmin, self.xmax, self.steps)
        yvec = np.linspace(self.ymin, self.ymax, self.steps)
        xvec, yvec = np.meshgrid(xvec,yvec)
        return xvec, yvec
    
    def fix_to_mesh(self,model):
        
        # Method to export results to the plot grid:
        
        hl=[]
        psil=[]
        for x,y in zip(self.mesh()[0].flatten(),self.mesh()[1].flatten()):
            head = model.calc_head(x, y)
            psi_0 = model.calc_psi(x, y)
            hl.append(head)
            psil.append(psi_0)
        h= np.array(hl).reshape((self.steps,self.steps))
        psi=np.array(psil).reshape((self.steps,self.steps))
        return h , psi
    
    def plot2d(self,model,tt=None, ys = None, traj_array = None, levels=10, alpha=0.6, quiver=False, streams=False, figsize = (18,12)):
        """
        Method to plot results in 2D. Support the plotting of time of travel (Inputs to the time of travel
        results in tt and ys) and contouring of heads and stream functions:
        Input:
        Model: AEM model
        tt (np.array): Time of travel result from the time_travel method in solvers.py.
        ys: Location of particles in Time of Travel (result ys form the time_travel method in solvers.py)
        levels (int): number of head levels to contour.
        quiver (boolean): If true plot the stream function with flow vectors. Default is false.
        streams (boolean): If True, Plot the stream location
        figsize (tuple, 2d): 2d dimensions of the image.
        """
        
        h=self.fix_to_mesh(model)[0]
        psi=self.fix_to_mesh(model)[1]
        
        # Calculating gradients for quiver: 
        dy, dx = np.gradient(-h)
        e=1
        
        fig, ax = plt.subplots(1,2,figsize = figsize , sharey = True, gridspec_kw={'width_ratios': [1, 3.5]})
        contour = plt.contourf(self.mesh()[0], self.mesh()[1], h,
            levels,
            cmap = cm.Blues,alpha=alpha)
        ax[1].set_xlabel('x [m]')
        ax[1].set_ylabel('y [m]')
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        fig.colorbar(contour, ax=ax[1], shrink=0.9)
        
        if not (quiver) and not(streams) and (traj_array==None):
            ax[1].contour(self.mesh()[0], self.mesh()[1],psi,
                                      int(levels*2.5),
                                      colors=('#848482',),
                                      linewidths=(1,))
        elif quiver:
            
            ax[1].quiver(self.mesh()[0][::e,::e], self.mesh()[1][::e,::e], 
                         dx[::e,::e], dy[::e,::e], 
                         linewidths=0.1, alpha=0.5,width=0.001)
        if streams:
            ax[1].streamplot(self.mesh()[0][::e,::e], self.mesh()[1][::e,::e], 
                             dx[::e,::e], dy[::e,::e], color='#4169e1', 
                              linewidth=0.8, density=0.6,arrowsize=1.2,zorder=0)
            
        if traj_array is not None: #Plotting streamlines of river particles captured by well:
            for trajectory in traj_array:
                ax[1].plot(trajectory[0,:],trajectory[1,:],linestyle = '--', 
                           linewidth=2.8, color = "maroon", label = "particle trajectory")
        
        ax[1].plot([0,0],[np.min(self.mesh()[1]),np.max(self.mesh()[1])], 
                   color = '#4169e1', linestyle = '-', linewidth = 20) #river line
        if self.riv_coords is not None:
            ax[1].plot([0, 0], [self.riv_coords[0], self.riv_coords[1]], 
                   color='r', linestyle='-', linewidth=8) #River capture


        if tt is not None:
        #Travel times plot
            #loc=[np.nan]*int((len(self.mesh()[1])-len(tt))/2)
            ax[0].plot(tt,ys,  '--o',color="#0592D0", markersize=3)
            ax[0].set_xlabel('Travel time - Days')
            ax[0].set_ylabel('y [m]')
            #ax[0].set_ylim(0,100)
            ax[0].grid(alpha=0.2)
        else:
            fig.delaxes(ax[0])
        #plt.tight_layout()

        return ax
    
    def plot3d(self, model):
        """
        Experimental 3D plotting method
        """
        fig, ax = plt.subplots(figsize = (15,20),subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(self.mesh()[0], self.mesh()[1], self.fix_to_mesh(model)[0],
                            cmap=cm.coolwarm,
                            linewidth=0,
                            antialiased=True)                        
        plt.gca().zaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('drawdown [m]')
        fig.colorbar(surf, shrink=.8, ax=[ax], location = "left") 
        return ax
    





