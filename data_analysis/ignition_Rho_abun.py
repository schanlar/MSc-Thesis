import mesa_reader as mr
import numpy as np
import os,math,glob,re

##############################################################

'''
Here we consider an ignition temperature (for oxygen) at 
log(T) = 9.17, instead at max density.
'''

##############################################################


grid = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data'

models = ['1.8000_0.0200_0.0140', '1.8000_0.0200_0.0160',
	  '1.9000_0.0010_0.0160', '1.9000_0.0200_0.0140', '1.9000_0.0200_0.0160',
	  '2.0000_0.0001_0.0160', '2.0000_0.0010_0.0160', '2.0000_0.0200_0.0160',
	  '2.1000_0.0010_0.0160', '2.1000_0.0200_0.0000', '2.1000_0.0200_0.0160',
	  '2.2000_0.0200_0.0000', '2.2000_0.0200_0.0160',
	  '2.3000_0.0200_0.0000', '2.3000_0.0200_0.0160',
	  '2.4000_0.0010_0.0000', '2.4000_0.0200_0.0000',
	  '2.5000_0.0010_0.0000', '2.5000_0.0200_0.0000',
	  '2.6000_0.0010_0.0000', '2.6000_0.0200_0.0000',
	  '2.7000_0.0200_0.0000']

for path in glob.glob(os.path.join(grid, '*')):
	model = path.split('/')
	model = model[-1]
	model_ignites = False
	if model in models:
		h = mr.MesaData(os.path.join(path, 'LOGS/history.data'))
		for idx,val in enumerate(h.data('log_center_T')):
			if math.isclose(val, 9.17, rel_tol = 0.01):
				ignition_density = h.data('log_center_Rho')[idx]
				model_ignites = True
		if not model_ignites:
			print('Model does not reach ignition temperature!')
			continue
		min_diff = 1000
		for profile in glob.glob(os.path.join(path, 'LOGS/profile*')):
			if profile.split('/')[-1] == 'profiles.index':
				continue
			p = mr.MesaData(profile)
			current_diff = np.abs(p.data('logRho')[-1] - ignition_density)

			if current_diff <= min_diff:
				min_diff = current_diff
				profile_Rho9 = profile.split('/')[-1]


		p = mr.MesaData(os.path.join(path, f'LOGS/{profile_Rho9}'))
		dm = p.data('dq') * p.data('mass')[0]

		# Define core boundary
		mask = 0.80 * max(p.data('logP'))
		core_mass = p.data('mass')[np.where(p.data('logP') < mask)][-1]

		# Calculate mass fractions within the core
		carbon_fraction = (p.data('c12')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum() / core_mass
		oxygen_fraction = (p.data('o16')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum() / core_mass
		neon_fraction = (p.data('ne20')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum() / core_mass	
		oxygen_to_neon_ratio = oxygen_fraction / neon_fraction

		print('--'*50)
		print(f'MODEL: {model}, profile: {profile_Rho9}, at density: {p.data("logRho")[-1]}, (ignition Rho: {ignition_density}), core mass: {core_mass}')
		print(f'Carbon fraction: {carbon_fraction}')
		print(f'Oxygen fraction: {oxygen_fraction}')
		print(f'Neon fraction: {neon_fraction}')
		print(f'O16/Ne20: {oxygen_to_neon_ratio}')

