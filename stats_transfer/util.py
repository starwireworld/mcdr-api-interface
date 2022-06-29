
def get_global_stats(json):
    final = {}

    for player in json.keys():
        for key in json[player].keys():
            if key not in final:
                final[key] = 0
            final[key] += json[player][key]

    return final


def get_player_stats(json):
    final = {}

    for uuid in json.keys():
        player = str(uuid)
        final[player] = json[uuid]

    return final


def try_get_json(json, key, fallback):
    try:
        return json[key]
    except KeyError:
        return fallback
