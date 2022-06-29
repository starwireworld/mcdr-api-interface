import requests
from mcdreforged.api.all import *

import time
import multiprocessing
import json
import os
import uuid

## Config ##

# Update api every n secs
UPDATE_INTERVAL = 60 * 60

# Version of the stat files
# 1.7.6 - 1.12.2 (0)
# 1.13 - *       (1)
STAT_FORMAT_VERSION = 0

# Name of world
WORLD_NAME = 'world'

# Url to post data to
UPDATE_URI = ''

# Auth token (Header: token)
AUTH_TOKEN = ''

##       ##

PLAYER_STATS_PATH = f"{os.getcwd()}/server/{WORLD_NAME}/stats"
RUNNER = None

## Main Functions ##


def run_update():
    player_stats = {}

    # Load user stats
    for i in os.listdir(PLAYER_STATS_PATH):
        player_uuid = uuid.UUID(i.rsplit(".", 1)[0])
        with open(f'{PLAYER_STATS_PATH}/{i}', 'r') as file:
            json_data = json.loads(file.read())
            json_data = parse_stats_old(
                json_data) if STAT_FORMAT_VERSION == 0 else parse_stats(json_data)
            player_stats[player_uuid] = json_data

    # Process global stats
    global_json = get_global_stats(player_stats)

    # Make to send JSON
    to_send = global_json
    to_send["players"] = get_player_stats(player_stats)

    # Send data
    requests.post(UPDATE_URI, json=to_send, headers={'token': AUTH_TOKEN})


def main():
    while True:
        start = time.time()
        try:
            run_update()
        except:
            pass
        time.sleep(UPDATE_INTERVAL - (time.time() - start))

## Util Functions ##


def try_get_json(json, key, fallback):
    try:
        return json[key]
    except KeyError:
        return fallback

## Stat Parsers ##


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


## MCDR Events ##

def on_load(server, prev_module):
    global RUNNER
    RUNNER = multiprocessing.Process(target=main)
    RUNNER.start()


def on_unload(server):
    if RUNNER is None:
        return
    RUNNER.terminate()
