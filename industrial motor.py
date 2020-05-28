import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "rgjd96"
deviceType = "raspberrypi"
deviceId = "654321"
authMethod = "token"
authToken = "17481a04m7"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        temp=random.randint(20, 90)
        #print(temp)
        hum =random.randint(30, 85)
        #print(hum)
        vib =random.randint (20, 50)
        #Send Temperature, Humidity, &Vibration to IBM Watson
        data = { 'Temprature' : temp, 'Humidity' : hum, 'Vibration': vib }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "Vibration = %s m/s2" % vib, "to IBM Watson")
        

        success = deviceCli.publishEvent("Wheater", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

