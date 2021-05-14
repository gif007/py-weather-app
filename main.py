#!/bin/python
import frames
from tkinter import *


if __name__ == '__main__':
    root = Tk()
    root.title('Weather Forecast')
    TwentyFourHourForecast = frames.Forecast(root)
    root.mainloop()
