from util import try_get_json

# Parse stats from version 1.13 onward
def parse_stats(json):
    mined_block = 0
    play_ticks = 0
    deaths = 0

    if "stats" in json:
        json = json["stats"]

        if "minecraft:mined" in json:
            for i in json["minecraft:mined"].values():
                mined_block += i

        if "minecraft:custom" in json:
            play_ticks = try_get_json(
                json["minecraft:custom"], "minecraft:play_time", 0)
            deaths = try_get_json(
                json["minecraft:custom"], "minecraft:deaths", 0)

    return {
        "minedBlocks": mined_block,
        "playTicks": play_ticks,
        "deathCount": deaths
    }


# Parse stats from version 1.7.6 to 1.12.2
def parse_stats_old(json):
    mined_blocks = 0
    play_ticks = try_get_json(json, "stat.playOneMinute", 0)
    deaths = try_get_json(json, "stat.deaths", 0)

    for key in json.keys():
        if key.startswith("stat.mineBlock."):
            mined_blocks += json[key]

    return {
        "minedBlocks": mined_blocks,
        "playTicks": play_ticks,
        "deathCount": deaths
    }
