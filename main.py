#!/bin/python
import frames
from tkinter import *

currentView = None

def viewTwentyFour(parent):
    global currentView
    if not currentView == 'twentyfour':
        TwentyFourHourForecast = frames.Forecast(parent)
        currentView = 'twentyfour'
        return TwentyFourHourForecast
    else:
        return


if __name__ == '__main__':
    root = Tk()
    root.title('Weather Forecast')
    menubar = Menu(root)
    root['menu'] = menubar
    menu_views = Menu(menubar)
    menubar.add_cascade(menu=menu_views, label='Views')
    menu_views.add_command(label='24 Hour Forecast', command=(lambda: viewTwentyFour(root)))
    root.mainloop()
