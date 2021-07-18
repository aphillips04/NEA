import json
from classes import *

with open("playerdata.json", "a+") as f:
    if not f.read():
        json.dump({}, f, indent=4)
