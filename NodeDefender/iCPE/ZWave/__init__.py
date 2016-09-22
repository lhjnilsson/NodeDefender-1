from inspect import isclass
from .commandclasses import *
from .genericclasses import *
from .basicclasses import *

class _ZWaveNode:
    def __init__(self, mac, nodeid, outMQTTQueue, outSocketQueue, **kwargs):
        self.mac = str(mac)
        self.nodeid = str(nodeid)
        self.MQTT = outMQTTQueue
        self.WS = outSocketQueue
        self.WebForm = {} # Holds alias, name and such
        self.WebForm['fields'] = []
        self.WebForm['nodeid'] = self.nodeid
        self.WebForm['mac'] = self.mac
        for key, value in kwargs.items():
            self.WebForm[key] = value
            print(key, value)
            self.__dict__[key] = value
        super().__init__()

    def __call__(self, topic, payload):
        try:
            getattr(self, 'c'+payload['class'])(topic, payload)
        except AttributeError:
            print('Unknown class', 'c'+payload['class'])
        except KeyError:
            print('Class not in payload?', payload)

    def Form(self):
        for field in self.WebForm['fields']:
            field['value'] = eval('self.' +field['class'])
        return self.WebForm

def ZWaveNode(mac, nodeid, *classes):
    supported = []
    unsupported = []
    for cls in classes:
        try:
            eval('c' + cls)
            supported.append(cls)
        except NameError:
            unsupported.append(cls)
    class _NewClass(_ZWaveNode, *[eval('c'+x) for x in supported]):
        pass
    return _NewClass, unsupported