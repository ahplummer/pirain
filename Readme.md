# pirain

## Purpose
This code is intended for use with a RaspBerryPI with a GPIO relay switch.

It interfaces into the Rainbird/Hunter brand of sprinkler controller, specifically
into the 'rain gauge sensor' connection.

The way this works is that every X minutes/X hours, depending on your desire, this
script will call out to a weather API for a given zip code.  The following data is 
collected:
* Yesterday's precipitation
* Current Conditions precipitation
* Tomorrow's precipitation

Together with some thresholding rules, will determine whether or not your sprinkler's
schedule needs to be overridden or not.

This saves water, and is a geekery thing to do.

## Requirements
* RaspberryPi
* [RaspberryPi Relay Expansion Board](https://www.amazon.com/gp/product/B01G05KLIE/ref=oh_aui_search_asin_title?ie=UTF8&psc=1)
* Hunter/Rainbird sprinkler controller with moisture sensor override
* Python 3 on your RPi
* free API key at [https://api.apixu.com](https://api.apixu.com)

## Installation
* clone this repo onto the RPi
* Optionally, create a virtual environment (recommended)
* do a `pip install -r requirements`
* test the relay and python installation by:
    * execute `python drive_relayCLOSE.py` and `python drive_relayOPEN.py`
    * also, feel free to execute `python relayinterface.py` directly
* Set envvars with ZIPCODE to use, and APIKEY.
    * If you created a virtualenv, feel free to write the following at the end
    of your <virt directory>\bin\activate file:
    ```
    export APIKEY=<your key>
    export ZIPCODE=<your zip>
    ```  
    NOTE: You'll need to re-activate your virtualenv, if you've modified the activate script.
* Execute `python driver.py`
* Create a cronscript:
```
#!/bin/bash
cd <pirain directory>
. <virtenv>/bin/activate
date >> <pirain directory>/output.txt
python driver.py >> <pirain directory>/output.txt
```
* Set it up on a cron:
    * `sudo crontab -e`, entry will look like: 
    
    ```*/60 * * * * pi <pirain directory>/crondriver.sh```
    
    
# Gotcha's / TODO's
* RPi.GPIO won't compile on your Mac. Don't try.
* Tests aren't fully covered, but the parsing routines are.
* Code is as brittle as the API. 
* Plan on pulling up some of the logic into the abstract class, but will do so
later when another supported API is leveraged.  Will feature-toggle the API used.
