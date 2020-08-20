#!/bin/python
"""Create a window that contains a text area and buttons.
   The buttons will run weatherAPI and submit its output
   to the text area."""

from tkinter import *
from weatherAPI import *
import sys
from os.path import join as _

memos = {}
region = ''
regions = csv_reader(_(sys.path[0], 'regions.csv'))


def set_region(region_choice):
    """Sets the current region"""
    global region
    region = regions[region_choice]
    mbutton['text'] = region_choice.title()


def change_label(weatherObject, unit):
    """Takes a weatherObject and a unit and changes
       the label text"""
    weatherOutput = weatherObject.render_output(unit)
    weatherOutput = '\n'.join(weatherOutput)
    output['text'] = weatherOutput
    root.title('Weather - ' + weatherObject.region)


def weather_delegate(unit):
    """Takes a unit and call ph() on a weatherObject"""
    if not region:
        output['text'] = 'Please select a region.'
        return

    if region in memos.keys():
        weatherObject = memos[region]
        change_label(weatherObject, unit)
        return

    weatherObject = WeatherPage(region)
    weatherObject.get_data()
    weatherObject.produce_output()
    change_label(weatherObject, unit)
    memos[region] = weatherObject


def reset():
    """Resets the label and the notes dictionary"""
    global memos
    global region
    memos = {}
    region = ''
    mbutton['text'] = 'Select Region'
    output['text'] = "24 Hour Weather Forecast"
    root.title('Weather')


# Create and pack frames
root = Tk()
root.title('Weather')

output = Label(root, text="24 Hour Weather Forecast", justify=LEFT)
output.pack(side=TOP, anchor=W)

buttonFrame = Frame()
Button(buttonFrame, text="Celsius", command=(lambda unit='c': weather_delegate(unit))).pack(side=LEFT)
Button(buttonFrame, text="Fahrenheit", command=(lambda unit='f': weather_delegate(unit))).pack(side=LEFT)
mbutton = Menubutton(buttonFrame, text='Select Region')
picks   = Menu(mbutton, tearoff=False)
mbutton.config(menu=picks, direction='above', relief=GROOVE)
picks.add_command(label='Lunenburg',  command=(lambda: set_region('LUNENBURG')))
picks.add_command(label='Halifax',  command=(lambda: set_region('HALIFAX')))
picks.add_command(label='Truro',  command=(lambda: set_region('TRURO')))
picks.add_command(label='Sydney',  command=(lambda: set_region('SYDNEY')))
picks.add_command(label='Yarmouth',  command=(lambda: set_region('YARMOUTH')))
mbutton.pack(side=LEFT)
Button(buttonFrame, text='Exit', command=quit).pack(side=RIGHT)
Button(buttonFrame, text='Reset', command=reset).pack(side=RIGHT)
buttonFrame.pack(side=BOTTOM, fill=BOTH)

root.mainloop()
