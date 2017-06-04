import json, requests
import time
 
# Uncomment if using Unicorn hat or phat
#import unicornhat as pixel

# Uncomment if using Blinkt
import blinkt as pixel


# Flickers the cloud blue
def blueFlicker():
    pixel.set_all(0, 0, 90)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(0, 0, 70)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(0, 0, 50)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(0, 0, 30)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(0, 0, 50)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(0, 0, 70)
    pixel.show()
    time.sleep(.25)


# Flickers the cloud red
def redFlicker():
    pixel.set_all(90, 0, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(70, 0, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(50, 0, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(30, 0, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(50, 0, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(70, 0, 0)
    pixel.show()
    time.sleep(.25)

# Flickers the cloud gold
def goldFlicker():
    pixel.set_all(115, 75, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(105, 65, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(95, 55, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(85, 45, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(95, 55, 0)
    pixel.show()
    time.sleep(.25)
    pixel.set_all(105, 65, 0)
    pixel.show()
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
            pixel.set_all(90, 0, 0)  # Solid Red Cloud
        else:
            redFlicker()

    # Check if cloud should be gold, we will let red always overide gold
    if gold_cloud == 1 and red_cloud == 0:
        if flicker == 0:
            pixel.set_all(115, 75, 0)  # Solid Gold Cloud
        else:
            goldFlicker()


    # If cloud is not gold or red it should then be blue
    if gold_cloud == 0 and red_cloud == 0:
        if flicker == 0:
            pixel.set_all(0, 0, 90)  # Solid Blue Cloud
        else:
            blueFlicker()
    
    pixel.show()


  

