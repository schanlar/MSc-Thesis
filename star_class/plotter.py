'''
@author Savvas Chanlaridis
@version v.13.12.18
@description:
The script reads data from a csv file with a
known header format, stores the data using
the star class which provides a more intuitive way of
displaying a dataset, and plots the evolution of the
metal core as a function of the initial mass of the star.
'''


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pc
from star_class import star
import csv, sys


def read_data(path):
    '''
    The script assumes that the csv file has a specific format for the header info.
    The csv file contains all the data for the masses of single helium stars.
    The displayed messages are stored in a data_log.txt file.
    '''

    data = []
    sys.stdout = open('data_log.txt','wt')


    try:
        with open(path + '.csv') as csvFile:
            reader = csv.reader(csvFile, delimiter = ';')
            for row in reader:
                data.append(row)
    except:
        raise FileNotFoundError('The file was not found within this path. \n' +
                                'The csv extension should NOT be included!')


    header = data.pop([0][0]) # Extract header info
    print('#'*123)
    print(header)
    print('#'*123)

    # The csv file may contain data with different delimiters
    # This loop ensures all floats are expressed with a period
    # as a decimal separator.

    for i in range(0, len(data)):

        # Since we know the format of the header,
        # we're only interested on the first 5 columns
        # of data
        for j in range(0, 6):
            try:
                data[i][j] = float(data[i][j])

            except ValueError:
                print('Bad value:', data[i][j], 'for ', header[j])
                print("Attempting to correct...")

                data[i][j] = float(data[i][j].replace(',', '.', 1))

                print('Replaced with: ', data[i][j])

    sys.stdout.close()
    return header, data


def organize_data(header, data):
    '''
    The function takes two mandatory arguments: header, data.
    The latter is a list of lists in which every element represents
    a set of parameters defined by the header.
    With this function we want to organize our dataset using an
    object-oriented approach. For this reason we utilize the star class.
    '''

    stars = [] # Every element of the list is
               # a star object

    for i in range(0, len(data)):

        stars.append(star(data[i][header.index('mass')], ccore = data[i][header.index('ccore')],
             fcore = data[i][header.index('fcore')], fmass = data[i][header.index('fmass')],
            envelope = data[i][header.index('envelope')], wind = data[i][header.index('wind')],
                     fate = data[i][header.index('fate')], termination = data[i][header.index('termination')]))


    return stars


def plotter(saveFigure = False):

    header, my_data = read_data('singles_table')
    helium_stars = organize_data(header, my_data)

    # Define limits to fill areas of interest

    x_fill_ccsn = [2.1, 5.3, 9.2, 9.2, 3.1, 9.2, 9.2, 3.1]
    y_fill_ccsn = [1.43, 1.43, 3.45, 5.4, -0.1, -0.1, 2.1, 2.1]


    x_fill_ecsn = [2.0, 5.18, 5.3, 2.1, 2.15, 3.1, 3.1, 2.1]
    y_fill_ecsn = [1.37, 1.37, 1.43, 1.43, -0.1, -0.1, 2.1, 2.1]


    x_fill_wd = [0.8, 3.1, 5.18, 2.0, 1.8, 2.15, 2.1, 1.8]
    y_fill_wd = [0.7, 0.3, 1.37, 1.37, -0.1, -0.1, 2.1, 2.1]
    # --------------------------------------------------------------------------------------------------



    # Plotting the data

    fig, (ax1, ax2) = plt.subplots(2, figsize = (15,15), sharex = True)

    # Top panel plot
    # Use list comprehension to access the data.
    # Comparing floats should be done with caution due to rounding and precision issues.


    ax1.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
             [helium_stars[i].getEnvelope() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
             '*', color = 'g', markersize = 10, label = r'He-rich envelope, $\eta = 0.8$')

    ax1.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             [helium_stars[i].getEnvelope() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             '*', color = 'k', markersize = 10, label = r'He-rich envelope, $\eta = 1.0$')

    ax1.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             [helium_stars[i].getEnvelope() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             '*', color = 'magenta', markersize = 10, label = r'He-rich envelope, $\eta = 1.58$')

    ax1.set_ylabel(r'Envelope Mass, M$_{env}$ [M$_{\odot}$]', fontsize = 13)
    ax1.set_ylim([-0.1, 2.1])

    ax1.fill(x_fill_ccsn[4:], y_fill_ccsn[4:], "b", alpha = 0.1) # The range of core mass for Fe-CCSN
    ax1.fill(x_fill_ecsn[4:], y_fill_ecsn[4:], "r", alpha = 0.1) # The range of core mass for ECSN
    ax1.fill(x_fill_wd[4:], y_fill_wd[4:], "y", alpha = 0.1) # The range of core mass for WDs

    fig.legend(loc = 'lower right', bbox_to_anchor=(0.98, 0.52), shadow = True, prop={'size': 12})

    # Annotate potential SNe-Ic region

    ax1.annotate('SNe-Ic', xy = (0.095, 0.08), xytext = (0.095, 0.11), xycoords = 'axes fraction',
            fontsize = 12, ha='center', va='bottom',
            bbox = dict(boxstyle='round', facecolor='white'),
            arrowprops = dict(arrowstyle='-[, widthB = 3.9, lengthB = 0.8', lw = 2.0))

    # --------------------------------------------------------------------------------------------------

    # Bottom panel plot

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
             [helium_stars[i].getCcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
             '+', color = 'g', markersize = 10, label = r"Core mass after He-depletion, $\eta = 0.8$")

    ax2.scatter([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8 and
                helium_stars[i].getMass() < 3.5],
                [helium_stars[i].getFcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8 and
                helium_stars[i].getMass() < 3.5],
                marker = '^', color = 'g', s = 80, facecolors='none')

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8 and
                helium_stars[i].getMass() >= 3.5],
             [helium_stars[i].getFcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8 and
                helium_stars[i].getMass() >= 3.5], marker = '^', color = 'g', markerfacecolor = 'None',
             markersize = 10, label = r"Final core mass, $\eta = 0.8$")

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             [helium_stars[i].getCcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             '+', color = 'k', markersize = 10, label = r"Core mass after He-depletion, $\eta = 1.0$")

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             [helium_stars[i].getFcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.0],
             marker = '^', color = 'k', markerfacecolor = 'None', markersize = 10,
             label = r"Final core mass, $\eta = 1.0$")

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             [helium_stars[i].getCcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             '+', color = 'magenta', markersize = 10, label = r"Core mass after He-depletion, $\eta = 1.58$")

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             [helium_stars[i].getFcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 1.58],
             marker = '^', color = 'magenta', markersize = 10, markerfacecolor = 'None',
             label = r"Final core mass, $\eta = 1.58$")

    ax2.fill(x_fill_ccsn[:4], y_fill_ccsn[:4], "b", alpha = 0.15) # The range of core mass for Fe-CCSN
    ax2.fill(x_fill_ecsn[:4], y_fill_ecsn[:4], "r", alpha = 0.15) # The range of core mass for ECSN
    ax2.fill(x_fill_wd[:4], y_fill_wd[:4], "y", alpha = 0.15) # The range of core mass for WDs

    ax2.set_xlim([1.8, 9.1])
    ax2.set_ylim([0.5, 5.5])

    legend = ax2.legend(loc = 'upper left', shadow = True, prop={'size': 12})

    ax2.set_xlabel(r'Initial Mass, M$_i$ [M$_{\odot}$]', fontsize = 13)
    ax2.set_ylabel(r'Core Mass, M$_c$ [M$_{\odot}$]', fontsize = 13)
    # --------------------------------------------------------------------------------------------------

    # Fitting curve

    fit = np.polyfit([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
                     [helium_stars[i].getCcore() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
                     1) # Fits a linear function of the form: a*x+b
    fit_fn = np.poly1d(fit)  # fit_fn is now a function which takes in x and returns an estimate for y

    ax2.plot([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8],
             fit_fn([helium_stars[i].getMass() for i in range(0, len(helium_stars)) if helium_stars[i].getWind() == 0.8]),
             '--', color = "tab:red")
    #print(fit)

    # Fitting legend

    props = dict(boxstyle = 'round', facecolor = 'white', alpha = 0.9)
    textstr = '\n'.join(('Linear regression:',
                     r'$M_c \simeq 0.57 \cdot M_i - 0.51$'))

    ax2.text(1.9, 3.9, textstr, fontsize = 13, bbox = props)
    # --------------------------------------------------------------------------------------------------

    # Add second legend

    leg_CCSN = pc.Patch(facecolor = 'b', alpha = 0.15, label = "Fe-CCSN")
    leg_ECSN = pc.Patch(facecolor = 'r', alpha = 0.15, label = "ECSN")
    leg_WD = pc.Patch(facecolor = 'y', alpha = 0.15, label = "WDs")

    ax1.legend(handles = [leg_CCSN, leg_ECSN, leg_WD], loc = 'center', prop={'size': 14},
        bbox_to_anchor = (0.5, 1.05), ncol = 3, shadow = True)

    plt.gca().add_artist(legend)
    # --------------------------------------------------------------------------------------------------


    if saveFigure:
        plt.tight_layout()
        plt.savefig('coreGrowth.png', bbox_inches = 'tight', dpi = 300)
    else:
        plt.tight_layout()
        plt.show()
    



if __name__ == '__main__':
    plotter(saveFigure=True)
