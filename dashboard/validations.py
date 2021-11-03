import base64
import curses
from pprint import pprint
import json
from typing import List
import pathlib

import requests
from dotenv import dotenv_values

from dashboard.config_file import ConfigFile

env_config = dotenv_values('.env')

def validation_screen(stdscr):
    row = 5
    column = 10
    try:
        filename = env_config["CONFIG_FILE"]
    except KeyError:
        stdscr.addstr(row, column, f"***ERROR: No `CONFIG_FILE` listed in `.env`***", curses.color_pair(2))
        return
    
    try:
        config_file = ConfigFile(filename)
    except FileNotFoundError:
        stdscr.addstr(row, column, f"***ERROR: {filename} does not exist", curses.color_pair(2))
        return
    
    if "validators_file" not in config_file._sections:
        stdscr.addstr(row, column, f"***ERROR: No [validators_file] section in config file", curses.color_pair(2))
        return
    
    validation_file = config_file["validators_file"].get_lines()[0]
    config_directory = pathlib.Path(filename).parent.resolve()
    complete_validation_file = config_directory.joinpath(validation_file)
    
    # TODO: add check for [validators]

    row, column = print_section("validators", get_validator_list(str(complete_validation_file)), stdscr, row, column)

def get_validator_list(filename):
    validator_config = ConfigFile(filename)
    validator_list_sites = validator_config["validator_list_sites"].get_lines()
    validators = set()
    for site in validator_list_sites:
        jsn = requests.get(site).json()
        blob = jsn["blob"]
        decoded_blob = json.loads(base64.b64decode(blob))
        for validator in decoded_blob["validators"]:
            validators.add('- ' + validator["validation_public_key"])
    return [f"Count: {len(validators)}"] + list(validators)



def print_section(section_name: str, return_lines: List[str], stdscr, row: int, column: int):
    stdscr.addstr(row, column, f"***{section_name.upper()}***", curses.color_pair(3))
    row += 2

    for line in return_lines:
        color_pair = 1
        if "Error" in line:
            color_pair = 2
        stdscr.addstr(row, column, line, curses.color_pair(color_pair))
        row += 1
    row += 2
    return (row, column)

if __name__ == "__main__":
    get_validator_list("/Users/mvadari/.config/ripple/validators.txt")