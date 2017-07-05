from ... import db
from datetime import datetime
from ...iCPE.zwave import commandclass

class HeatModel(db.Model):
    __tablename__ = 'heat'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)

    def __init__(self, heat, date = datetime.now()):
        self.high = heat
        self.low = heat
        self.average = heat
        self.date = date

class PowerModel(db.Model):
    __tablename__ = 'power'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

    high = db.Column(db.Float)
    low = db.Column(db.Float)
    average = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, power = 0.0, date = datetime.now()):
        self.high = power
        self.low = power
        self.average = power
        self.total = power
        self.date = date

    def to_json(self):
        node = self.node.name if self.node else None
        icpe = self.icpe.macaddr if self.icpe else None
        sensor = self.sensor.sensorid if self.sensor else None
        
        return {'high' : self.high, 'low' : self.low, 'average' : self.average,
                'node' : node, 'icpe' : icpe, 'sensor' : sensor,
                'date' : str(self.date)}

class EventModel(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    icpe_id = db.Column(db.Integer, db.ForeignKey('icpe.id'))
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))
    commandclass_id = db.Column(db.Integer, db.ForeignKey('commandclass.id'))
    commandclasstype_id = db.Column(db.Integer,
                                    db.ForeignKey('commandclasstype.id'))

    value = db.Column(db.String(16))

    critical = db.Column(db.Boolean)
    normal = db.Column(db.Boolean)

    def __init__(self, value, date = None):
        self.value = value
        self.date = date if date else datetime.now()

    def to_json(self):
        if self.commandclasstype:
            name = self.commandclasstype.name
            icon = eval('commandclass.'+self.commandclass.name+'.'+\
                        self.commandclasstype.name+'.Icon')(self.value)
        elif self.commandclass:
            name = self.commandclass.name
            icon = eval('commandclass.'+self.commandclass.name+'.Icon')\
                        (self.value)
        else:
            name = 'unkown'
            icon = 'fa fa-question'

        return {'iCPE' : self.icpe.macaddr, 'sensor' : self.sensor.productname, 'node' :
                self.icpe.node.name, 'value' : self.value,\
                'date' : str(self.date), 'icon' : icon,\
                'name' : name}