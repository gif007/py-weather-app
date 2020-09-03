#!/bin/python

import csv
import datetime



''' Functions for WeatherAPI '''

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


''' Random functions '''

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

