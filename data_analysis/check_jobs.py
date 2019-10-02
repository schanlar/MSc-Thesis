import glob
from file_read_backwards import FileReadBackwards
import time
import warnings

#condorPath = '/vol/hal/halraid/jantoniadis/HeCores/Condor/full_grid'
condorPath = '/vol/hal/halraid/schanlar/Condor/Binaries'
#condorPath = '/vol/hal/halraid/schanlar/Condor/carbon_free'
config = 'binary'


def checkOutput(path, config = 'single'):
    '''
    The config variable accepts either the value "single" or
    the value "binary"
    '''


    hasFinished = False
    keyword1 = 'stop because'
    keyword2 = 'termination'
    line_counter = 1

    if config == 'single':
        #name = path[-20:]
        t_ar = path.split('/')
        name = t_ar.pop(-1)
    elif config == 'binary':
        idx = path.index('bin')
        name = path[idx:]
    else:
        raise ValueError('config must be set either to single or binary!')


    with FileReadBackwards(f'{path}/condor.out') as file:
        for line in file:
            # check only the last 20 lines
            if line_counter <= 20:
                if line.startswith(f'{keyword1}') or line.startswith(f'{keyword2}'):
                    current_status = f'Model {name} has been terminated!'
                    hasFinished = True
                    break
                else:
                    current_status = f'Model {name} still running!'
                line_counter += 1
            else:
                break
    return hasFinished, current_status


def main():

    start_timer = time.time()

    model_paths = [path for path in glob.glob(condorPath + '/*')]
    model_paths.sort()

    finished = 0
    running = 0
    for i in model_paths:
        try:
            hasFinished, status = checkOutput(i, config=config)

            if hasFinished:
                print(status)
                finished += 1
            else:
                print(status)
                running += 1
        except:
            #pass
            warnings.warn('Run into trouble when trying to check this path', SyntaxWarning)

    print(f'From {len(model_paths)} models, {finished} have finished, and {running} are still running!')
    stop_timer = time.time()
    print(f'Time elapsed: {round(stop_timer - start_timer, 2)} seconds')

if __name__ == '__main__':
    main()
