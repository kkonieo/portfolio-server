import json
import os
import string
import time

import requests

# request delay
DELAY = 0.3
# request host
HOST = os.getenv("HOST")

# make alphabet range ( a to z)
queries = [x + y for y in string.ascii_lowercase for x in string.ascii_lowercase]
data = set()

# scrap data
for query in queries:
    try:
        url = f"{HOST}/api/tags/search?term={query}&category=technical"
        response = requests.get(url)

        response_data = response.json()["results"]
        for item in response_data:
            data.add(item["text"])
        time.sleep(DELAY)
    except Exception:
        print(f"error - query: {query}")

# make json data
json_data = []
for idx, tag in enumerate(data):
    json_data.append({"model": "skill.skill", "pk": idx + 1, "fields": {"name": tag}})

# save
f = open("output.json", "w")
f.write(json.dumps(json_data))
f.close()
