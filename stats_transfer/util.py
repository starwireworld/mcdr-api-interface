# Sum the stats of all the players into the global stats
def get_global_stats(json):
    final = {}

    for player in json.keys():
        for key in json[player].keys():
            if key not in final:
                final[key] = 0
            final[key] += json[player][key]

    return final


# Convert the UUID key to a String key
def get_player_stats(json):
    final = {}

    for uuid in json.keys():
        player = str(uuid)
        final[player] = json[uuid]

    return final


# Try to get a value from a dict, it it fails return a fallback value
def try_get_json(json, key, fallback):
    try:
        return json[key]
    except KeyError:
        return fallback
