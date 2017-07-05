from ... import db
from datetime import datetime
from .nodes import LocationModel

user_list = db.Table('user_list',
                     db.Column('group_id', db.Integer,
                               db.ForeignKey('group.id')),
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('user.id'))
                    )
node_list = db.Table('node_list',
                     db.Column('group_id', db.Integer,
                               db.ForeignKey('group.id')),
                     db.Column('node_id', db.Integer,
                               db.ForeignKey('node.id'))
                    )

mqtt_list = db.Table('mqtt_list',
                     db.Column('group_id', db.Integer,
                               db.ForeignKey('group.id')),
                     db.Column('mqtt_id', db.Integer,
                               db.ForeignKey('mqtt.id'))
                    )

class GroupModel(db.Model):
    '''
    Representing one group containing iCPEs and Users
    '''
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    description = db.Column(db.String(250))
    created_on = db.Column(db.DateTime)
    users = db.relationship('UserModel', secondary=user_list,
                            backref=db.backref('groups', lazy='dynamic'))
    mqtts = db.relationship('MQTTModel', secondary=mqtt_list,
                            backref=db.backref('groups', lazy='dynamic'))
    nodes = db.relationship('NodeModel', secondary=node_list,
                            backref=db.backref('groups', lazy='dynamic'))
    location = db.relationship('LocationModel', uselist=False,
                               backref='group')

    messages = db.relationship('MessageModel', backref='group',
                               cascade='save-update, merge, delete')

    def __init__(self, name, email, description):
        self.name = name
        self.email = email
        self.description = str(description)
        self.created_on = datetime.now()
    
    def to_json(self):
        return {'name' : self.name, 'email' : self.email, 'created' :
                str(self.created_on), 'description' : self.description,
                'users' : [user.email for user in self.users],
                'nodes' : [node.name for node in self.nodes]}