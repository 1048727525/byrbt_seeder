import json
with open('transmission_settings.json', 'r') as file:
    info = json.load(file)
info["stop_label"] = 1
with open('transmission_settings.json', 'w') as file:
    json.dump(info, file, indent=4, sort_keys=True)