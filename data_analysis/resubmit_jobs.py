import re
import os
import glob
from file_read_backwards import FileReadBackwards

condorPath = '/vol/hal/halraid/schanlar/Condor/carbon_free'





def searchOutput(path):

    with FileReadBackwards(path+'/condor.out') as file:
        for line in file:
            if line.startswith('save ' + path + '/photos/') or line.startswith('save photos/'):
                words = re.split('/|, | ', line)
                break
    return words[-4], words[-1]



def createFiles(path):

    out_dir = os.path.join(path, 'Restarted')
    condor_out_path = os.path.join(out_dir, 'condor_restart.out')
    condor_log_path = os.path.join(out_dir, 'condor_restart.log')
    condor_err_path = os.path.join(out_dir, 'condor_restart.err')

    if not os.path.isdir(out_dir):

        os.system('mkdir ' + out_dir)
        os.chdir(out_dir)

        os.system('touch condor_restart.out')
        os.system('touch condor_restart.log')
        os.system('touch condor_restart.err')

        os.chdir(path)
        os.system('touch condor.re')
        os.system('touch restart_mesa.sh')

        os.system('echo ' + 'Universe = vanilla >> condor.re')
        os.system('echo ' + 'getenv = True >> condor.re')
        os.system('echo ' + 'Executable = restart_mesa.sh >> condor.re')
        os.system('echo ' + 'Output =' + condor_out_path +' >> condor.re')
        os.system('echo ' + 'Error =' + condor_err_path + ' >> condor.re')
        os.system('echo ' + 'Log =' + condor_log_path + ' >> condor.re')
        os.system('echo ' + 'image_size = 4 GB >> condor.re')
        os.system('echo ' + 'request_memory = 4 GB >> condor.re')
        os.system('echo ' + 'environment = OMP_NUM_THREADS=1;PYTHONBUFFERED=1;MESA_DIR=/vol/aibn1107/data2/schanlar/mesa-r10398 >> condor.re')
        os.system('echo ' + 'request_cpus = 1 >> condor.re')
        os.system('echo ' + 'queue >> condor.re')

    else:
        print("Files already exist!")




def restartMesa(path, photo, model):

    out_dir = os.path.join(path, 'Restarted')

    fileExists = os.path.isfile(path + '/restart_mesa.sh')

    if fileExists:
        os.chdir(path)
        os.system('> restart_mesa.sh')
        os.system('echo ' + '\#\!/bin/bash >> restart_mesa.sh')
        os.system('echo ' + './re ' + photo + ' >> restart_mesa.sh')

        os.system('chmod +x ' + os.path.join(path, 'restart_mesa.sh'))
        print('Restarting photo', photo, 'for model', model)
        os.system('condor_submit condor.re')







def main():

    #dir_paths = [i for i in glob.glob(condorPath + '/*')]

    dir_paths = ['/vol/hal/halraid/schanlar/Condor/carbon_free/2.1000_0.0200_0.0000']

    for path in dir_paths:

        try:

            os.chdir(path)
            photo, model = searchOutput(path)

            createFiles(path)
            restartMesa(path, photo, model)
    
        except Exception as e:
            print(f'Something went wrong for {path}')
            print(e) 
            continue









if __name__ == '__main__':
    main()    


            


