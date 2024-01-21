import json
import requests

data = {"coordinates": {"x": 100, "y": 100}}

filename = "single_resistor.jpg"

url = "http://127.0.0.1:5000/mask"

files = [
    ("image", ("new" + filename, open(filename, "rb"), "image/jpeg")),
    ("data", ("data", json.dumps(data), "application/json")),
]

r = requests.post(url, files=files)
print(r)
