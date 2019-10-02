import numpy as np
from astropy import units as u
from astropy import constants as c
import mesa_reader as mr
import os



def nuc_energy(A1,A2,mu1,mu2,X,mtot):

     # A1 -> A2 + energy

    energy_per_reaction = ((A2*mu1 - A1*mu2)*u.mu*c.c**2).to(u.erg)

    reactions_per_gram = (1*u.g / (A2*mu1*u.mu)).to(u.dimensionless_unscaled)/u.g

    mtot = u.Quantity(mtot,u.Msun)

    return (energy_per_reaction*reactions_per_gram *(X*mtot)).to(u.erg)

def kinetic_energy(p,Xige,Xime,Xfe=0.2):

    mass = p('dq')*p('mass')[0]

    Mige = p('mass')[0]*Xige

    Mime = p('mass')[0]*Xime

    c12  = 12.00000

    o16  = 15.994915

    ne20 = 19.992440

    na23 = 22.989769

    mg24 = 23.985042

    si28 = 27.976927

    fe56 = 55.934937

    ni56 = 55.942129



    E = 0.0

    msum = 0.0

    i=0

    for m in mass[::-1]:

        if msum <= Mige:

            E += nuc_energy(12,56,c12,ni56,p('c12')[::-1][i]*(1-Xfe),m)

            E += nuc_energy(12,56,c12,fe56,p('c12')[::-1][i]*Xfe,m)

            E += nuc_energy(16,56,o16,ni56,p('o16')[::-1][i]*(1-Xfe),m)

            E += nuc_energy(16,56,o16,fe56,p('o16')[::-1][i]*Xfe,m)

            E += nuc_energy(20,56,ne20,ni56,p('ne20')[::-1][i]*(1-Xfe),m)

            E += nuc_energy(20,56,ne20,fe56,p('ne20')[::-1][i]*Xfe,m)

            E += nuc_energy(23,56,na23,ni56,p('na23')[::-1][i]*(1-Xfe),m)

            E += nuc_energy(23,56,na23,fe56,p('na23')[::-1][i]*Xfe,m)

            E += nuc_energy(24,56,mg24,ni56,p('mg24')[::-1][i]*(1-Xfe),m)

            E += nuc_energy(24,56,mg24,fe56,p('mg24')[::-1][i]*Xfe,m)

        elif ((msum > Mige) & (msum <= (Mige+ Mime))):

            E += nuc_energy(12,28,c12,si28,p('c12')[::-1][i],m)

            E += nuc_energy(16,28,o16,si28,p('o16')[::-1][i],m)

            E += nuc_energy(20,28,ne20,si28,p('ne20')[::-1][i],m)

            E += nuc_energy(23,28,na23,si28,p('na23')[::-1][i],m)

            E += nuc_energy(24,28,mg24,si28,p('mg24')[::-1][i],m)

        i+=1

        msum += m

    Eint=(p('total_energy')*mass* u.erg/u.gram * u.Msun).sum().to(u.erg)


    return E,Eint,E+Eint







if __name__ == '__main__':

    path = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data/2.5000_0.0200_0.0000/LOGS'
    profile_path = os.path.join(path, 'profile3.data')
    p = mr.MesaData(profile_path).data

    a,b,c = kinetic_energy(p,Xige=0.6,Xime=0.6,Xfe=0.1)

    print(a,b,c)
