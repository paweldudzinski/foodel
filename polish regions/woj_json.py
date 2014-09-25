# -*- coding: utf-8 -*-
import json

with open("poland_json.json") as json_file:
    json_data = json.load(json_file)
    print(json_data)

