import time
import multiprocessing
import json
import os
import uuid

import requests
from mcdreforged.api.all import *

from config import *
from util import *
from parsers import *

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


## MCDR Events ##

def on_load(server, prev_module):
    global RUNNER
    RUNNER = multiprocessing.Process(target=main)
    RUNNER.start()


def on_unload(server):
    if RUNNER is None:
        return
    RUNNER.terminate()
