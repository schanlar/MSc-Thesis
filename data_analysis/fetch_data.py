'''
###############################################################
			HOW TO
###############################################################

Step 1: Define the path to the server where
the data are stored -> grid_dir

Step2: Execute the script from the command
line as follows

	$ python fetch_data.py /path/to/local/folder/name True

if you want all of the data to be copied, or

	$ python fetch_data.py /path/to/local/folder/name False

if you want to obtain only a copy of the history file, and the
final/last saved profile

###############################################################
'''


import glob
import os, sys
import time
from file_read_backwards import FileReadBackwards



# PATHS
grid_dir = '/vol/hal/halraid/jantoniadis/HeCores/Condor/full_grid'

#out_dir = '/vol/aibn1107/data2/schanlar/HeCoresCondor/small_data'
#out_dir = '/vol/aibn1107/data2/schanlar/HeCoresCondor/full_data'
#fetchAll = False






def fetch(grid_dir, out_dir, fetchAll = False):

    '''
    The function takes two absolute paths as arguments:
    the path where it will look up for the data, and
    the path where it will save them.

    A third optional argument can be provided if you
    want to copy the full data set.
    By default this argument is set to False, hence
    the script will attempt to copy just the history
    and the last saved profile.
    '''

    n = 'data'

    # Make folder to keep data
    if not os.path.exists(out_dir):

        sp = out_dir.split('/')
        n = sp.pop(-1) # The name of the folder
        os.chdir(f'{"/".join(sp)}') # The absolute path

        print('Creating folder...')

        os.system(f'mkdir {n}')

    sys.stdout = open(f'fetch_{n}_log.txt', 'wt')

    # Fetch from original path
    model_paths = [path for path in glob.glob(grid_dir + '/*')]
    model_paths.sort()


    historyExists = 0
    profileExists = 0


    for tag, path in enumerate(model_paths, start = 1):

        logs_path = os.path.join(path,'LOGS')

        if fetchAll:

            sp = path.split('/')
            folder_name = sp.pop(-1)

            os.chdir(out_dir)
            os.system(f'mkdir {folder_name}')
            new_model_path = os.path.join(out_dir, folder_name)

            os.system(f'cp -r {logs_path} {new_model_path}')

        else:

            if os.path.isfile(logs_path + '/history.data'):

                historyExists += 1

                #folder_name = path[-20:]
                sp = path.split('/')
                folder_name = sp.pop(-1)

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
                print('#'*50)


            else:

                print('Final profile #' + str(tag) + ' from:', folder_name, 'was not found!')

                with FileReadBackwards(f'{logs_path}/profiles.index') as file:
                    for line in file:
                        num = line.split(' ')
                        break

                print('Copying last saved profile...')

                os.system(f'cp {logs_path}/profile{num[-1]}.data {new_model_path}')
                print('#'*50)



    print(str(historyExists), 'history files ' + 'out of ' + str(len(model_paths)) + ' were copied from', grid_dir)
    print(str(profileExists), 'final profiles ' + 'out of ' + str(len(model_paths)) + ' were copied from', grid_dir)

    #sys.stdout.close()



def main():

    out_dir = sys.argv[1]
    fetchAll = sys.argv[2]

    if fetchAll == 'False' or fetchAll == 'false':
        fetchAll = False
    elif fetchAll == 'True' or fetchAll == 'true':
        fetchAll = True
    else:
        raise ValueError('Unrecognized argument!')

    start = time.time()
    fetch(grid_dir = grid_dir, out_dir = out_dir, fetchAll = fetchAll)
    end = time.time()

    time_elapsed = end - start

    print(f'Elapsed time: {round(time_elapsed, 2)} seconds.')


if __name__ == '__main__':
    main()
