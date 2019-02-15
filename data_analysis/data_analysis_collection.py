import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pc
import mesa_reader as mr
import astropy.units as u
import astropy.constants as c
import os

#from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
#from mpl_toolkits.axes_grid1.inset_locator import mark_inset


mesa_dir = '/vol/aibn1107/data2/schanlar/mesa-r10398'
work_dir = '/vol/aibn1107/data2/schanlar/Thesis_work/singles/Case_B_urca/'
plot_results_dir = '/users/schanlar/Desktop/HeliumCores2'

# The basic canvas for plots
def prepare_canvas():
    plt.rcParams['figure.figsize'] = [15, 10]
    plt.rcParams['axes.linewidth'] = 2 #3
    #plt.legend(prop={'size': 16})
    #legend = plt.legend(loc = 'upper left', prop = {'size':12},
          #bbox_to_anchor=(1, 1), shadow = True)

    fontsize = 15 #20
    ax = plt.gca()
    ax.tick_params(direction='in',length=5)
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(fontsize)
        tick.label1.set_fontweight('bold')
# ------------------------------------------------------------------------------

# Density for electron captures
def capture_density(t,rho_0,Q,t_comp,ft):
    rho = rho_0/(1 + (3*c.k_B*t/Q)* np.log(2*np.log(2)*(c.k_B*t/(c.m_e*c.c**2))**5 * (Q/(c.k_B*t))**2 * (t_comp/ft)))
    return rho
# ------------------------------------------------------------------------------

# Plot various limits for nuclear burning + weak reactions
def burning_regions(mesa_dir = mesa_dir,
                    xlim=None,
                    ylim=None,
                    ecap_density_corrections=True,
                    t_comp=1e4*u.yr):


 #   hydrogen_burning_line = os.path.join(mesa_dir,'data/star_data/plot_info/hydrogen_burn.data')
    helium_burning_line = os.path.join(mesa_dir,'data/star_data/plot_info/helium_burn.data')
    carbon_burning_line = os.path.join(mesa_dir,'data/star_data/plot_info/carbon_burn.data')
    oxygen_burning_line = os.path.join(mesa_dir,'data/star_data/plot_info/oxygen_burn.data')
    electron_degeneracy_line = os.path.join(mesa_dir,'data/star_data/plot_info/psi4.data')



 #   hburn = np.genfromtxt(hydrogen_burning_line)
    heburn = np.genfromtxt(helium_burning_line)
    cburn = np.genfromtxt(carbon_burning_line)
    oburn = np.genfromtxt(oxygen_burning_line)
    electron = np.genfromtxt(electron_degeneracy_line)


    # Radiation pressure line
    logrho = np.arange(-9.0,10.0,0.1)
    logt = np.log10(3.2e7) + (logrho - np.log10(0.7))/3.0


    plt.plot(heburn[:,0],heburn[:,1],ls=':',color='black')
    plt.text(5.1, 7.95, 'He burn', fontsize=22,
               rotation=0, rotation_mode='anchor')


    plt.plot(cburn[:,0],cburn[:,1],ls=':',color='black')
    plt.text(5.1, 8.67, 'C burn', fontsize=22,
               rotation=0, rotation_mode='anchor')


    plt.plot(oburn[:,0],oburn[:,1],ls=':',color='black')
    plt.text(5.1, 9.05, 'O burn', fontsize=22,
               rotation=0, rotation_mode='anchor')

    plt.plot(electron[:,0],electron[:,1],ls='--',color='black')

    plt.plot(logrho,logt,ls='--',color='black')

    plt.text(7.0, 9.5, r'$\epsilon_{\rm F}/k T \simeq 4$', fontsize=22, rotation=0, rotation_mode='anchor')

    plt.text(5.12, 9.5, r'$P_{\rm rad}\simeq P_{\rm gas}$', fontsize=22, rotation=0, rotation_mode='anchor')


    #Weak reaction lines
    plt.text(9.05, 7.52, r'$^{25}{\rm Mg}\leftrightarrow ^{25}{\rm Na}$', fontsize=15, rotation=90,verticalalignment='bottom')
    plt.text(9.25, 7.52, r'$^{23}{\rm Na} \leftrightarrow ^{23}{\rm Ne}$', fontsize=15, rotation=90,verticalalignment='bottom')
    plt.text(9.65, 7.52, r'$^{24}{\rm Mg}\rightarrow ^{24}{\rm Na}$', fontsize=15, rotation=90,verticalalignment='bottom')
    plt.text(9.75, 7.52, r'$^{24}{\rm Na}\rightarrow ^{24}{\rm Ne}$', fontsize=15, rotation=90,verticalalignment='bottom')
    plt.text(9.85, 7.52, r'$^{25}{\rm Na}\leftrightarrow ^{25}{\rm Ne}$', fontsize=15, rotation=90,verticalalignment='bottom')
    plt.text(10.00, 7.52, r'$^{20}{\rm Ne}\rightarrow ^{20}{\rm F}\rightarrow  ^{20}{\rm O}$', fontsize=15, rotation=90,verticalalignment='bottom')


    if ecap_density_corrections:
        t = np.arange(7.5,11,0.1)
        t = 10**t * u.K
        rho_ce = capture_density(t,10**9.96,7.025*u.MeV,t_comp,10**9.801*u.s)
        plt.plot(np.log10(rho_ce),np.log10(t.value),color='red',ls='--')
    else:
        plt.axvline(x=9.96,color='red',ls='-')

    plt.text(10.0, 8.3, r'$e^{-}$cSN', fontsize=15, rotation=90,color='red',verticalalignment='bottom')
# ------------------------------------------------------------------------------

# Central density vs central temperature
def logRho_logT_plotter(paths,
                        labels,
                        xlim=None,
                        ylim=None,
                        saveFigure=False
                        ):

    prepare_canvas()
    burning_regions()

    # now loop over data
    for i in range(len(paths)):
        h = mr.MesaData(paths[i])
        plt.plot(h.data('log_center_Rho'),h.data('log_center_T'),label=labels[i])

    legend = plt.legend(loc = 'upper left', prop = {'size':12},
          bbox_to_anchor=(1, 1), shadow = True)

    #frame & labels
    xlabel = r'$\log (\rho_{\rm c} / {\rm gr}\,{\rm cm}^{-3})$'
    ylabel = r'$\log (T_{\rm c} / {\rm K})$'
    plt.xlabel(xlabel, fontsize=23)
    plt.ylabel(ylabel, fontsize=23)

    if xlim:
        plt.xlim(xlim)
    else:
        plt.xlim([5,10.5])
    if ylim:
        plt.ylim(ylim)
    else:
        plt.ylim([7.5,10.0])


    if saveFigure:
        plt.savefig(os.path.join(plot_results_dir,'Rhoc_vs_Tc.pdf'), bbox_inches = 'tight', dpi =300)
        plt.show()
    else:
        plt.show()
# ------------------------------------------------------------------------------

# Mass-loss rate vs mass
def mdot_vs_mass(paths,labels, saveFigure=False):

    prepare_canvas()
    for i in range(len(paths)):
        h = mr.MesaData(paths[i])
        plt.plot(h.data('star_mass'),h.data('log_abs_mdot'),label=labels[i])

    legend = plt.legend(loc = 'upper left', prop = {'size':12},
      bbox_to_anchor=(1, 1), shadow = True)

    xlabel = r'Mass [M$_{\odot}]$'
    ylabel = r'$\dot{M}\,{\rm [ M}_{\odot}\,{\rm yr}^{-1}$]'
    plt.xlabel(xlabel, fontsize=23)
    plt.ylabel(ylabel,fontsize=23)

    plt.ylim([-10,-3.0])

    if saveFigure:
        plt.savefig(os.path.join(plot_results_dir,'mdot_vs_m.pdf'), bbox_inches = 'tight', dpi =300)
        plt.show()
    else:
        plt.show()
# ------------------------------------------------------------------------------

# Hertzprung-Russel Diagram
def hrd(paths,labels, saveFigure=False):

    prepare_canvas()

    xlabel = r'$\log(T_{eff}/[K])$'
    ylabel = r'$\log(L/[L_{\odot}])$'
    plt.xlabel(xlabel, fontsize=23)
    plt.ylabel(ylabel, fontsize=23)

    for i in range(len(paths)):
        h = mr.MesaData(paths[i])
        he = h.data('log_LHe')
        filt = np.where(he>1)
        filt = filt[0][0]
        plt.plot(h.data('log_Teff')[filt:],h.data('log_L')[filt:],label=labels[i])

    legend = plt.legend(loc = 'upper left', prop = {'size':12},
        bbox_to_anchor=(1, 1), shadow = True)


    plt.xlim([5,3])

    if saveFigure:
        plt.savefig(os.path.join(plot_results_dir,'hrd.pdf'), bbox_inches = 'tight', dpi =300)
        plt.show()
    else:
        plt.show()
# ------------------------------------------------------------------------------

# Energetics
def potential_energy(rad,rho):
    udr = c.G*16./3. * np.pi**2. *rho**2 * rad**4
    return np.trapz(udr,rad).to(u.erg)


def total_energy(Et,mass):
    Et = Et*u.erg/u.gram
    mass = (mass*u.Msun)

    return (Et*mass).sum().to(u.erg)

def nuc_energy(A1,A2,mu1,mu2,X,mtot):
     # A1 -> A2 + energy
    energy_per_reaction = ((A2*mu1 - A1*mu2)*u.mu*c.c**2).to(u.erg)
    reactions_per_gram = (1*u.g / (A2*mu1*u.mu)).to(u.dimensionless_unscaled)/u.g
    mtot = u.Quantity(mtot,u.Msun)
    return (energy_per_reaction*reactions_per_gram *(X*mtot)).to(u.erg)

def abundance_calc(path, mcore, massCut = 0.7, displayElements = False):
    # Calculates the abundance of specific elements.
    # X1 refers to the abundance of elements that will
    # be burned to Nickel (mass cut at 0.7),
    # whilst X2 refers to the abundance of elements
    # that will be burned to Silicon.

    p = mr.MesaData(path)

    species = ['c12', 'o16', 'ne20', 'ne22', 'ne23', 'na23', 'na25', 'mg24', 'mg25', 'si28']
    X1 = []
    X2 = []

    for element in range(len(species)):

        t = p.data(species[element])[p.data('mass') <= massCut] # abundance of a species below massCut
        k = p.data(species[element])[p.data('mass') >= (mcore - massCut)] # abundance of a species above massCut

        X1.append(np.mean(t))
        X2.append(np.mean(k))

        if displayElements:
            print('Abundance of '+ str(species[element]) + ' for M <= ' + str(massCut) + ': ', X1[-1])
            print('Abundance of '+ str(species[element]) + ' for M >= ' + str(massCut) + ': ', X2[-1])
            print('--')

    return X1, X2
# ------------------------------------------------------------------------------

def pressure_regimes_plotter(paths,
                            labels,
                            xlim=None,
                            ylim=None,
                            saveFigure=False):


    prepare_canvas()

    for i in range(len(paths)):
        h = mr.MesaData(paths[i])
        plt.plot(h.data('log_center_Rho'),h.data('log_center_T'),label=labels[i])

    legend = plt.legend(loc = 'upper left', prop = {'size':12},
          bbox_to_anchor=(1, 1), shadow = True)


    #frame & labels
    xlabel = r'$\log (\rho_{\rm c} / {\rm gr}\,{\rm cm}^{-3})$'
    ylabel = r'$\log (T_{\rm c} / {\rm K})$'
    plt.xlabel(xlabel, fontsize=23)
    plt.ylabel(ylabel, fontsize=23)

    if xlim:
        plt.xlim(xlim)
    else:
        plt.xlim([5,10.5])
    if ylim:
        plt.ylim(ylim)
    else:
        plt.ylim([7.5,10.0])


    # **********************************************************************************************
    x_fill_deg = [1.59, 6.4, 6.4]
    y_fill_deg = [6, 6, 8.9]
    plt.fill(x_fill_deg, y_fill_deg, 'y', alpha = 0.1)

    x_fill_non_deg = [0, 1.59, 6.4, 3.94]
    y_fill_non_deg = [7.59, 6, 8.9, 8.9]
    plt.fill(x_fill_non_deg, y_fill_non_deg, 'g', alpha = 0.1)

    x_fill_non_deg2 = [3.94, 6.4, 9.4, 7.25]
    y_fill_non_deg2 = [8.9, 8.9, 10, 10]
    plt.fill(x_fill_non_deg2, y_fill_non_deg2, 'g', alpha = 0.1)

    x_fill_non_deg3 = [0, 1.59, 0]
    y_fill_non_deg3 = [6, 6, 7.59]
    plt.fill(x_fill_non_deg3, y_fill_non_deg3, 'g', alpha = 0.1)

    x_fill_rel = [6.4, 9.4, 9.4, 6.4]
    y_fill_rel = [6, 6, 10, 8.9]
    plt.fill(x_fill_rel, y_fill_rel, 'r', alpha = 0.1)

    x_fill_rel2 = [9.4, 11, 11, 9.4]
    y_fill_rel2 = [6, 6, 10, 10]
    plt.fill(x_fill_rel2, y_fill_rel2, 'r', alpha = 0.1)


    x_fill_non_deg_non_rel = [0, 7.25, 0]
    y_fill_non_deg_non_rel = [7.59, 10, 10]
    plt.fill(x_fill_non_deg_non_rel, y_fill_non_deg_non_rel, 'b', alpha = 0.1)


    leg_NDNR = pc.Patch(facecolor = 'g', alpha = 0.2, label = 'Non-degenerate, non-relativistic')
    leg_NDR = pc.Patch(facecolor = 'b', alpha = 0.2, label = 'Non-degenerate, relativistic')
    leg_DNR = pc.Patch(facecolor = 'y', alpha = 0.2, label = 'Degenerate, non-relativistic')
    leg_DR = pc.Patch(facecolor = 'r', alpha = 0.2, label = 'Degenerate, relativistic')

    plt.legend(handles = [leg_NDNR, leg_NDR, leg_DNR, leg_DR], loc = 'center', prop = {'size':12},
              bbox_to_anchor=(0.5, 1.05), ncol=2, fancybox=True, shadow = True)

    plt.gca().add_artist(legend)

    # **********************************************************************************************

    if saveFigure:
        plt.savefig(os.path.join(plot_results_dir,'Rho_T_press_regimes.pdf'), bbox_inches = 'tight', dpi =300)
        plt.show()
    else:
        plt.show()
