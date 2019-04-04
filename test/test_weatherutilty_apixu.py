import unittest, sys, os, json
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')
from weatherutility_apixu import WeatherUtilityApixu

class TestWeatherUtilityAPIXU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up class')
        cls._apikey = os.environ['APIKEY']
        cls._json_cc = 'test_apixu_current.json'
        cls._json_history = 'test_apixu_history.json'
        cls._json_forecast = 'test_apixu_forecast_2day.json'

    def test_parseCurrentConditionsPrecipitation(self):
        with open(TestWeatherUtilityAPIXU._json_cc, 'r') as f:
            json_data = json.load(f)
        utility = WeatherUtilityApixu(TestWeatherUtilityAPIXU._apikey)
        results = utility.parseCurrentConditionsPrecipitation(json_data)
        self.assertEqual(results, 0.0)

    def test_parseHistoryPrecipitation(self):
        with open(TestWeatherUtilityAPIXU._json_history, 'r') as f:
            json_data = json.load(f)
        utility = WeatherUtilityApixu(TestWeatherUtilityAPIXU._apikey)
        results = utility.parseHistoryPrecipitation(json_data)
        self.assertEqual(results, 0.35)

    def test_parseNextDayForecastPrecipitation(self):
        with open(TestWeatherUtilityAPIXU._json_forecast, 'r') as f:
            json_data = json.load(f)
        utility = WeatherUtilityApixu(TestWeatherUtilityAPIXU._apikey)
        results = utility.parseNextDayForecastPrecipitation(json_data)
        self.assertIsNotNone(results)

    def test_shouldOverrideFromForecastRain(self):
        today = .085
        tomorrow = .03
        threshold = .1
        multiplierOne = 1
        multiplierTwo = .5

        utility = WeatherUtilityApixu(TestWeatherUtilityAPIXU._apikey)
        results = utility.shouldOverrideFromForecastRain(today, tomorrow, multiplierOne, multiplierTwo, threshold)
        self.assertEqual(True, results)

    @classmethod
    def tearDownClass(cls):
        print('Tearing down class')

if __name__ == '__main__':
    unittest.main()