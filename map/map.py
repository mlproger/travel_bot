import asyncio
from email.utils import unquote
import os
import time
from folium import PolyLine, Map, Marker, Icon
import requests
import polyline
import cloudconvert
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


async def get_point_from_api(name: str) -> list:
    # q = f"https://nominatim.openstreetmap.org/search?q={name}&format=json&polygon=1&addressdetails=1"
    # q = unquote(q)
    # print(q)
    # p = await asyncio.to_thread(requests.get, f"https://nominatim.openstreetmap.org/search?q={name}&format=json&polygon=1&addressdetails=1")\
    headers = {
        "User-Agent": "MyGeocoder/1.0 (contact: my@example.com)",  
        "Referer": "http://localhost" 
    }
    p = requests.get(f"https://nominatim.openstreetmap.org/search?q={name}&format=json&polygon=1&addressdetails=1", headers=headers)
    print(p.json())
    p_res = p.json()
    p1 = []
    p1.append(float(p_res[0]["lon"]))
    p1.append(float(p_res[0]["lat"]))
    return p1



async def set_route(points: dict):
    print(points)
    q = "http://router.project-osrm.org/route/v1/driving/"
    cc = []
    for point in points:
        for coord in points[point]:
            cc.append(coord[::-1])
            q += str(coord).replace("[", "").replace("]", "").replace(" ","")+";"
    q = q[:-1]
    q = unquote(q)
    print(q)
    r = await asyncio.to_thread(requests.get, q)
    res=r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    m = Map()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    PolyLine(locations=routes).add_to(m)
    m.fit_bounds(routes)
    for i in range(len(cc)):
        if i == 0:
            Marker(location=cc[i], icon = Icon(color="green"),popup="Точка").add_to(m)
        elif i == len(cc) - 1:
            Marker(location=cc[i], icon = Icon(color="red"),popup="Точка").add_to(m)
        else:
            Marker(location=cc[i], popup="Точка").add_to(m)
    m.save(f"{dir_path}/route.html")

    time.sleep(1)
    
    dr = webdriver.Remote("http://selenium-hub:4444/wd/hub", options = ChromeOptions())
    # # dr = webdriver.Chrome()
    dr.get(f"file://{dir_path}/route.html")
    print(f"file://{dir_path}/route.html")
    time.sleep(5)
    dr.save_screenshot(f"{dir_path}/route.png")
    dr.quit()

    return f"{dir_path}/route.png"






