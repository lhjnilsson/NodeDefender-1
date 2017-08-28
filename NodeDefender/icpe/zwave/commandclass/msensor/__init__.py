from NodeDefender.icpe.zwave.commandclass.msensor import AirTemperature

classtypes = {'1' : 'AirTemperature', '0x01' : 'AirTemperature',
         '01' : 'AirTemperature'}
info = {'number' : '31', 'name' : 'msensor', 'types' : True}
fields = None

def event(payload):
    try:
        return eval(classtypes[payload['mtype']] + '.event')(payload)
    except KeyError as e:
        print(str(e))

def icon(value):
    return None
