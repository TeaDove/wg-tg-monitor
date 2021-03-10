from pathlib import Path
import os
import logging
import configparser
import subprocess
import json

from aiogram import Bot, Dispatcher, executor, types, utils
import aiogram

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%y-%m-%d %H:%M:%S')
SCRIPT = Path(os.path.realpath(__file__))
os.chdir(SCRIPT.parent)


config = configparser.ConfigParser()
config.read("data/config.ini")
bot = Bot(token=config['credentials']['telegram-api'])
dp = Dispatcher(bot)
SUBSPACE_FOLDER = SCRIPT.parent / ".." / ".." / "subspace-wg" / "data"
PEERS_DICT = {}


def get_peers_dict() -> dict:
    with open(SUBSPACE_FOLDER / "config.json", 'r') as f:
        config = json.load(f)
        for profile in config["profiles"]:
            peer_config = configparser.ConfigParser()
            peer_config.read(SUBSPACE_FOLDER / "wireguard" / "peers" / (profile["id"]+".conf"))
            PEERS_DICT[peer_config['Peer']['PublicKey']] = profile["name"]


@dp.message_handler(commands = "wg")
async def send(message: types.Message):
    if message.from_user.id == int(config["credentials"]["owner_id"]):
        wg_output = subprocess.run(["wg"], capture_output=True).stdout.decode()
        peers = wg_output.split("peer: ")
        #logging.warn(peers)
        lines = peers[0].strip("\n").splitlines() 
        str_to_send = ''
        for line in lines:
            parts = line.split(':', 1)
            str_to_send += "    <b>" + parts[0].strip() + ": </b>" + parts[1].strip() + "\n"
        await message.reply(str_to_send, parse_mode="html")
        for peer in peers[1:]:
            lines = peer.strip("\n").splitlines()
            str_to_send = "peer: " + lines[0] + "\n"
            for line in lines[1:]:
                parts = line.split(':', 1)
                str_to_send += "    <b>" + parts[0].strip() + ": </b>" + parts[1].strip() + "\n"
            if lines[0] in PEERS_DICT:
                str_to_send += "    <b>name:</b><i> " + PEERS_DICT[lines[0]] + "</i>\n"
            await message.answer(str_to_send, parse_mode="html")

if __name__ == '__main__':
    get_peers_dict()
    executor.start_polling(dp, skip_updates=True)
