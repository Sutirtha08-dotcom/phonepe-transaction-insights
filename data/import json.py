import json

with open('data/aggregated/transaction/country/india/2018/1.json') as f:
    data = json.load(f)

print(json.dumps(data, indent=2))