import json, requests
import time

from neopixel import *

# LED strip configuration:
LED_COUNT   = 19      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
# Intialize the library (must be called once before other functions).
strip.begin()

# Sets the stip all one color
def colorAll(strip, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()

# Flickers the cloud blue
def blueFlicker():
    colorAll(strip, Color(0, 0, 90))
    time.sleep(.25)
    colorAll(strip, Color(0, 0, 70))
    time.sleep(.25)
    colorAll(strip, Color(0, 0, 50))
    time.sleep(.25)
    colorAll(strip, Color(0, 0, 30))
    time.sleep(.25)
    colorAll(strip, Color(0, 0, 50))
    time.sleep(.25)
    colorAll(strip, Color(0, 0, 70))
    time.sleep(.25)

# Flickers the cloud red
def redFlicker():
    colorAll(strip, Color(0, 90, 0))
    time.sleep(.25)
    colorAll(strip, Color(0, 70, 0))
    time.sleep(.25)
    colorAll(strip, Color(0, 50, 0))
    time.sleep(.25)
    colorAll(strip, Color(0, 30, 0))
    time.sleep(.25)
    colorAll(strip, Color(0, 50, 0))
    time.sleep(.25)
    colorAll(strip, Color(0, 70, 0))
    time.sleep(.25)

# Flickers the cloud gold
def goldFlicker():
    colorAll(strip, Color(75, 115, 0))
    time.sleep(.25)
    colorAll(strip, Color(65, 105, 0))
    time.sleep(.25)
    colorAll(strip, Color(55, 95, 0))
    time.sleep(.25)
    colorAll(strip, Color(45, 85, 0))
    time.sleep(.25)
    colorAll(strip, Color(55, 95, 0))
    time.sleep(.25)
    colorAll(strip, Color(60, 105, 0))
    time.sleep(.25)

# Gets weather forecast
def getWeather():
    # Change to your location
    url = requests.get('https://query.yahooapis.com/v1/public/yql?q=select item.forecast from weather.forecast where woeid in (select woeid from geo.places(1) where text="sheboygan, wi")&format=json')
    global weather
    weather = json.loads(url.text)

    # Gets todays High and Low
    global today_high
    today_high = (weather['query']['results']['channel'][0]['item']['forecast']['high'])
    global today_low
    today_low = (weather['query']['results']['channel'][0]['item']['forecast']['low'])
    
    # Gets tomorrows High and Low
    global next_high
    next_high = (weather['query']['results']['channel'][1]['item']['forecast']['high'])
    global next_low
    next_low = (weather['query']['results']['channel'][1]['item']['forecast']['low'])

    # Get weather code of tomorrows forecast
    global next_forecast 
    next_forecast = (weather['query']['results']['channel'][1]['item']['forecast']['code'])

    print "updated weather"
    print "todays high is", int(today_high)
    print "todays low is", int(today_low)
    print "tomorrows code is", int(next_forecast)
    print "next high is", int(next_high)
    print "next low is", int(next_low)
    
    

getWeather()
timer = time.time()

while True:
    # Update weather once an hr
    if time.time() - timer > 3600:
        getWeather()
        timer = time.time()

    # Check forecast codes to make sure none are rain or snow https://developer.yahoo.com/weather/documentation.html
    if next_forecast == "24" or next_forecast == "26" or next_forecast == "27" or next_forecast == "28" or next_forecast == "29" or next_forecast == "30" or next_forecast == "31" or next_forecast == "32" or next_forecast == "33" or next_forecast == "34" or next_forecast == "36" or next_forecast == "44":
        flicker = 0
    else:
        flicker = 1
    
    # Adds 10% to todays high than checks to see if that is less than tomorrows high.
    # If tomorrow is more than 10% hotter cloud should be red
    if ((int(today_high)*0.1) +int(today_high)) < int(next_high):
        red_cloud = 1
    else:
        red_cloud = 0

    # Subtracts 10% from todays low than checks to see if that is greater than tomorrows low.
    # If tomorrow is more than 10% colder the cloud should be gold
    if (int(today_low) -(int(today_low)*0.1)) > int(next_low):
        gold_cloud = 1
    else:
        gold_cloud = 0

    # Check if cloud should be red
    if red_cloud == 1:
        if flicker == 0:
            colorAll(strip, Color(0, 90, 0))  # Solid Red Cloud
        else:
            redFlicker()

    # Check if cloud should be gold, we will let red always overide gold
    if gold_cloud == 1 and red_cloud == 0:
        if flicker == 0:
            colorAll(strip, Color(75, 115, 0))  # Solid Gold Cloud
        else:
            goldFlicker()


    # If cloud is not gold or red it should then be blue
    if gold_cloud == 0 and red_cloud == 0:
        if flicker == 0:
            colorAll(strip, Color(0, 0, 90))  # Solid Blue Cloud
        else:
            blueFlicker()


  
