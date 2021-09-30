import requests
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
import genetics
import googlemaps

def timeDistance(loc1, loc2):
    #f = open("timedistance.txt", "r")
   #print("COPY")
   # print('\'destination_addresses\': [\'' + loc2 + '\'], \'origin_addresses\': [\'' + loc1 + '\']')


    api_key = "AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    r = requests.get(url + "origins=" + loc1 + "&destinations=" + loc2 + "&key=" + api_key)
    time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
    distance = str(r.json()["rows"][0]["elements"][0]["distance"]["text"])
    arr = [int(time.split()[0]), float(distance.split()[0])]
    #print("REAL")
    #print(r.json())
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

def route(p, chromosome):
    gmaps = googlemaps.Client(key ='AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA')

    marker_points = []
    waypoints = []

    # extract the location points from the previous directions function
    results = gmaps.directions(origin=(40.8093,-73.4862), destination = (40.81912,-73.4577))
    #print(results)


    for leg in results[0]["legs"]:
        leg_start_loc = leg["start_location"]
        marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
        for step in leg["steps"]:
            end_loc = step["end_location"]
            waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
    last_stop = results[0]["legs"][-1]["end_location"]
    marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')


    #p.line([chromosome[i][5], chromosome[i+1][3]], [chromosome[i][4], chromosome[i+1][2]], line_width=2, color='black',
    #p.circle(float(marker_points[0].split(",")[1]),float(marker_points[0].split(",")[0]), size=7, alpha=0.5, color='green')
    #p.line([float(marker_points[0].split(",")[1]), float(marker_points[1].split(",")[1])],[float(marker_points[0].split(",")[0]), float(marker_points[1].split(",")[0])], line_width=2, color='black')
    #origin = (40.8093, -73.4862), destination = (, ))
    p.circle(-73.4862,40.8093, size=7, alpha=0.5, color='green')
    p.circle(-73.4577, 40.81912, size=7, alpha=0.5, color='green')
    print(len(waypoints))
    for i in range(len(waypoints)-1):
        p.line([float(waypoints[i].split(",")[1]), float(waypoints[i+1].split(",")[1])], [float(waypoints[i].split(",")[0]), float(waypoints[i+1].split(",")[0])], line_width=2, color='black')

    show(p)


