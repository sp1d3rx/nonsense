from xml.dom.minidom import parse, parseString
from socket import *
from time import sleep
import httplib

sleepdelay = 3600
x = 0

while x < 6:
    sleepdelay = 3630
    if x <> 0: sleep(sleepdelay)
    x = x + 1
#    weatherHOST="www.google.com" #google API stopped working...
    weatherHOST="weather.yahooapis.com"
#    weatherAPI="/ig/api?weather=20500"
    weatherAPI="/forecastrss?w=2122265" #2122265 is Moscow....
    printerIP="127.0.0.99" #Your Printer IP address here...
    printerPORT=9100

    try:
        conn = httplib.HTTPConnection(weatherHOST)
        conn.request("GET", weatherAPI)
        weatherResponse = conn.getresponse()
    except:
        print "Could not connect to website.\n Check web settings and try again."

    if weatherResponse.status <> 200:
        print "Error returned from weather API. Double-check the API exists."
        print "-------------------------------------------------------------"
        print weatherResponse.read()
        print weatherResponse.status
        quit

    weatherXMLData = weatherResponse.read()

    dom = parseString(weatherXMLData)

    try:
        cTemp = dom.getElementsByTagName("yweather:condition")[0].getAttribute("temp")
        cCond = dom.getElementsByTagName("yweather:condition")[0].getAttribute("text")
    except:
        print "Weather API must have changed. Review the API and update this program."
        print "\n"
        print "Problem: "#, dom.getElementsByTagName("problem_cause")[0].getAttribute("data")
        print "------------====================------------------------------------------"
        print weatherXMLData
        print "------------====================------------------------------------------"
        quit

    try:
        printer = socket(AF_INET, SOCK_STREAM)
        printer.connect((printerIP, printerPORT))

    except:
        print "Could not connect to printer.\n Check IP or PORT and try again."
        quit

    try:
        s = "@PJL RDYMSG DISPLAY=\"MOSCOW Temp: %sF %s\"\r\n" % (cTemp,cCond)
        print s
        printer.send(s)
        printer.close()
    except:
        print "Can't send weather update to printer. Skipping printer update."

