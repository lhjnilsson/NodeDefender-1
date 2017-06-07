'''
Copyright (c) 2016 Connection Technology Systems Northern Europe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE
SOFTWARE.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_socketio import SocketIO
from flask_moment import Moment
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.gevent import GeventScheduler
from .factory import CreateApp, CreateLogging, CreateCelery, Serializer
from redis import ConnectionPool
from redlock import RedLock
from gevent import monkey
monkey.patch_all()

# Initialize the Flask- Application
app = CreateApp()

# Setup logging
logger, loggHandler = CreateLogging(app)

# Initialize Api
api = Api(app)

# Config-file 

RedisPool = ConnectionPool()

# Initialize SocketIO
try:
    socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URI'],
                    async_mode='gevent')
except KeyError:
    socketio = SocketIO(app, async_mode='gevent')

# Initialize SQLAlchemy for Database
db = SQLAlchemy(app)
logger.info('Database started')

# Initialize Celery
celery = CreateCelery(app)

# For the Authentication
LoginMan = LoginManager()
LoginMan.init_app(app)
LoginMan.login_view = 'AuthView.Login'
LoginMan.login_message_category = "info"

bcrypt = Bcrypt(app)

serializer = Serializer(app)

# Report that startup is successfull
logger.info('NodeDefender Succesfully started')

# MQTT
from . import conn

# Frontend
moment = Moment(app)
from .models import SQL, redis
from . import frontend, mail
