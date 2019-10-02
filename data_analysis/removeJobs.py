import os

def remove(starting_number, final_number):
    iterations = float(final_number) - float(starting_number)
 
    for model in range(0, int(iterations)):
        next_model = float(starting_number) + float(model)
        os.system('condor_rm ' + str(next_model))
        os.system('sleep 0.3')


def main():
    x = input("Starting model: ")
    y = input("Last model: ")

    remove(x,y)


if __name__ == '__main__':
    main()
