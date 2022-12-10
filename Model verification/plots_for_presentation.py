# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 18:12:34 2022

@author: vcant
"""

import model_proposal
import solvers
import numpy as np
import matplotlib.pyplot as plt

### Example 01: One well: River capture length, percentage of discharge
#-------------------------------------------

ks = np.arange(0.5, 5.5, 0.5)

tts = []

for ka in ks:
    
    aem_model = model_proposal.Model(k = ka, H = 20, h0 = 18)


    well = model_proposal.Well(aem_model, Q = 150, rw = 0.2, x = 30, y = 50)

    solv = solvers.river_length(aem_model)

    print("River Capture Length, Capture position and contribution to discharge is:")
    print(solv.solve_river_length())

    length, riv_coords, capture_fraction = solv.solve_river_length()
    tt = solv.time_travel(0.2)
    tts.append(np.array(tt).min())
    

tts = np.array(tts)
#%%
fig, ax = plt.subplots()

ax.plot(ks,tts, color = "#0592D0")
#ax.set_title("Traveltime performance with hydraulic conductivity")
ax.set_ylabel("Travel time [days]")
ax.set_xlabel("Hydraulic Conductivity [m/d]")
plt.grid(alpha = 0.2)
plt.savefig("traveltime_k.png")

#%%
ks = np.arange(0.5, 5.5, 0.5)

tts = []

for ka in ks:
    
    aem_model = model_proposal.Model(k = ka, H = 20, h0 = 18)


    well = model_proposal.Well(aem_model, Q = 150, rw = 0.2, x = 30, y = 50)

    solv = solvers.river_length(aem_model)

    print("River Capture Length, Capture position and contribution to discharge is:")
    print(solv.solve_river_length())

    length, riv_coords, capture_fraction = solv.solve_river_length()