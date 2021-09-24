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
    p.circle(chromosome[0][3], chromosome[0][2], size=7, alpha=0.5, color='blue')
    p.circle(chromosome[0][5], chromosome[0][4], size=7, alpha=0.5, color='green')
    for i in range(len(chromosome)):
        p.line([chromosome[i][3], chromosome[i][5]], [chromosome[i][2], chromosome[i][4]], line_width=2, color='black',
               alpha=0.4)
        if i != 0 and i != len(chromosome)-1:
            p.circle(chromosome[i][3], chromosome[i][2], size=7, alpha=0.5, color='green')
            p.circle(chromosome[i][5], chromosome[i][4], size=7, alpha=0.5, color='green')
        try:
            p.line([chromosome[i][5], chromosome[i+1][3]], [chromosome[i][4], chromosome[i+1][2]], line_width=2, color='black',
               alpha=0.2)
        except IndexError:
            p.circle(chromosome[i][3], chromosome[i][2], size=7, alpha=0.5, color='green')
            p.circle(chromosome[i][5], chromosome[i][4], size=7, alpha=0.5, color='green')
        print("trip", i, ":", chromosome[i])
    show(p)
