from ...models.manage import sensor as SensorSQL
from ...models.redis import sensor as SensorRedis
from . import redisconn, commandclass
from .. import mqtt, zwave
from ... import celery
from datetime import datetime
from .. import logger
from ..decorators import ParsePayload

@ParsePayload
def Verify(topic, payload, mqttsrc = None):
    if len(SensorRedis.Get(topic.macaddr, topic.sensorid)):
        return True
    
    if SensorRedis.Load(topic.macaddr, topic.sensorid):
        return True

    Add(topic, payload)
    return True

def Add(topic, payload):
    zinfo = zwave.db.SensorInfo(payload.vid, payload.pid)
    SensorSQL.Create(topic.macaddr, topic.sensorid, zinfo)
    SensorRedis.Load(topic.macaddr, topic.sensorid)
    return True

def Update(macaddr, sensorid):
    sensor = SensorSQL.Get(macaddr, sensorid)
    if not sensor.commandclasses:
        mqtt.sensor.Query(macaddr, sensorid)
        return True
    for cc in sensor.commandclasses:
        commandclass.Update(cc)
    return True

@celery.task
def Load(icpe = None):
    for sensor in SensorSQL.List(icpe):
        SensorRedis.Load(sensor)
    return True
