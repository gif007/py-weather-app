import requests
import sys
import bs4


memo = dict()
def resetMemo():
    global memo
    memo = dict()


def getWeatherForecast(URL, unit):
    """Returns formatted 24 hour weather forecast"""
    if URL in memo.keys():
        print('using memoized weather data')
        soup = memo[URL]
    else:
        print('fetching weather data')
        response = requests.get(URL)
        try:
            response.raise_for_status()
        except:
            print('Invalid URL')
            sys.exit()
        else:
            soup = getSoup(response)
            memo[URL] = soup

    hours, temperatures, summaries = getForecastData(soup)

    if unit == 'F':
        temperatures = convertToFahrenheit(temperatures)

    hoursBuffer = 10
    temperaturesBuffer = 15
    summariesBuffer = getPadding(summaries)
   
    header = createHeader(hoursBuffer, temperaturesBuffer, summariesBuffer)

    lines = []
    for i in range(24):
        lines.append('%s %s %s' % (
            hours[i].ljust(hoursBuffer),
            temperatures[i].ljust(temperaturesBuffer),
            summaries[i].ljust(summariesBuffer))
        )
        

    return header + '\n' + '\n'.join(lines)


def getSoup(response):
    """Returns a soup object"""
    return bs4.BeautifulSoup(response.text, features='lxml')


def convertToFahrenheit(temperatures):
    return [str(round((int(n) * (9/5) + 32))) for n in temperatures]


def createHeader(hoursBuffer, temperaturesBuffer, summariesBuffer):
    """Create and return a header with a horizontal rule"""
    header = '%s %s %s' % (
        'Time'.ljust(hoursBuffer),
        'Temperature'.ljust(temperaturesBuffer),
        'Summary'.ljust(summariesBuffer)
    )

    horizontalRule = '-' * sum([hoursBuffer, summariesBuffer, temperaturesBuffer])

    return header + '\n' + horizontalRule

def getForecastData(soup):
    """Returns hours, temperatures and summaries"""
    return getHours(soup), getTemperatures(soup), getSummaries(soup)


def getTemperatures(soup):
    """Returns a list of temperatures in celsius"""
    temps = []
    for temperatures in soup.select('td[headers="header2"]'):
        temps.append(temperatures.getText())

    return temps


def getSummaries(soup):
    """Returns a list of summaries"""
    summs = []
    for summary in soup.select('td div p'):
        summs.append(summary.getText())

    return summs


def getHours(soup):
    """Returns a list of hours"""
    hours = []
    for hour in soup.select('td[headers="header1"]'):
        hours.append(hour.getText())

    return hours


def getPadding(strings):
    """Take a list of strings and return a padding based on the longest string"""
    lengths = [len(string) + 4 for string in strings]

    return max(lengths)


if __name__ == '__main__':
    from sys import argv
    if len(argv) > 1:
        unit = argv[1]
    else:
        unit = 'C'

    print('The weather for Lunenburg, Nova Scotia')
    print(getWeatherForecast('https://weather.gc.ca/forecast/hourly/ns-21_metric_e.html', unit))