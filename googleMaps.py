import requests, json
import smtplib

def map(loc1, loc2):
    api_key = "AIzaSyCoZXeFCIM0XBfv7jcdWvds4zfJcoGm7TA"
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    r = requests.get(url + "origins=" + loc1 + "&destinations=" + loc2 + "&key=" + api_key)
    time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
    distance = str(r.json()["rows"][0]["elements"][0]["distance"]["text"])
    arr = [int(time.split()[0]), float(distance.split()[0])]
    return arr

