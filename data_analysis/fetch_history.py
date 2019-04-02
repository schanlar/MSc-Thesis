# PATHS
grid_dir = '/vol/hal/halraid/jantoniadis/HeCores/Condor/full_grid'
out_dir = '/vol/aibn1107/data2/schanlar/HeCoresCondor/Histories'

import glob
import os

# Make folder to keep all history files
if not os.path.exists(out_dir):
    os.chdir('/vol/aibn1107/data2/schanlar/HeCoresCondor')
    print('Creating folder...')
    os.system('mkdir ' + 'Histories')


# Fetch from original path
model_paths = [path for path in glob.glob(grid_dir + '/*')]

counter = 1
for path in model_paths:
    folder_name = path[-20:]
    new_history_name = folder_name + '.data'


    logs_path = os.path.join(path,'LOGS')
    os.chdir(logs_path)
    print('Processing...')
    os.system('cp ' + 'history.data ' + out_dir + '/' + new_history_name)
    print('History file #'+ str(counter) + ':', new_history_name, 'created!')
    counter += 1

print(str(counter), 'history files were copied from', grid_dir)
