import mesa_reader as mr
import numpy as np
import os, glob, math, re

################################################################

'''
Find the core mass fraction of carbon and oxygen, when
the star has exited the HeMS phase.
'''

################################################################

grid = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data'
core_masses = []
carbon_fractions = []
model_names = []

for path in glob.glob(os.path.join(grid, '*')):
	model = path.split('/')
	model = model[-1]

	h = mr.MesaData(os.path.join(path, 'LOGS/history.data'))
	has_reached_Rho9 = False
	has_entered_HeMS = False
	#core_mass = 0.0
	#for idx, val in enumerate(h.data('log_LHe')):
	#	if val > 1 and not has_entered_HeMS:
	#		has_entered_HeMS = True

	#	if val < 1 and has_entered_HeMS:
	#		model_number = h.data('model_number')[idx]
	#		core_mass = h.data('c_core_mass')[idx]
	#	try:
	#		if core_mass > 0.0:
	#			core_masses.append(core_mass)
	#			break
	#		else:
	#			continue
	#	except Exception as e:
	#		continue
	for idx, val in enumerate(h.data('c_core_mass')):
		if val > 0.0 and h.data('center_he4')[idx] <= 0.001:
			core_mass = val
			#core_masses.append(core_mass)
			model_number = h.data('model_number')[idx]
			break
	
	print('--'*50)
	print(f'MODEL: {model}')
	print(f'Looking in LOGS for profile closest to {model_number}')

	# Initialize with a large difference
	min_diff = 1000
	with open(os.path.join(path, 'LOGS/profiles.index')) as file:
		next(file)
		for line in file:
			stripped_line = line.strip()
			info = re.split(' |, |\n', stripped_line)
			current_diff = np.abs(model_number - int(info[0]))
			if current_diff <= min_diff:
				min_diff = current_diff
				profile_number = info[-1]
			

	print(f'Found profile{profile_number}.data')

	p = mr.MesaData(os.path.join(path, f'LOGS/profile{profile_number}.data'))

	dm = p.data('dq') * p.data('mass')[0]
	print(f'Core mass: {core_mass}')

	#carbon_mass = (h.data('center_c12')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum()
	#carbon_fraction = carbon_mass / (p.data('mass')[0])

	oxygen_fraction = (p.data('o16')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum() / core_mass
	carbon_fraction = (p.data('c12')[np.where(p.data('mass') <= core_mass)] * dm[np.where(p.data('mass') <= core_mass)]).sum() / core_mass
	if carbon_fraction >= 0.24 or (carbon_fraction+oxygen_fraction) >= 0.8:
		model_names.append(model)
		core_masses.append(core_mass)
		carbon_fractions.append(carbon_fraction)
		print(f'Carbon fraction: {carbon_fraction}')
		print(f'Oxygen fraction: {oxygen_fraction}')
		print(f'Summed: {carbon_fraction+oxygen_fraction}')
	else:
		print('MODEL SKIPPED!')
	
print(f'{min(core_masses)} <= M_c <= {max(core_masses)}')
print(f'{min(carbon_fractions)} <= X_c <= {max(carbon_fractions)}')
