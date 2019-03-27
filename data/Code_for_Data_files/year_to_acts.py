import json

year_to_acts = {}

with open("actlist.txt", encoding="utf8") as acts:
    for act in acts:
        act = act.strip()
        year = act[len(act)-4:]
        if not(year in year_to_acts):
            year_to_acts[year] = []
        year_to_acts[year].append(act)

print(json.dumps(year_to_acts, indent = 2))
