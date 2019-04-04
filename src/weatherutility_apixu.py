import requests, json
from pylogger import projectLogger
from weatherutility_abstract import WeatherUtilityAbstract
from datetime import datetime, timedelta, date

ccURL="https://api.apixu.com/v1/current.json?key=<APIKEY>&q=<ZIPCODE>"
forecastURL="https://api.apixu.com/v1/forecast.json?key=<APIKEY>&q=<ZIPCODE>&dt=<YYYY-MM-DD>" #(tomorrow)
historyURL="https://api.apixu.com/v1/history.json?key=<APIKEY>&q=<ZIPCODE>&dt=<YYYY-MM-DD>" #(yesterday)

class WeatherUtilityApixu(WeatherUtilityAbstract):
    def __init__(self, apikey):
        super().__init__(apikey)

    def parseCurrentConditionsPrecipitation(self, json_data):
        results = None
        try:
            results = json_data['current']['precip_in']
        except:
            pass
        return results

    def parseHistoryPrecipitation(self, json_data):
        results = None
        try:
            results = json_data['forecast']['forecastday'][0]['day']['totalprecip_in']
        except:
            pass
        return results

    def parseNextDayForecastPrecipitation(self, json_data):
        results = None
        days = json_data['forecast']['forecastday']
        for day in days:
            results = day['day']['totalprecip_in']
            break
        return results

    def shouldOverrideFromPastRain(self, historyResults, threshold):
        results = False
        if historyResults >= threshold:
            results = True
        return results

    def shouldOverrideFromForecastRain(self, currentResults, forecastResults, firstDayMultiplier, secondDayMultiplier, forecastThreshold):
        results = False
        if ((firstDayMultiplier * currentResults) + (secondDayMultiplier * forecastResults)) >= forecastThreshold:
            results = True
        return results


    def getJSONHistory(self, zipcode):
        yesterday = date.today() - timedelta(1)
        dt = yesterday.strftime('%Y-%m-%d')
        url = historyURL.replace("<APIKEY>", self._apikey).replace("<ZIPCODE>", zipcode).replace("<YYYY-MM-DD>", dt)
        projectLogger().debug('Attempting to retrieve: %s', url)

        resp = requests.get(url)
        jsonload = json.loads(resp.text)
        return jsonload

    def getJSONCurrentConditions(self, zipcode):
        url = ccURL.replace("<APIKEY>", self._apikey).replace("<ZIPCODE>", zipcode)
        projectLogger().debug('Attempting to retrieve: %s', url)
        resp = requests.get(url)
        jsonload = json.loads(resp.text)
        return jsonload

    def getJSONForecast(self, zipcode):
        tomorrow = date.today() + timedelta(1)
        dt = tomorrow.strftime('%Y-%m-%d')
        url = forecastURL.replace("<APIKEY>", self._apikey).replace("<ZIPCODE>", zipcode).replace("<YYYY-MM-DD>", dt)
        projectLogger().debug('Attempting to retrieve: %s', url)
        resp = requests.get(url)
        jsonload = json.loads(resp.text)
        return jsonload

    def computeSprinklerOverride(self, zipcode, pastThreshold, futureThreshold, multiplierOne, multiplierTwo):
        historyJSON = self.getJSONHistory(zipcode)
        historyResults = self.parseHistoryPrecipitation(historyJSON)
        projectLogger().debug('Yesterday precip is: %s', historyResults)
        ccJSON = self.getJSONCurrentConditions(zipcode)
        ccResults = self.parseCurrentConditionsPrecipitation(ccJSON)
        projectLogger().debug('Current Conditions precip is: %s', ccResults)
        forecastJSON = self.getJSONForecast(zipcode)
        forecastResults = self.parseNextDayForecastPrecipitation(forecastJSON)
        projectLogger().debug('Forecast for tomorrow is: %s', forecastResults)

        if not self.shouldOverrideFromPastRain(historyResults, pastThreshold):
            if not self.shouldOverrideFromForecastRain(ccResults, forecastResults, multiplierOne, multiplierTwo,
                                                          futureThreshold):
                projectLogger().debug('Override Sprinkler indicator: False, (checked past, current, and future')
                result = False
            else:
                projectLogger().debug(
                    'Override Sprinkler indicator: True, (due to rainfall current/forecast for tomorrow)')
                result = True

        else:
            projectLogger().debug('Override Sprinkler indicator: True, (due to rainfall yesterday)')
            result = True

        return result