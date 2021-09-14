import requests
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
import genetics
import gmplot


def timeDistance(loc1, loc2):
    api_key = "AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    r = requests.get(url + "origins=" + loc1 + "&destinations=" + loc2 + "&key=" + api_key)
    time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
    distance = str(r.json()["rows"][0]["elements"][0]["distance"]["text"])
    arr = [int(time.split()[0]), float(distance.split()[0])]
    return arr


def plot(lat, lng, zoom=10, map_type='roadmap'):
    bokeh_width, bokeh_height = 700, 600
    gmap_options = GMapOptions(lat=lat, lng=lng,
                               map_type=map_type, zoom=zoom)
    p = gmap("AIzaSyAz5utpPH8ALqDCcxD2IB4D14ZcWOj21p4", gmap_options, title='New York City',
             width=bokeh_width, height=bokeh_height)

    #p.line([-73.7061, -73.6184], [chromosome[i][5], [chromosome[i][4]]], line_width=2, color='black',
    #       alpha=0.3)
    #show(p)
    return p

def map_route(p, chromosome):

    for i in range(len(chromosome) - 1):
        p.circle(chromosome[i][3], chromosome[i][2], size=10, alpha=0.5, color='green')
        p.circle(chromosome[i][5], chromosome[i][4], size=10, alpha=0.5, color='green')
        p.circle(chromosome[i+1][3], chromosome[i+1][2], size=10, alpha=0.5, color='green')
        p.line([chromosome[i][3], chromosome[i][5]], [chromosome[i][2], chromosome[i][4]], line_width=2, color='black', alpha=0.3)
        p.line([chromosome[i][5], chromosome[i + 1][3]], [chromosome[i][4], chromosome[i+1][2]], line_width=2,
               color='black', alpha=0.3)


    # LAT AND LONG ARE SWITCHED

    # p.circle(-73.7061, 40.78209, size=10, alpha=0.5, color='red')
    #p.circle(-73.6184, 40.70933, size=10, alpha=0.5, color='red')

    # p.circle(-73.6453, 40.73827, size=10, alpha=0.5, color='orange')
    # p.circle(-73.6848, 40.65596, size=10, alpha=0.5, color='orange')
    #
    # p.circle(-73.6497, 40.77011, size=10, alpha=0.5, color='blue')
    # p.circle(-73.575, 40.67888, size=10, alpha=0.5, color='blue')
    #
    # p.circle(-73.5674, 40.70171, size=10, alpha=0.5, color='green')
    # p.circle(-73.6124, 40.85639, size=10, alpha=0.5, color='green')

    show(p)
