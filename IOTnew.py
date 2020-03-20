import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from sklearn import linear_model
from sklearn import preprocessing
import pandas as pd
import blynklib

pin=27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.IN) #sound
GPIO.setup(3,GPIO.OUT) #sound/output
GPIO.setup(27,GPIO.IN) #temperature DHT11
GPIO.setup(17,GPIO.IN) #gas
GPIO.setup(22,GPIO.IN) #raindrop
GPIO.setup(4,GPIO.OUT) #buzzer
sensor = Adafruit_DHT.DHT11
df=pd.read_csv("Weather3.csv")
X = df[['HUMIDITY', 'TEMPERATURE']]
y = df['WEATHER FORECAST']

reg = linear_model.LinearRegression()
reg.fit(df[['HUMIDITY', 'TEMPERATURE']], df['WEATHER FORECAST'])
BLYNK_AUTH='IpOfhJ5EehVIZb86tB7EYXFA_MsennTg'
blynk=blynklib.Blynk(BLYNK_AUTH)

while(True):
        blynk.run()
	x=GPIO.input(2)
	if x==1:
		GPIO.output(3,GPIO.LOW)
		print("Sound detected")
		blynk.notify("Too much sound in the zone!!!")
	else:
		print('No sound')

        x=GPIO.input(17)
        if x==0 :
                blynk.notify("Fire Alert!!!")
                print("Fire Alert!!!")
                GPIO.output(4,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(4,GPIO.LOW)
        else :
                print("Safe ")

        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!

        z=GPIO.input(22)
        if not z.is_active:
                blynk.notify("It's raining!")
                print("It's raining!")
        else :
                print("It's not raining")

        if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                fahrenheit=float((temperature*1.8)+32)  #formula
                X = df[['HUMIDITY', 'TEMPERATURE']]
                y = df['WEATHER FORECAST']
                le = preprocessing.LabelEncoder()#making LabelEncoder function varibale
                df = df.apply(le.fit_transform)#this is used to convert string values into integer values
                reg = linear_model.LinearRegression()
                reg.fit(df[['HUMIDITY', 'TEMPERATURE']], df['WEATHER FORECAST'])
                print("WEATHER REPORT")
                print(reg.predict([[humidity,fahrenheit]]))


                if(float(reg.predict([[humidity,fahrenheit]]))>=0 and float(reg.predict([[humidity,fahrenheit]]))<1):
                        try:
                                blynk.notify('Light rain')
                                print("Light rain")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif(float(reg.predict([[humidity,fahrenheit]]))>=1 and float(reg.predict([[humidity,fahrenheit]]))<2):
                        try:                    
                                blynk.notify('Broken Clouds')
                                print("Broken Clouds")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]]))>=2 and float(reg.predict([[humidity, fahrenheit]])) < 3):
                        try:
                                blynk.notify('Proximity Shower Rain')
                                print("Proximity Shower Rain ")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]]))>=3 and float(reg.predict([[humidity, fahrenheit]])) < 4):
                        try:
                                blynk.notify('Sky is Clear')
                                print("Sky is Clear")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]]))>=4 and float(reg.predict([[humidity, fahrenheit]])) < 5):
                        try:
                                blynk.notify('Scattered Clouds')
                                print("Scattered Clouds")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 5 and float(reg.predict([[humidity, fahrenheit]])) < 6):
                        try:
                                blynk.notify('Few Clouds')
                                print("Few Clouds")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 6 and float(reg.predict([[humidity, fahrenheit]])) < 7):
                        try:
                                blynk.notify('Squalls')
                                print("Squalls")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 7 and float(reg.predict([[humidity, fahrenheit]])) < 8):
                        try:
                                blynk.notify('Overcast Clouds')
                                print("Overcast clouds ")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 8 and float(reg.predict([[humidity, fahrenheit]])) < 9):
                        try:        
				blynk.notify('Heavy Snow')
                                print("Heavy Snow")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 9 and float(reg.predict([[humidity, fahrenheit]])) < 10):
                        try:
                                blynk.notify('Mist')
                                print("Mist")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 10 and float(reg.predict([[humidity, fahrenheit]])) < 11):
                        try:
                                blynk.notify('Haze')
                                print("Haze")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                elif (float(reg.predict([[humidity, fahrenheit]])) >= 11 and float(reg.predict([[humidity, fahrenheit]])) < 12):
                        try:
                                blynk.notify('Fog')
                                print("Fog")
                        except KeyboardInterrupt:
                                print("Exit")
                                GPIO.cleanup()
                else:
                        print("not predicted")
        else:
                print('Failed to get reading. Try again!')
        time.sleep(10)
        break
