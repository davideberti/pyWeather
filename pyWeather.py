# -*- coding: utf-8 -*-
__author__ = 'Admin'

import os
import urllib
import urllib2
import json
from decimal import Decimal
from xtermcolor import colorize

class Configuration:
    """config class holding APIKey, City, and Imperial"""
    def __init__(self):
        self.APIKey = "ed21de01250e9800e4759318de5ff"
        self.City = ""
        self.Imperial = True

class Conditions:
    """Condition class"""
    def __init__(self):
        self.ChanceOfRain = "" # "chanceofrain"`
        self.FeelsLikeC  = 0   #string"`
        self.PrecipMM = 0      #      float32 `json:"precipMM,string"`
        self.TempC  = 0        #      int     `json:"tempC,string"`
        self.TempC2 = 0        #      int     `json:"temp_C,string"`
        self.Time = 0          #      int     `json:"time,string"`
        self.VisibleDistKM  = 0#int     `json:"visibility,string"`
        self.WeatherCode  = 0  #int     `json:"weatherCode,string"`
        self.WeatherDesc  = [] # []struct{ Value string }
        self.WindGustKmph = 0  #int `json:",string"`
        self.Winddir16Point = ""  #string
        self.WindspeedKmph  = 0   #int `json:"windspeedKmph,string"`

class Astro:
    def __init__(self):
        self.Moonrise = ""
        self.Moonset  = ""
        self.Sunrise  = ""
        self.Sunset   = ""

class Weather:
    def __init__(self):
        self.Astronomy = [] #[]astro
        self.Date      = "" #string
        self.Hourly    = [] #[]cond
        self.MaxtempC  = 0  #int `json:"maxtempC,string"`
        self.MintempC  = 0  #int `json:"mintempC,string"`

class Location:
    def __init__(self):
        self.Query = "" #string `json:"query"`
        self.Type  = "" #string `json:"type"`

class Data:
    def __init__(self):
        self.cond    #              `json:"current_condition"`
        self.err     #              `json:"error"`
        self.loc     #              `json:"request"`
        self.weather #              `json:"weather"`

class resp:
    def __init__(self):
        self.listData = []

dictRain = { False:"mm", True:"in" }

dictTemp = { False:"C", True:"F" }

dictVis = { False:"km", True:"mi" }

dictWind = { False:"km/h", True:"mph" }

slotTimes = [ 9 * 60, 12 * 60, 18 * 60, 22 * 60 ]

dictCodes = {
    113: "iconSunny",
    116: "iconPartlyCloudy",
    119: "iconCloudy",
    122: "iconVeryCloudy",
    143: "iconFog",
    176: "iconLightShowers",
    179: "iconLightSleetShowers",
    182: "iconLightSleet",
    185: "iconLightSleet",
    200: "iconThunderyShowers",
    227: "iconLightSnow",
    230: "iconHeavySnow",
    248: "iconFog",
    260: "iconFog",
    263: "iconLightShowers",
    266: "iconLightRain",
    281: "iconLightSleet",
    284: "iconLightSleet",
    293: "iconLightRain",
    296: "iconLightRain",
    299: "iconHeavyShowers",
    302: "iconHeavyRain",
    305: "iconHeavyShowers",
    308: "iconHeavyRain",
    311: "iconLightSleet",
    314: "iconLightSleet",
    317: "iconLightSleet",
    320: "iconLightSnow",
    323: "iconLightSnowShowers",
    326: "iconLightSnowShowers",
    329: "iconHeavySnow",
    332: "iconHeavySnow",
    335: "iconHeavySnowShowers",
    338: "iconHeavySnow",
    350: "iconLightSleet",
    353: "iconLightShowers",
    356: "iconHeavyShowers",
    359: "iconHeavyRain",
    362: "iconLightSleetShowers",
    365: "iconLightSleetShowers",
    368: "iconLightSnowShowers",
    371: "iconHeavySnowShowers",
    374: "iconLightSleetShowers",
    377: "iconLightSleet",
    386: "iconThunderyShowers",
    389: "iconThunderyHeavyRain",
    392: "iconThunderySnowShowers",
    395: "iconHeavySnowShowers" #, // ThunderyHeavySnow
}

iconUnknown = [
    "    .-.      ",
    "     __)     ",
    "    (        ",
    "     `-’     ",
    "      •      "]
iconSunny = [
    "\033[38;5;226m    \\   /    \033[0m",
    "\033[38;5;226m     .-.     \033[0m",
    "\033[38;5;226m  ― (   ) ―  \033[0m",
    "\033[38;5;226m     `-’     \033[0m",
    "\033[38;5;226m    /   \\    \033[0m"]
iconPartlyCloudy = [
    "\033[38;5;226m   \\  /\033[0m      ",
    "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "             "]
iconCloudy = [
    "             ",
    "\033[38;5;250m     .--.    \033[0m",
    "\033[38;5;250m  .-(    ).  \033[0m",
    "\033[38;5;250m (___.__)__) \033[0m",
    "             "]
iconVeryCloudy = [
    "             ",
    "\033[38;5;240;1m     .--.    \033[0m",
    "\033[38;5;240;1m  .-(    ).  \033[0m",
    "\033[38;5;240;1m (___.__)__) \033[0m",
    "             "]
iconLightShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;111m     ‘ ‘ ‘ ‘ \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"]
iconHeavyShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
    "\033[38;5;21;1m   ‚‘‚‘‚‘‚‘  \033[0m",
    "\033[38;5;21;1m   ‚’‚’‚’‚’  \033[0m"]
iconLightSnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;255m     *  *  * \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m"]
iconHeavySnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
    "\033[38;5;255;1m    * * * *  \033[0m",
    "\033[38;5;255;1m   * * * *   \033[0m"]
iconLightSleetShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;111m     ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m* \033[0m",
    "\033[38;5;255m    *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘  \033[0m"]
iconThunderyShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;228;5m    ⚡\033[38;5;111;25m‘ ‘\033[38;5;228;5m⚡\033[38;5;111;25m‘ ‘ \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"]
iconThunderyHeavyRain = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;21;1m  ‚‘\033[38;5;228;5m⚡\033[38;5;21;25m‘‚\033[38;5;228;5m⚡\033[38;5;21;25m‚‘   \033[0m",
    "\033[38;5;21;1m  ‚’‚’\033[38;5;228;5m⚡\033[38;5;21;25m’‚’   \033[0m"]
iconThunderySnowShowers = [
    "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
    "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
    "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
    "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m"]
iconLightRain = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m",
    "\033[38;5;111m   ‘ ‘ ‘ ‘   \033[0m"]
iconHeavyRain = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;21;1m  ‚‘‚‘‚‘‚‘   \033[0m",
    "\033[38;5;21;1m  ‚’‚’‚’‚’   \033[0m"]
iconLightSnow = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;255m    *  *  *  \033[0m",
    "\033[38;5;255m   *  *  *   \033[0m"]
iconHeavySnow = [
    "\033[38;5;240;1m     .-.     \033[0m",
    "\033[38;5;240;1m    (   ).   \033[0m",
    "\033[38;5;240;1m   (___(__)  \033[0m",
    "\033[38;5;255;1m   * * * *   \033[0m",
    "\033[38;5;255;1m  * * * *    \033[0m"]
iconLightSleet = [
    "\033[38;5;250m     .-.     \033[0m",
    "\033[38;5;250m    (   ).   \033[0m",
    "\033[38;5;250m   (___(__)  \033[0m",
    "\033[38;5;111m    ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m*  \033[0m",
    "\033[38;5;255m   *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘   \033[0m"]
iconFog = [ "             ",
    "\033[38;5;251m _ - _ - _ - \033[0m",
    "\033[38;5;251m  _ - _ - _  \033[0m",
    "\033[38;5;251m _ - _ - _ - \033[0m",
    "             " ]

dictWinDir    = {
    	"N":   "\033[1m↓\033[0m",
		"NNE": "\033[1m↓\033[0m",
		"NE":  "\033[1m↙\033[0m",
		"ENE": "\033[1m↙\033[0m",
		"E":   "\033[1m←\033[0m",
		"ESE": "\033[1m←\033[0m",
		"SE":  "\033[1m↖\033[0m",
		"SSE": "\033[1m↖\033[0m",
		"S":   "\033[1m↑\033[0m",
		"SSW": "\033[1m↑\033[0m",
		"SW":  "\033[1m↗\033[0m",
		"WSW": "\033[1m↗\033[0m",
		"W":   "\033[1m→\033[0m",
		"WNW": "\033[1m→\033[0m",
		"NW":  "\033[1m↘\033[0m",
		"NNW": "\033[1m↘\033[0m",
	}


def initialize(config):
    #userhome = os.path.expanduser('~')
    #configpath = path.Join(usr.HomeDir, ".wegorc")
    config.APIKey = "ed21de01250e9800e4759318de5ff"
    config.City = "San Jose"
    config.Imperial = True

def printDay(weather):
    ret = ["|", "|", "|", "|", "|"]
    slots = []
    #print json.dumps(weather, indent=4, sort_keys=False)
    hourly = weather[0]['hourly'][0]['chanceofovercast']
    print hourly#['chanceofovercast']
    for h in hourly:
        c = 2
        for i,s in enumerate(slots):
            if abs(1-slotTimes[i]) < abs(s.Time-slotTimes[i]):
                h.Time = c
                slots[i] = h
	#for _, h := range hourly {
	#	c := int(math.Mod(float64(h.Time), 100)) + 60*(h.Time/100)
	#	for i, s := range slots {
	#		if math.Abs(float64(c-slotTimes[i])) < math.Abs(float64(s.Time-slotTimes[i])) {
	#			h.Time = c
	#			slots[i] = h

    for s in slots:
        ret = formatCond(s, False)
        for i in ret:
            ret[i].append("|")
	#for s in slots:
	#	ret = formatCond(s, False)
	#	for i in ret:
	#		ret[i].append("│")

    d = weather[0]['date']
    #print d
	#d, _ := time.Parse("2006-01-02", w.Date)
    dateFmt = "┤ " + d.encode('utf-8') + "  ├"
    print \
        "                                                       ┌─────────────┐                                                       \n" \
        "┌──────────────────────────────┬───────────────────────" +    dateFmt + "───────────────────────┬──────────────────────────────┐\n" \
        "│           Morning            │             Noon      └──────┬──────┘    Evening            │            Night             │\n" \
		"├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤\n"
    #print "ret"
    return ret.append(
		"└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘\n")
	#return ret

def getColor(temp):
    col = 21
    if (temp > 0):
        col = 196
    options = { -15:27,-14:27,-13:27,-12:33,-11:33,-10:33, -9:39,-8:39,-7:39,-6:45,-5:45,-4:45,-3:51,-2:51,-1:51,
                0:50,1:50,2:49,3:49,4:48,5:48,6:47,7:47,8:46,9:46,10:82,11:82,12:82,13:118,14:118,15:118,16:154,
                17:154,18:154,19:190,20:190,21:190,22:226,23:226,24:226,25:220,26:220,27:220,28:214,29:214,30:214,
                31:208,32:208,33:208,34:202,35:202,36:202}

    color = options.get(temp,col)
    tempUnit = temp
    if (config.Imperial):
        tempUnit = temp*1.8 + 32.0

    return fmt.Sprintf("\033[38;5;%03dm%d\033[0m", col, tempUnit)


def formatTemp(condition):
    getColor(temp)
    t = condition.TempC
    if (t == 0):
        t = condition.TempC2

    if (condition.FeelsLikeC < t):
        return fmt.Sprintf("%s – %s °%s         ", color(condition.FeelsLikeC), color(t), dictTemp[config.Imperial])[:48]
    elif (condition.FeelsLikeC > t):
		return fmt.Sprintf("%s – %s °%s         ", color(t), color(condition.FeelsLikeC), dictTemp[config.Imperial])[:48]

    return fmt.Sprintf("%s °%s            ", color(condition.FeelsLikeC), dictTemp[config.Imperial])[:31]

def getColor2(spd):
    col = 46
    if (spd > 0):
        col = 196

    options = {1:82,2:82,3:82,4:118,5:118,6:118,7:154,8:154,9:154,10:190,11:190,12:190,13:226,14:226,15:226,
               16:220,17:220,18:220,19:220,20:214,21:214,22:214,23:214,24:208,25:208,26:208,27:208,
               28:202,29:202,30:202,31:202}
    return options.get(spd,col)

def formatWind(condition):
	#getColor2(spd)
	spdUnit = spd
	if (config.Imperial):
		spdUnit = spd / 1.609
	return fmt.Sprintf("\033[38;5;%03dm%d\033[0m", col, spdUnit)

	if (condition.WindGustKmph > condition.WindspeedKmph):
		return fmt.Sprintf("%s %s – %s %s     ", windDir[condition.Winddir16Point], color(condition.WindspeedKmph), color(condition.WindGustKmph), dictWind[config.Imperial])[:57]

	return fmt.Sprintf("%s %s %s        ", windDir[condition.Winddir16Point], color(condition.WindspeedKmph), dictWind[config.Imperial])[:40]

def formatVisibility(condition):
    distUnit = condition['visibility']
    if (config.Imperial):
        distUnit = (float(distUnit) * 0.621)
    ret = str(distUnit)+" "+dictVis[config.Imperial]+"            "
    return ret

def formatRain(condition):
    rainUnit = condition['precipMM']
    if (config.Imperial):
        rainUnit = float(rainUnit) * 0.039

    #if (condition['ChanceOfRain'] != 0) :
    #    return fmt.Sprintf("%.1f %s | %s%%        ", rainUnit, unitRain[config.Imperial], c.ChanceOfRain)[:15]

	ret = str(rainUnit)+" "+dictRain[config.Imperial]
    return ret

def formatCond(condition, current):
    ret = []
    code = condition['weatherCode']
    arrow = condition['winddir16Point']
    windSpeed = condition['windspeedMiles']
    visibility = condition['visibility']
    precipMM = condition['precipMM']
    icon = dictCodes[float(code)] #get(code,iconUnknown)
#    desc = condition['weatherDesc'][0]['value']
    if(current):
        desc = condition['weatherDesc'][0]['value']
    print eval(icon)[0] + desc
    print eval(icon)[1]
    print eval(icon)[2] + dictWinDir[arrow] + " " + str(windSpeed) + " mp/h"
    print eval(icon)[3] + str(formatVisibility(condition))
    print eval(icon)[4] + str(formatRain(condition))

    #elif (lastRune =  utf8.DecodeLastRuneInString(desc); lastRune != ' ' {
    # esc = desc[:len(desc)-size] + "…"

    s = icon[0]+desc
    ret.append(s)
    ret.append(icon[1])
    ret.append(icon[2])
    #"%s %s %s", icon[0], icon[0], desc)
    #s = icon[2]ret.append(ret, fmt.Sprintf("%v %v %v", cur[1], icon[1], formatTemp(condition)))
    #ret.append(ret, fmt.Sprintf("%v %v %v", cur[2], icon[2], formatWind(condition)))
    s = icon[3]+str(formatVisibility(condition))
    ret.append(s)
    s = icon[4]+str(formatRain(condition))
    ret.append(s)#ret.append(ret, fmt.Sprintf("%v %v %v", cur[4], icon[4], formatRain(condition)))
    return ret

def main():
    initialize(config)
    uri="https://api.worldweatheronline.com/free/v2/weather.ashx?%s"
    num_of_days = 1
    params = urllib.urlencode({'key':config.APIKey, 'q': config.City, 'format': 'json', 'num_of_days': num_of_days, 'tp':3,'lang':'en'})
    response = urllib2.urlopen(uri % params)
    data = json.load(response)
    #print data
    print ("Weather for %s: %s" % (data['data']['request'][0]['type'], data['data']['request'][0]['query']))
    out = formatCond(data['data']['current_condition'][0],True) #make([]string, 5), r.Data.Cur[0], true)
    #for i in out:
    #    print i

    if (num_of_days == 0):
        return

    for i in range(num_of_days):
        ret = printDay(data['data']['weather'])
        #print ret

if __name__ == "__main__":
    config = Configuration()
    main()
