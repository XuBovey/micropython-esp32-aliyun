from simple import MQTTClient
from machine import Pin,Timer
import network
import time
import re

#根据实际情况填写
productkey = 'a1SoaRN1uSU'
device_name = 'skids_test'
#devicesecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'

clientId = '12345'
paswd = 'AA5B7973A3F7138B222015C21602D16A7AE6F607'

# 服务器 华东2（上海）
SERVER = productkey +'.iot-as-mqtt.cn-shanghai.aliyuncs.com'  #MQTT Server
CLIENT_ID = clientId + "|securemode=3,signmethod=hmacsha1|"   #设备ID
PORT=1883
username= device_name + '&' + productkey
password= paswd
 
publish_TOPIC = '/sys/'+productkey+'/'+ device_name +'/thing/event/property/post'
subscribe_TOPIC ='/sys/'+productkey+'/'+ device_name +'/thing/service/property/set'

client=None

led = Pin(15, Pin.OUT, value=0) #led

def Dataupload(timer):
    try:
        print("hello")
        # client.publish(topic=publish_TOPIC,msg= message, retain=False, qos=0)
        
    except Exception as ex_results2:
        print('exception2',ex_results2)
        timer.deinit()
        
    
def sub_cb(topic, msg):
    dic=msg.decode()
    print(dic)
    refind(dic)
    
def refind(dicc):
    match0=re.search(r"{\"powerstate\":(.*?)}",dicc)#获取灯的开关信息
    if match0:
        value0=eval(match0.group(1))
        led.value(value0)

try:
    client = MQTTClient(CLIENT_ID, SERVER,PORT,username,password,60)
    print(client)
    client.set_callback(sub_cb)
    client.connect() #connect mqtt
    client.subscribe(subscribe_TOPIC)
    print("Connected to %s, subscribed to %s topic" % (SERVER, subscribe_TOPIC))
    timer=Timer(0)
    timer.init(mode=Timer.PERIODIC, period=5000,callback=Dataupload)
    while True:
        client.wait_msg()
        
except Exception as ex_results:
    print('exception1',ex_results)
    
finally:
    if(client is not None):
        client.disconnect()
