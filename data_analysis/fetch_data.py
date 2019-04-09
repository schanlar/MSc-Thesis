# PATHS
grid_dir = '/vol/hal/halraid/jantoniadis/HeCores/Condor/full_grid'
out_dir = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data'

import glob
import os, sys

sys.stdout = open('fetch_data_log.txt', 'wt')

# Make folder to keep data
if not os.path.exists(out_dir):
    os.chdir('/vol/aibn1107/data2/schanlar/HeCoresCondor')
    print('Creating folder...')
    os.system('mkdir full_data')


# Fetch from original path
model_paths = [path for path in glob.glob(grid_dir + '/*')]


historyExists = 0
profileExists = 0


for tag, path in enumerate(model_paths, start = 1):

    logs_path = os.path.join(path,'LOGS')
    if os.path.isfile(logs_path + '/history.data'):
       
        historyExists += 1

        folder_name = path[-20:]
        os.chdir(out_dir)
        os.system('mkdir ' + folder_name)
        new_model_path = os.path.join(out_dir, folder_name)

        os.chdir(logs_path)
        print('Processing...')
        os.system('cp history.data ' + new_model_path)
        print('History file #'+ str(tag) + ' in:', folder_name, 'created!')


    else:
        
        print('History file #'+ str(tag) + ' from:', folder_name, 'was not found!')



    if os.path.isfile(path + '/final_profile.data'):
        
        profileExists += 1

        os.chdir(path)
        os.system('cp final_profile.data ' + new_model_path)
        print('Final profile #' + str(tag) + ' in:', folder_name, 'created')


    else:
       
        print('Final profile #' + str(tag) + ' from:', folder_name, 'was not found!')



print(str(historyExists), 'history files ' + 'out of ' + str(tag) + ' were copied from', grid_dir)
print(str(profileExists), 'profile files ' + 'out of ' + str(tag) + ' were copied from', grid_dir)

sys.stdout.close()
