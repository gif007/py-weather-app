#!/bin/python
# weatheroffice interface

import sys
import random
from classes.Weather import WeatherPage
from functions import *


# Temperatures and weather summaries for various regions (7-day):
LUNENBURG_XML = 'https://weather.gc.ca/rss/city/ns-21_e.xml'

if __name__ == '__main__':
    regions = csv_reader('regions.csv')
    region = regions[sys.argv[1].upper()]
    data = WeatherPage(region)
    data.get_data()
    data.produce_output()
    print_lines(data.render_output())