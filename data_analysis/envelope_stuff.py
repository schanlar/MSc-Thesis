import mesa_reader as mr
import numpy as np
import matplotlib.pyplot as plt
import os

logs_path = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data/2.5000_0.0200_0.0000/LOGS'

h = mr.MesaData(os.path.join(logs_path, 'history.data'))
p1 = mr.MesaData(os.path.join(logs_path, 'profile4.data'))
p2 = mr.MesaData(os.path.join(logs_path, 'profile82.data'))

logL = h.data('log_L')
mdot = h.data('log_abs_mdot')
logRho = h.data('log_center_Rho')



plt.figure(figsize = (10,6))

#plt.plot(logL[np.where(mdot > -8)], mdot[np.where(mdot > -8)])
#plt.plot(logRho, h.data('log_center_T'))

plt.plot(p1.data('radius'), p1.data('logRho'))
plt.plot(p2.data('radius'), p2.data('logRho'))


#plt.axvline(8.30695475116774, c='r', linestyle = '--')
plt.show()




for idx, val in enumerate(logL):
	if val == max(logL):
		print(f'Max luminosity (log): {val}')
		print(f'Corresponding mdot: {mdot[idx]}')
		print(f'Max mdot: {max(mdot)}')
		print(f'Max luminosity at density: {logRho[idx]}')
		print(f'radius: {10**h.data("log_R")[idx]} Rsol')
		print(f'Max radius: {max(10**h.data("log_R"))} Rsol')


