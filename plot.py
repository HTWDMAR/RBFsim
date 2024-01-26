import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import StrMethodFormatter


class plotting: #Class to assist plotting of the results
    def __init__(self, xmin, xmax, ymin, ymax, steps, riv_coords = None):
        self.xmin=xmin
        self.ymin=ymin
        self.xmax=xmax
        self.ymax=ymax
        self.riv_coords=riv_coords
        self.steps=steps

    def mesh(self): #Method to create plot grid
        xvec = np.linspace(self.xmin, self.xmax, self.steps)
        yvec = np.linspace(self.ymin, self.ymax, self.steps)
        xvec, yvec = np.meshgrid(xvec, yvec)
        return xvec, yvec

    def fix_to_mesh(self, model): #Method to export results to the plot grid
        h1=[]
        psi1=[]
        for x,y in zip(self.mesh()[0].flatten(),self.mesh()[1].flatten()):
            head = model.calc_head(x, y)
            psi_0 = model.calc_psi(x, y)
            h1.append(head)
            psi1.append(psi_0)
        h = np.array(h1).reshape((self.steps, self.steps))
        psi = np.array(psi1).reshape((self.steps, self.steps))
        return h, psi

    #Method to create 2-D plot
    def plot2d(self, model, tt=None, ys = None, traj_array = None, sharey = False, levels = 10, alpha=0.6, quiver = False, streams = False, figsize = (18,12)):
        plt.rcParams.update({'font.size': 25})
        h = self.fix_to_mesh(model)[0]
        psi = self.fix_to_mesh(model)[1]

        #Calculate gradients for quiver
        dy, dx = np.gradient(-h)
        e = 1

        fig, ax = plt.subplots(1,2, figsize = figsize, sharey = sharey, gridspec_kw={'width_ratios': [1, 3.5]})
        contour = plt.contourf(self.mesh()[0], self.mesh()[1], h, levels, cmap = cm.YlGnBu, alpha=alpha)
        ax[1].set_xlabel('Length of Domain (m)', fontsize=25,labelpad=15)
        ax[1].set_ylabel('Width of Domain (m)', fontsize=25,labelpad=15)
        ax[1].tick_params(axis='both', which='major', labelsize=25)
        ax[1].tick_params(axis='both', which='minor', labelsize=25)
        
        plt.rcParams['contour.negative_linestyle'] = 'solid'
        #plt.xlabel('x [m]', fontsize=15)
        #plt.ylabel('y [m]', fontsize=15)
        cbar = fig.colorbar(contour, ax=ax[1]) #, shrink=0.9
        cbar.set_label('Hydraulic Head (m)', fontsize=25, labelpad=-120)  # Add this line
        cbar.ax.tick_params(labelsize=25)

        if not (quiver) and not (streams) and (traj_array==None):
            ax[1].contour(self.mesh()[0], self.mesh()[1], psi, int(levels*2.5), colors=('#848482',), linewidths=(1,))


        elif quiver:
            ax[1].quiver(self.mesh()[0][::e, ::e], self.mesh()[1][::e, ::e], dx[::e, ::e], dy[::e, ::e], linewidths=0.1, alpha=0.5, width=0.001)

        if streams:
            ax[1].streamplot(self.mesh()[0][::e, ::e], self.mesh()[1][::e, ::e], dx[::e, ::e], dy[::e, ::e], color='#000000', linewidth=1.6, density=1.0, arrowsize=1.2, zorder=0)

        if traj_array is not None: #Plotting streamlines of the river particles captured by the well
            for trajectory in traj_array:
                ax[1].plot(trajectory[0,:], trajectory[1, :], linestyle='--', linewidth=2.8, color = "maroon", label="particle trajectory")
    
        ax[1].plot([0,0], [np.min(self.mesh()[1]), np.max(self.mesh()[1])], color='#4169e1', linestyle='-', linewidth=20) #River capture line

        if self.riv_coords is not None:
            ax[1].plot([0,0], [self.riv_coords[0], self.riv_coords[1]], color='r', linestyle='-', linewidth=8) #River line

        if tt is not None: #Travel time plot
            ax[0].plot(tt, ys, '--o', color='#0592D0', markersize=5)
            ax[0].set_xlabel('Travel time - (d)', fontsize=25)
            ax[0].set_ylabel('Domain Width (m)', fontsize=25)
            ax[0].grid(alpha=0.2)

        else:
            fig.delaxes(ax[0])
        ax[1].set_ylim(0, 500)   # Modify here to show entire system # PKY changed from None to 150 20.12.23
        ax[0].set_ylim(0, 500)  ## Modify here to show entrie system # PKY changed from None to 150
        return ax, fig

    def plot3d(self, model): #3D Plotting of the results
        fig, ax = plt.subplots(figsize=(15, 20), subplot_kw={'projection': "3d"})
        surf = ax.plot_surface(self.mesh()[0], self.mesh()[1], self.fix_to_mesh(model)[0], cmap=cm.coolwarm_r, linewidth=0, antialiased=True)
        ax.zaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))  # Corrected format specifier
        ax.set_xlabel('Length of Domain (m)', fontsize=25, labelpad=25)  # Increase font size and labelpad
        ax.set_ylabel('Width of Domain (m)', fontsize=25, labelpad=28)  # Increase font size and labelpad
        ax.set_zlabel('Hydraulic Head (m)', fontsize=25, labelpad=5)  # Increase font size and labelpad
        colorbar = fig.colorbar(surf, shrink=0.5, ax=ax, location="right")
        colorbar.ax.tick_params(labelsize=25)  # Set the font size for colorbar labels

        ax.set_zticks([])  # Hide the z-axis ticks

        ax.set_ylim(0, None)  # Modify here to show entire vicinity

        ax.tick_params(axis='x', labelsize=25)
        ax.tick_params(axis='y', labelsize=25)

        return ax, fig

