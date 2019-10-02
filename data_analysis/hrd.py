import mesa_reader as mr
#import homogenize_plot as hp
import matplotlib.pyplot as plt
import numpy as np
import os


ORIG_MATPLOTLIB_CONF = dict(plt.rcParams) # Store original settings

def prepare_canvas(fig_width = None, fig_height = None,
        columns = 2, fontsize = 8, revert = False):
    '''
    The basic canvas for plots
    '''

    # FIXME: Change canvas

    assert(columns in [1,2]), f'Columns: {columns} must be either 1 or 2'

    if fig_width is None:
        if columns == 2:
            fig_width = 3.5
        else:
            fig_width = 7

    if fig_height is None:
        golden_mean = (np.sqrt(5.0) - 1.0) / 2.0    # Aesthetic ratio
        fig_height = fig_width * golden_mean # height in inches

    params = {'backend': 'pdf',
                  #'text.latex.preamble':
                  #[ r'\usepackage{siunitx}',
                  #  r'\usepackage[utf8]{inputenc}',
                  #  r'\usepackage[T1]{fontenc}',
                  #  r'\DeclareSIUnit \jansky {Jy}' ],
                  'axes.labelsize' : fontsize,
                  'axes.titlesize' : fontsize,
                  'font.size': fontsize,
                  'legend.fontsize' : fontsize,
                  'xtick.labelsize' : fontsize,
                  'ytick.labelsize' : fontsize,
                  #'xtick.major.size' : 18,
                  #'xtick.minor.size' : 9,
                  #'ytick.major.size' : 18,
                  #'ytick.minor.size' : 9,
                  #'xtick.major.width' : 0.8,
                  #'xtick.minor.width' : 0.6,
                  #'ytick.major.width' : 0.8,
                  #'ytick.minor.width' : 0.6,
                  'axes.linewidth' : 0.5,
                  'lines.linewidth' : 1,
                  'text.usetex' : True,
                  'figure.figsize' : [fig_width, fig_height],
                  'font.family' : 'serif',
                  'savefig.bbox' : 'tight',
                  'savefig.dpi' : 300  # set to 600 for poster printing or PR
                                      # figures
        }

    plt.rcParams.update(params)



    if revert:
        plt.rcParams.update(ORIG_MATPLOTLIB_CONF) # Call global configuration
                                                      # for plots



logs_path = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data/2.5000_0.0200_0.0000/LOGS'

h = mr.MesaData(os.path.join(logs_path, 'history.data'))

Teff = h.data('log_Teff')
logL = h.data('log_L')
he = h.data('log_LHe')
filt = np.where(he>1)
filt = filt[0][0]

#hp.homogenise_plot()
prepare_canvas(columns=1, fontsize=10)
plt.xlabel(r'$\rm \log(T_{eff}/K)$')
plt.ylabel(r'$\rm \log(L/L_{\odot})$')

plt.gca().invert_xaxis()

plt.plot(Teff[filt:], logL[filt:], c='b', label=r'$\rm 2.5 M_{\odot}; Z=0.02, f_{OV} = 0.0$')

legend = plt.legend(loc = 'upper left', shadow = False)

#plt.show()

plt.savefig('HRD.pdf')
