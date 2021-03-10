from pathlib import Path
import os
import logging
import configparser
import subprocess
import json
import asyncio

from aiogram import Bot, Dispatcher, executor, types, utils
import aiogram

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
SCRIPT = Path(os.path.realpath(__file__))
os.chdir(SCRIPT.parent)


config = configparser.ConfigParser()
config.read("data/config.ini")
bot = Bot(token=config['credentials']['telegram-api'])
dp = Dispatcher(bot)
SUBSPACE_FOLDER = SCRIPT.parent / "subspace-wg" / "data"
PEERS_DICT = {}
OWNERS = config["credentials"]["owners_id"].split()


def get_peers_dict() -> dict:
    with open(SUBSPACE_FOLDER / "config.json", 'r') as f:
        config = json.load(f)
        for profile in config["profiles"]:
            peer_config = configparser.ConfigParser()
            peer_config.read(SUBSPACE_FOLDER / "wireguard" / "peers" / (profile["id"]+".conf"))
            PEERS_DICT[peer_config['Peer']['PublicKey']] = profile["name"]

async def send_wg_stats():
    channel_id = config["credentials"]["channel_id"]
    if (SCRIPT.parent / "data" / "messages.json").exists():
        with open(SCRIPT.parent / "data" / "messages.json", 'r') as f:
            messages_id = json.load(f)
    else:
        with open(SCRIPT.parent / "data" / "messages.json", 'w') as f:
            messages_id = None
            json.dump([], f)
    if messages_id is not None:
        for message_id in messages_id:
            try:
                await dp.bot.delete_message(channel_id, message_id)
            except:
                pass
    messages_id = []
    get_peers_dict()
    wg_output = subprocess.run(["wg"], capture_output=True).stdout.decode()
    peers = wg_output.split("peer: ")
    lines = peers[0].strip("\n").splitlines() 
    str_to_send = ''
    for line in lines:
        parts = line.split(':', 1)
        str_to_send += "    <b>" + parts[0].strip() + ": </b>" + parts[1].strip() + "\n"
    message = await dp.bot.send_message(channel_id, str_to_send, parse_mode="html")
    messages_id.append(message.message_id)
    for peer in peers[1:]:
        lines = peer.strip("\n").splitlines()
        str_to_send = "peer: " + lines[0] + "\n"
        for line in lines[1:]:
            parts = line.split(':', 1)
            str_to_send += "    <b>" + parts[0].strip() + ": </b>" + parts[1].strip() + "\n"
        if lines[0] in PEERS_DICT:
            str_to_send += "    <b>name:</b><i> " + PEERS_DICT[lines[0]] + "</i>\n"
        message = await dp.bot.send_message(channel_id, str_to_send, parse_mode="html")
        messages_id.append(message.message_id)
    with open(SCRIPT.parent / "data" / "messages.json", 'w') as f:
        json.dump(messages_id, f)

if __name__ == '__main__':
    asyncio.run(send_wg_stats())