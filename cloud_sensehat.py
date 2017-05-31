import json, requests
import time

from sense_hat import SenseHat
sense = SenseHat()

# Flickers the cloud blue
def blueFlicker():
    sense.clear(0, 0, 90)
    time.sleep(.25)
    sense.clear(0, 0, 70)
    time.sleep(.25)
    sense.clear(0, 0, 50)
    time.sleep(.25)
    sense.clear(0, 0, 30)
    time.sleep(.25)
    sense.clear(0, 0, 50)
    time.sleep(.25)
    sense.clear(0, 0, 70)
    time.sleep(.25)

# Flickers the cloud red
def redFlicker():
    sense.clear(90, 0, 0)
    time.sleep(.25)
    sense.clear(70, 0, 0)
    time.sleep(.25)
    sense.clear(50, 0, 0)
    time.sleep(.25)
    sense.clear(30, 0, 0)
    time.sleep(.25)
    sense.clear(50, 0, 0)
    time.sleep(.25)
    sense.clear(70, 0, 0)
    time.sleep(.25)

# Flickers the cloud gold
def goldFlicker():
    sense.clear(115, 75, 0)
    time.sleep(.25)
    sense.clear(105, 65, 0)
    time.sleep(.25)
    sense.clear(95, 55, 0)
    time.sleep(.25)
    sense.clear(85, 45, 0)
    time.sleep(.25)
    sense.clear(95, 55, 0)
    time.sleep(.25)
    sense.clear(105, 65, 0)
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
        gold_flamecloud = 1
    else:
        gold_cloud = 0

    # Check if cloud should be red
    if red_cloud == 1:
        if flicker == 0:
            sense.clear(90, 0, 0)  # Solid Red Cloud
        else:
            redFlicker()

    # Check if cloud should be gold, we will let red always overide gold
    if gold_cloud == 1 and red_cloud == 0:
        if flicker == 0:
            sense.clear(115, 75, 0)  # Solid Gold Cloud
        else:
            goldFlicker()


    # If cloud is not gold or red it should then be blue
    if gold_cloud == 0 and red_cloud == 0:
        if flicker == 0:
            sense.clear(0, 0, 90)  # Solid Blue Cloud
        else:
            blueFlicker()


  

