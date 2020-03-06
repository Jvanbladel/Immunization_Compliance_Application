from ICA_super import *
from Patients import *




class ImmunizationScreen(icaSCREENS):
    '''
    class holds immunization records for both patients.

    both main menu and med info will link to here
    '''


    patientMRN = [] # append MRNs to here. Helps prevent multiple of same patient screen

    def __init__(self, patient):



