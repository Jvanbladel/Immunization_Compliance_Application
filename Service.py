
class patientHistory():
    def __init__(self, data):
        self.ImmunizationServiceList = data[0]
        pass

class ImmunizationService():
    def __init__(self, data):
        self.Immunization = data[0]
        pass

class Immunization():
    def __init__(self, data):
        self.type = data[0]
        pass
