'''
@author Savvas Chanlaridis
@version v.13.12.18
@description:
Create a class (star) that defines a star in terms of its initial mass
and other parameters
'''

class star(object):

    # We assume the star is not in a binary system

    # Constructor

    def __init__(self, mass, binary = False, **kwargs):
        self.initial_mass = mass
        self.binary = binary
        self.carbon_core = kwargs.get('ccore')
        self.final_core = kwargs.get('fcore')
        self.final_mass = kwargs.get('fmass')
        self.helium_envelope = kwargs.get('envelope')
        self.wind_eta = kwargs.get('wind')
        self.fate = kwargs.get('fate')
        self.termination = kwargs.get('termination')


    def __str__(self):
        return 'Star[' + '\n' + \
                '> In binary: ' + str(self.binary) + '\n' + \
                '> Initial mass: ' + str(self.initial_mass) + '\n' + \
                '> Carbon-core mass: ' + str(self.carbon_core) + '\n' + \
                '> Final metal-core mass: ' + str(self.final_core) + '\n' + \
                '> Final star mass: ' + str(self.final_mass) + '\n' + \
                '> He-rich envelope mass: ' + str(self.helium_envelope) + '\n' + \
                '> Wind scaling factor: ' + str(self.wind_eta) + '\n' + \
                '> Final fate: ' + str(self.fate) + '\n' + \
                '> Termination code: ' + str(self.termination) + '\n' + \
                ']'

    # Accesser Methods (Getters)

    def getMass(self):
        return self.initial_mass

    def getCcore(self):
        return self.carbon_core

    def getFcore(self):
        return self.final_core

    def getFmass(self):
        return self.final_mass

    def getEnvelope(self):
        return self.helium_envelope

    def getWind(self):
        return self.wind_eta

    def getFate(self):
        return self.fate

    def getTermination(self):
        return self.termination

    def getBinary(self):
        return self.binary



    # Mutator Methods (setters)

    def setMass(self, new_mass):
        self.initial_mass = new_mass

    def setCcore(self, new_ccore):
        self.carbon_core = new_ccore

    def setFcore(self, new_fcore):
        self.final_core = new_fcore

    def setFmass(self, new_fmass):
        self.final_mass = new_fmass

    def setEnvelope(self, new_envelope):
        self.helium_envelope = new_envelope

    def setWind(self, new_eta):
        self.wind_eta = new_eta

    def setFate(self, new_fate):
        self.fate = new_fate

    def setTermination(self, new_code):
        self.termination = new_code

    def setBinary(self, new_binary):
        self.binary = new_binary






def debug():
    '''
    FOR DEBUGGING ONLY!
    '''


    # Create some star objects

    star1 = star(mass = 3.5, ccore = 1.17, fate = 'Fe-CCSN', fmass = 3.1, fcore = 1.44,
            envelope = 1.5, termination = 'iron-collapse')

    star2 = star(mass = 2.4, binary = True)

    star3 = star(mass = 8.5)

    print(star1)
    print(type(star1))
    print(star2)
    print(star3)

    # Test getters

    print(star1.getCcore(), star1.getFmass())
    print(star2.getBinary())
    print(star3.getTermination())

    # Test setters

    star1.setCcore(1.15)
    print(star1)

    star3.setBinary(True)
    print(star3)

    print(star1.__dict__)

if __name__ == '__main__':
    debug()
