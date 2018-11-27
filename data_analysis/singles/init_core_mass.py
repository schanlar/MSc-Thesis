'''
@author: Savvas Chanlaridis
@date: 22/11/2018
@description:
    The script plots the metal core formed during the evolution of
    helium stars as a fuction of their initial mass. The regions where the metal core is
    massive enough to justify an iron core collapse, electron capture supernova, or simply
    end up as a white dwarf are also illustrated.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pc

# Data

initial_masses = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
                  3.0, 3.1, 3.2, 3.3, 3.4, 3.5,
                  4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

c_core_masses = [0.67, 0.71, 0.76, 0.81, 0.86, 0.91, 0.96, 1.01, 1.07, 1.13,
                 1.18, 1.24, 1.29, 1.35, 1.41, 1.47,
                 1.79, 2.47, 2.99, 3.51, 4.04, 4.57] # Carbon core mass right after He-depletion
                                                     # in the core

final_metal_core_masses = [1.206, 1.205, 1.38, 1.395, 1.22, 1.384, 1.397, 1.38, 1.381, 1.383,
                           1.425, 1.47, 1.51, 1.56, 1.604, 1.64,
                           1.9, 2.47, 3.17, 3.69, 4.27, 4.83]   # Final metal core mass at the end
                                                                # of calculations

# --------------------------------------------------------------------------------------------------

# Basic plot

plt.figure(figsize = (13, 9))

# Plot limits and labels

plt.xlabel(r'Initial Mass, M$_i$ [M$_{\odot}$]', fontsize = 13)
plt.ylabel(r'Core Mass, M$_c$ [M$_{\odot}$]', fontsize = 13)

plt.xlim([1.8, 9.1])
plt.ylim([0.5, 5.5])
# --------------------------------------------------------------------------------------------------

#plt.grid(b= True, axis = 'both', color = 'grey', linestyle = '--', linewidth = 0.7)
plt.plot(initial_masses, c_core_masses, "+", markersize = 10, color = 'magenta',
        label = "Core mass after He-depletion")

plt.plot(initial_masses, final_metal_core_masses, "*", markersize = 10, color = 'g',
        markerfacecolor='None', label = "Final core mass")

legend = plt.legend(loc = 'upper left', shadow = True, prop={'size': 12})
# --------------------------------------------------------------------------------------------------

# Fill areas of interest

x_fill_ccsn = [2.1, 4.06, 9.2, 9.2]
y_fill_ccsn = [1.43, 1.43, 4.4, 5.4]
plt.fill(x_fill_ccsn, y_fill_ccsn, "b", alpha = 0.15) # The range of core mass for Fe-CCSN

x_fill_ecsn = [2.0, 3.97, 4.06, 2.1]
y_fill_ecsn = [1.37, 1.37, 1.43, 1.43]
plt.fill(x_fill_ecsn, y_fill_ecsn, "r", alpha = 0.15) # The range of core mass for ECSN

x_fill_wd = [0.8, 2.13, 3.97, 2.0]
y_fill_wd = [0.7, 0.3, 1.37, 1.37]
plt.fill(x_fill_wd, y_fill_wd, "y", alpha = 0.15) # The range of core mass for WDs
# --------------------------------------------------------------------------------------------------

# Fitting

fit = np.polyfit(initial_masses, c_core_masses, 1) # Fits a linear function of the form: a*x+b
fit_fn = np.poly1d(fit)  # fit_fn is now a function which takes in x and returns an estimate for y

plt.plot(initial_masses, fit_fn(initial_masses), '--', color = "tab:blue")
print(fit)
# --------------------------------------------------------------------------------------------------

# Fitting legend

props = dict(boxstyle = 'round', facecolor = 'white', alpha = 0.9)
textstr = '\n'.join(('Linear regression:',
                     r'$M_c \simeq 0.57 \cdot M_i - 0.51$'))

plt.text(1.9, 4.6, textstr, fontsize = 13, bbox = props)
# --------------------------------------------------------------------------------------------------

# Add second legend

leg_CCSN = pc.Patch(facecolor = 'b', alpha = 0.15, label = "Fe-CCSN")
leg_ECSN = pc.Patch(facecolor = 'r', alpha = 0.15, label = "ECSN")
leg_WD = pc.Patch(facecolor = 'y', alpha = 0.15, label = "WDs")

plt.legend(handles = [leg_CCSN, leg_ECSN, leg_WD], loc = 'center', prop={'size': 12},
        bbox_to_anchor = (0.5, 1.05), ncol = 3, shadow = True)

plt.gca().add_artist(legend)
# --------------------------------------------------------------------------------------------------

plt.show()

# Save figure

#plt.savefig('init_core_mass.png', bbox_inches = 'tight', dpi = 300)
