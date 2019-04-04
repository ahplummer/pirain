from pylogger import projectLogger
import os
from weatherutility_apixu import WeatherUtilityApixu
from relayinterface import executeRelay

if __name__ == "__main__":
    if 'APIKEY' not in os.environ or 'ZIPCODE' not in os.environ:
        projectLogger().error('No APIKEY or ZIPCODE envvar, exiting')
        exit(1)
    if 'FUTURETHRESHOLD' in os.environ:
        futureThreshold = os.environ['FUTURETHRESHOLD']
    else:
        futureThreshold = .1
    if 'PASTTHRESHOLD' in os.environ:
        pastThreshold = os.environ['PASTTHRESHOLD']
    else:
        pastThreshold=.1
    if 'MULTIPLYIERONE' in os.environ:
        multiplierOne = os.environ['MULTIPLIERONE']
    else:
        multiplierOne = 1
    if 'MULTIPLIERTWO' in os.environ:
        multiplierTwo = os.environ['MULTIPLIERTWO']
    else:
        multiplierTwo = .5

    utility = WeatherUtilityApixu(os.environ['APIKEY'])
    shouldOverride = utility.computeSprinklerOverride(
        os.environ['ZIPCODE'],pastThreshold, futureThreshold, multiplierOne, multiplierTwo)
    projectLogger().info('Override sprinkler system for zip code %s: %s', os.environ['ZIPCODE'], shouldOverride)

    result, error = executeRelay(shouldOverride)
    projectLogger().info("Executing Sprinkler rain override to " + str(shouldOverride) + (
        "." if result == True else " but had error: (" + error + ")"))
