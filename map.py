import requests
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions, Label
from bokeh.models.widgets import Tabs, Panel
import genetics
import googlemaps

def cached_timedistance(loc1,loc2):
    lookup = (loc1 + "," + loc2)
    #print("looking for in cache", lookup)
    #TODO faster search method
    line_num = 0
    with open("timedistance.txt", "r") as myFile:
        for line in myFile:
            line_num += 1
            if lookup in line:
                return [int(line.split(",")[4]), float(line.split(",")[5])]
        api_key = "AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA"
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        r = requests.get(url + "origins=" + loc1 + "&destinations=" + loc2 + "&key=" + api_key)
        time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
        distance = str(r.json()["rows"][0]["elements"][0]["distance"]["text"])
        arr = [int(time.split()[0]), float(distance.split()[0])]
        with open("timedistance.txt", "a") as f:
            f.write(loc1)
            f.write(",")
            f.write(loc2)
            f.write(",")
            f.write(str(arr[0]))
            f.write(",")
            f.write(str(arr[1])+"\n")
    myFile.close()
    return arr

def plot(lat, lng, zoom=10, map_type='roadmap'):
    bokeh_width, bokeh_height = 900, 600
    gmap_options = GMapOptions(lat=lat, lng=lng,
                               map_type=map_type, zoom=zoom)
    p = gmap("AIzaSyAz5utpPH8ALqDCcxD2IB4D14ZcWOj21p4", gmap_options, title='New York City',
             width=bokeh_width, height=bokeh_height)
    return p

#TODO bug with population[12], pop[2] and pop[14]
def chromsome_route(p, chromosome):
    p.circle(chromosome[0][3], chromosome[0][2], size=7, alpha=0.5, color='blue')
    p.circle(chromosome[0][5], chromosome[0][4], size=7, alpha=0.5, color='green')
    for i in range(len(chromosome)):
        if i != 0 and i != len(chromosome) - 1:
            p.circle(chromosome[i][3], chromosome[i][2], size=7, alpha=0.5, color='green')
            p.circle(chromosome[i][5], chromosome[i][4], size=7, alpha=0.5, color='green')
        loc1 = str(chromosome[i][2]) + "," + str(chromosome[i][3])
        loc2 = str(chromosome[i][4]) + "," + str(chromosome[i][5])
        route(cache_route(loc1,loc2),p, a=1)
        try:
            loc3 = str(chromosome[i+1][2]) + "," + str(chromosome[i+1][3])
            route(cache_route(loc2,loc3),p, a=0.5)
            p.circle(chromosome[i][3], chromosome[i][2], size=7, alpha=0.5, color='green')
            times = Label(x=130, y=70, x_units='screen', y_units='screen',
                          text=chromosome[0][1] + ", " + chromosome[1][1] + ", " + chromosome[2][1] + ", " +
                               chromosome[3][1], render_mode='css',
                          border_line_color='black', border_line_alpha=1.0,
                          background_fill_color='white', background_fill_alpha=0.5)
        except IndexError:
            p.circle(chromosome[i][5], chromosome[i][4], size=7, alpha=0.5, color='green')
            times = Label(x=130, y=70, x_units='screen', y_units='screen',
                          text=chromosome[0][1] + ", " + chromosome[1][1] + ", " + chromosome[2][1], render_mode='css',
                          border_line_color='black', border_line_alpha=1.0,
                          background_fill_color='white', background_fill_alpha=0.5)
    p.add_layout(times)
    return p
    #show(p)

## restructure so that each trip is individual

def cache_route(loc1, loc2):
    f = open("routes.txt", "r")
    if loc1 in f.read():
        waypoints = []
        while "-----" not in f.read(): #5 lines
            waypoints.append(f.readline())
            f.close()
            return waypoints
    else:
        f = open("routes.txt", "a")
        gmaps = googlemaps.Client(key='AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA')
        marker_points = []
        waypoints = []

        results = gmaps.directions(origin=(loc1), destination=(loc2))

        for leg in results[0]["legs"]:
            leg_start_loc = leg["start_location"]
            marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
            for step in leg["steps"]:
                end_loc = step["end_location"]
                waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
        last_stop = results[0]["legs"][-1]["end_location"]
        marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

        for i in range(len(waypoints) - 1):
            f.write(waypoints[i])
        f.write("\n")
        f.close()
        return waypoints

def route(waypoints,p,a):
    for i in range(len(waypoints)-1):
        p.line([float(waypoints[i].split(",")[1]), float(waypoints[i+1].split(",")[1])], [float(waypoints[i].split(",")[0]), float(waypoints[i+1].split(",")[0])], line_width=2, alpha = a, color='grey')


def final_gui(population):
    lat,lon = 40.7128, -73.8010
    abs = []
    for i in range(len(population)):
        trip_map = chromsome_route(plot(lat, lon), population[i])
        panel = Panel(child = trip_map, title="Trip" + str(i))
        abs.append(panel)

    tabs = Tabs(tabs = abs)
    show(tabs)
