import urllib2, urllib, json, re, argparse, requests
from pprint import pprint

def get_woeid(city):
    woeidUrl = "http://woeid.rosselliot.co.nz/lookup/"+city
    r = requests.get(woeidUrl)
    # print r.text
    woeid = re.findall("<td class='woeid'>(.*?)</td>", r.text)[0]
    return woeid

def get_data(woeid):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid="+woeid
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    return data

def get_forecast(day, args, info):
    while day < args.d:
        forecast = info['item']['forecast'][day]
        if args.u == 'c': #centigrade
            lowC = (int(forecast['low'])-32)*5/9
            highC = (int(forecast['high'])-32)*5/9
            print forecast['date']+" "+forecast['day']+" "+str(lowC)+"~"+str(highC)+"C"+" "+forecast['text']
        else: #fahrenheit
            print forecast['date']+" "+forecast['day']+" "+forecast['low']+"~"+forecast['high']+"F"+" "+forecast['text']
        day+=1;

def get_current_condition(args, info):
    location = info['location']['city']
    condition = info['item']['condition']['text']
    fahrenheit = info['item']['condition']['temp']
    if args.u == 'c': #centigrade
        centigrade = (int(fahrenheit)-32)*5/9
        print location+", "+condition+", "+str(centigrade)+"C"
    else: #fahrenheit
        print location+", "+condition+", "+fahrenheit+"F"

if __name__ == '__main__':
    '''read config.py'''
    config = ""
    with open('./config.py', 'r') as fin:
        for line in fin:
            config=config+line

    # print config
    configLocation = re.findall('LOCATION=(\w+)', config)
    configUnit = re.findall('UNIT=(\w+)', line)
    # print type(configLocation[0])
    # print type(configUnit[0])

    '''parser'''
    argPrser = argparse.ArgumentParser(description='Process weather app argument.')
    argPrser.add_argument('-l', help="locations", metavar="locations")
    argPrser.add_argument('-u', help="unit", metavar="unit")
    argPrser.add_argument('-a', help="equal to -c -d 5", action='store_true')
    argPrser.add_argument('-c', help="current condition", action='store_true')
    argPrser.add_argument('-d', help="forecast day", type=int, metavar="day")
    argPrser.add_argument('-s', help="sunset/sunrise", action='store_true')
    args = argPrser.parse_args()
    # print args

    if args.l == None: #set config location
        city = configLocation[0]
    else:
        city = args.l

    if args.u == None: #set config unit
        args.u = configUnit[0]

    woeid = get_woeid(city)
    # print woeid
    data = get_data(woeid)
    # pprint(data['query']['results'])
    info = data['query']['results']['channel']

    if args.c == True: #current condition
        if args.a != True:
            get_current_condition(args, info)

    if args.d: #forecast
        if args.a != True:
            day = 0
            get_forecast(day, args, info)

    if args.s == True: #sun
        print "sunrise: "+info['astronomy']['sunrise']+", "+"sunrise: "+info['astronomy']['sunset']

    if args.a == True: #-c -d 5
        get_current_condition(args, info)
        day = 0
        args.d = 5
        get_forecast(day, args, info)
