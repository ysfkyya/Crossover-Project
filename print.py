from unittest import result
import psutil
import json


class Metric():

    def __init__(self):
        p = psutil.Process(1)
        self.cpu = p.cpu_percent()
        self.memory =psutil.virtual_memory()[2]
    
    def as_dict(self):
        x = {'cpu' : self.cpu, 'RAMmemory' : self.memory }
        return json.dumps(x)
    
result = Metric()
print(result.as_dict())  

#Sanal makinenin CPU ve RAMmemory bilgileri alinir.



