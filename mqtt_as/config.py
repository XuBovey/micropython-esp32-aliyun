# config.py Local configuration for mqtt_as demo programs.
from sys import platform
from mqtt_as import config

productkey = 'a1SoaRN1uSU'
device_name = 'skids_test'
devicesecret = '*****************************'

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

# config['server'] = '192.168.0.10'  # Change to suit
# config['server'] = 'iot.eclipse.org'
config['server'] = SERVER
config['port'] = PORT
config['user'] = username
config['password'] = password
config['client_id'] = CLIENT_ID

# Not needed if you're only using ESP8266
config['ssid'] = 'setting...'
config['wifi_pw'] = 'loading...@'


# For demos ensure the same calling convention for LED's on all platforms.
# ESP8266 Feather Huzzah reference board has active low LED's on pins 0 and 2.
# ESP32 is assumed to have user supplied active low LED's on same pins.
# Call with blue_led(True) to light

if platform == 'esp8266' or platform == 'esp32' or platform == 'esp32_LoBo':
    from machine import Pin
    def ledfunc(pin):
        pin = pin
        def func(v):
            pin(not v)  # Active low on ESP8266
        return func
    wifi_led = ledfunc(Pin(15, Pin.OUT, value = 0))  # Red LED for WiFi fail/not ready yet
    blue_led = ledfunc(Pin(17, Pin.OUT, value = 1))  # Message received
elif platform == 'pyboard':
    from pyb import LED
    def ledfunc(led, init):
        led = led
        led.on() if init else led.off()
        def func(v):
            led.on() if v else led.off()
        return func
    wifi_led = ledfunc(LED(1), 1)
    blue_led = ledfunc(LED(3), 0)
