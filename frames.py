from tkinter import *
import datetime
import json
from os.path import join
from sys import path
from logic import getWeatherForecast


class Forecast(Frame):
    """ Provides 24 hour weather forecast by region """

    def __init__(self, parent=None, **options):
        """Initialize unit, regions, memos and pack frame with title"""
        self.unit = 'C'
        self.appFont = ('times', 16, 'normal')
        self.currentRegion = None
        self.regions = self.getRegions()
        self.memos = self.instantiateMemos()
        Frame.__init__(self, parent, **options)
        self.pack(expand=YES, fill=BOTH)
        # Initialize dynamic portions of UI
        self.setup()
        # Create footer
        Label(self, width=75, font=('times', 14, 'bold'), text='weather.gc.ca\n').pack()


    def setup(self):
        """Initialize all dynamic portions of the UI"""
        self.header = Label(self, text=f'24 Hour Forecast')
        self.header.config(font=self.appFont)
        self.header.pack(side=TOP, expand=YES, fill=X)

        fullUnitName = 'celsius' if self.unit == 'C' else 'fahrenheit'
        self.subheader = Label(self, text=f'({fullUnitName})')
        self.subheader.config(font=('times', 14, 'normal'))
        self.subheader.pack(side=TOP, expand=YES, fill=X)

        self.city = Label(self, text='Please choose a city\n')
        self.city.config(font=self.appFont)
        self.city.pack(side=TOP, expand=YES, fill=X)

        self.table = Label(self, height=30, text='', anchor=N, justify=LEFT)
        self.table.config(font=('fixedsys', 12, 'normal'))
        self.table.pack(side=TOP, expand=YES, fill=BOTH)

        # Instantiate button frame with preset height and width
        self.buttons = Frame(self, height=50, width=300)
        self.buttons.pack(side=TOP, expand=NO, fill=None)
        self.buttons.pack_propagate(0)

        # Toggle unit between celsius and fahrenheit
        self.toggle = Button(self.buttons, text='F', command=self.toggleUnit)
        self.toggle.pack(side=LEFT, expand=YES)

        self.menuButton = Menubutton(self.buttons, text='Select Region')
        self.menuButton.pack(side=LEFT, expand=YES)

        # Create menu items
        self.instantiateMenu()

        # Reset all memoized data and UI
        Button(self.buttons, text='Reset', command=self.reset).pack(side=LEFT, expand=YES)
        # Quit program
        Button(self.buttons, text='Exit', command=self.quit).pack(side=LEFT, expand=YES)


    def reset(self):
        """Return UI and memo container to default values"""
        self.unit = 'C'
        self.menuButton.config(text='Select Region')
        self.currentRegion = None
        self.city.config(text='Please choose a city\n')
        self.table.config(text='')
        self.memos = self.instantiateMemos()
        fullUnitName = 'celsius' if self.unit == 'C' else 'fahrenheit'
        self.subheader.config(text=f'({fullUnitName})')
        self.toggle.config(text='F')


    def instantiateMenu(self):
        """Create the popup menu for region selection"""
        self.regionMenu = Menu(self.menuButton, tearoff=False)
        self.menuButton.config(menu=self.regionMenu, direction='above', relief=GROOVE)
        # Dynamically set up menu items based on region data
        for region in self.regions:
            self.regionMenu.add_command(label=region, command=(lambda region=region: self.updateForecast(region)))


    def instantiateMemos(self):
        """Set up default values for each region"""
        memos = dict()
        for region in self.regions:
            memos[region] = {
                'data': None
            }

        return memos


    def getRegions(self):
        """Instantiate region data from JSON file"""
        return json.loads(open(join(path[0], 'regions.json')).read())


    def updateForecast(self, region):
        """Update UI with forecast data"""
        self.currentRegion = region
        # Check memos for saved weather forecast
        if self.memos[region]['data']:
            data = self.memos[region]['data']
        else:
            # Create weather data if it does not exist in memo
            url = self.regions[region]['url']
            data = {
                'timestamp': self.stampIt(),
                'forecastInCelsius': getWeatherForecast(url, 'C'),
                'forecastInFahrenheit': getWeatherForecast(url, 'F'),
                'name': self.regions[region]['name'],
                'url': url
            }
            self.memos[region]['data'] = data

        self.city.config(text='%s - %s (Your local time)\n' % (data['name'], data['timestamp']))
        if self.unit == 'C':
            self.table.config(text='%s' % data['forecastInCelsius'])
        else:
            self.table.config(text='%s' % data['forecastInFahrenheit'])
        # Menu button reflects current region
        self.menuButton.config(text=data['name'])


    def stampIt(self):
        """Create timestamp"""
        return datetime.datetime.now().strftime("%d %B, %Y %H:%M %p")


    def toggleUnit(self):
        """Toggles unit between celsius and fahrenheit"""
        previousUnit = self.unit
        self.unit = 'F' if previousUnit == 'C' else 'C' 
        self.toggle.config(text=previousUnit)
        fullUnitName = 'celsius' if self.unit == 'C' else 'fahrenheit'
        self.subheader.config(text=f'({fullUnitName})')
        if self.currentRegion:
            data = self.memos[self.currentRegion]['data']
            if self.unit == 'C':
                self.table.config(text='%s' % data['forecastInCelsius'])
            else:
                self.table.config(text='%s' % data['forecastInFahrenheit'])
