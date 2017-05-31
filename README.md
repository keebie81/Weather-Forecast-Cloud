# Weather-Forecast-Cloud

![Clouds](clouds.png)

This project is a cloud that will check the weather forecast using the Yahoo Weather API. If the forecasted weather for the next day is more than 10% hotter it will light up red. If the weather forecast is more than 10% colder it will light up gold. If neither condition is met it will stay blue. It also will blink if rain or snow is in the forecast.

A guide on how to build this is available at Instructables https://www.instructables.com/id/Weather-Forecast-Cloud/

The project was originally designed for NeoPixels. The cloud_neopixel.py file has the code for that. But if you have a Raspberry Pi Sense Hat you can use cloud_sensehat.  If using a Pimoroni Blinkt or Unicorn HAT/PHAT you can use cloud_blinkt_unicorn.py

Depending on your project you may need to adjust the brightness levels of the LED's
