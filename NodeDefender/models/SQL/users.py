from ... import db, bcrypt
from datetime import datetime

class UserModel(db.Model):
    '''
    Table of Users

    Users is a part of a Group
    Logins are logged with List- Relation(LoginLogModel)
    Private messages are stored in List- relation(UserMessageModel)

    Password is encrypted
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(191), unique=True)
    password = db.Column(db.String(191))
    
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime)
    registered_at = db.Column(db.DateTime)
    
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
   
    technician = db.Column(db.Boolean)
    administrator = db.Column(db.Boolean)
    superuser = db.Column(db.Boolean)
    
    messages = db.relationship('MessageModel', backref='user',
                              cascade='save-update, merge, delete')

    def __init__(self, email):
        self.email = email
        self.firstname = None
        self.lastname = None
        self.password = None
        self.active = False
        self.confirmed_at = None
        self.registered_at = datetime.now()

        self.technician = False
        self.administrator = False
        self.superuser = False

    def to_json(self):
        return {'firstName': self.firstname,
                'lastName' : self.lastname,
                'email' : self.email,
               }

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def verify_password(self, password):
        if bcrypt.check_password_hash(self.password, password):
            return True
        else:
            return False
    

    def has_role(self, role):
        try:
            return getattr(self, role.lower())
        except AttributeError:
            print(role)