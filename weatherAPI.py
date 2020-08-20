#!/bin/python
# weatheroffice interface

import requests
import bs4
import sys
import random
import datetime
import copy
import csv


# Temperatures and weather summaries for various regions (7-day):
LUNENBURG_XML = 'https://weather.gc.ca/rss/city/ns-21_e.xml'


def csv_reader(filename):
    """Creates a python dictionary from a csv file"""
    openFile = open(filename, 'r')
    readFile = csv.reader(openFile)

    regions = {}

    for line in readFile:
        region_name = ', '.join( (line[0], line[1]) )
        regions[line[0].upper()] = (region_name, line[2])

    return regions


def get_time(time):
    """Takes a datetime object and returns a tuple
       containing the date and time"""

    return time.strftime('%d %B, %Y'), time.strftime('%I:%M %p') # date, time


def convert_hour(hourstr):
    """Take a string and return a formatted 12-hour time"""
    try:
        assert len(hourstr) == 5 # can't use assert in production code
    except AssertionError:
        print('Expected format: HH:MM')
    else:
        hour = int(hourstr[:2])
        minute = int(hourstr[-2:])
        time_object = datetime.time(hour=hour, minute=minute)
        time_output = time_object.strftime('%I:%M %p')

        return time_output


def fortune():
    ''' Fortunes '''
    fortunes = ['Godly luck.',
                'Your wisdom makes you superior to others.',
                'Error: Fortune not found.',
                'An interesting medical opportunity is in your near future.',
                'Today will be yesterday tomorrow.']

    n = random.randint(0, len(fortunes) - 1)
    print('Your fortune:', fortunes[n])


def print_lines(lines):
    """Helper function to test module"""
    for line in lines:
        print(line)


class WeatherPage:
    """Create and object representing a weather page
    with methods for collecting and displaying data."""
    def __init__(self, region):
        """Creates a variable called soup that contains
        the html text for a particle weather page based
        on region."""
        self.region, self.regionURL = region # (Name of region, URL)
        self.res = requests.get(self.regionURL)
        try:
            self.res.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
            sys.exit()
        else:
            self.soup = bs4.BeautifulSoup(self.res.text, features='lxml')

    def __str__(self):
        """Print string"""

        return 'Contains weather information for %s.' % self.region

    def convert_to_fahrenheit(self, c):
        """Takes a temperature in celsius and returns fahrenheit"""

        return int((c * (9 / 5)) + 32)

    def get_data(self):
        """Creates a variable that contains
        a dictionary with the current temperatures, summaries
        and times."""
        self.data = {'summaries': [], 'hours': [], 'temperatures': {'c': [], 'f': []}}

        for temperatures in self.soup.select('td[headers="header2"]'):
            self.data['temperatures']['c'].append(temperatures.getText())
            self.data['temperatures']['f'].append(str(self.convert_to_fahrenheit(int(temperatures.getText()))))

        for summary in self.soup.select('td div p'):
            self.data['summaries'].append(summary.getText())

        for hour in self.soup.select('td[headers="header1"]'):
            self.data['hours'].append(convert_hour(hour.getText()))

        return self.data


    def produce_output(self):
        """Produce the unformatted output for the weather forecast"""
        nowDate, nowTime = get_time(datetime.datetime.now())
        self.title = '24 Hour Weather Forecast'.center(58)
        self.header = "\n%s%s%s\n" % (self.region, nowTime.center(26), nowDate)
        self.colheads = '%s%s%s' % ('Time:'.ljust(16), 'Temp:'.ljust(9), 'Summary:'.ljust(13))
        self.output = [self.title, self.header, self.colheads]

        for i in range(24):
            line = '%s%s%s'
            self.output.append(line)

        return self.output, self.data


    def render_output(self, unit='c'):
        """Render the output with the values stored in
           self.data based on which temperature format
           the client requests"""
        output = copy.copy(self.output)
        self.outputRendered = []
        self.outputRendered.extend(output[:3])
        self.outputRendered.append('- ' * len(self.outputRendered[2]))
        output = output[3:]

        for i in range(len(output)):
            line = output[i] % (self.data['hours'][i].ljust(13),
                                     self.data['temperatures'][unit][i]+'º'+unit.upper().ljust(6),
                                     self.data['summaries'][i].ljust(10))
            self.outputRendered.append(line)

        return self.outputRendered


if __name__ == '__main__':
    regions = csv_reader('regions.csv')
    region = regions[sys.argv[1].upper()]
    data = WeatherPage(region)
    data.get_data()
    data.produce_output()
    print_lines(data.render_output())