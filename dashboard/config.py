import curses
from pprint import pprint
import textwrap
from typing import List
import pathlib

from dotenv import dotenv_values

from .config_file import ConfigFile

accepted_protocols = ["http", "https", "ws", "wss", "peer"]

env_config = dotenv_values('.env')

def generate_config_screen(stdscr):
    try:
        filename = env_config["CONFIG_FILE"]
    except KeyError:
        stdscr.addstr(row, column, f"***ERROR: No `CONFIG_FILE` listed in `.env`***", curses.color_pair(2))
    max_rows, max_cols = stdscr.getmaxyx()
    column_width = (max_cols - 10) / 2 - 10

    row = 5
    column = 10

    config_file = ConfigFile(filename)

    row, column = print_section("ports", parse_ports(config_file, column_width), stdscr, row, column)
    row, column = print_section("peers", parse_peers(config_file), stdscr, row, column)
    row, column = print_section("validator", parse_validator(config_file), stdscr, row, column)
    row, column = print_section("amendments", parse_amendments(config_file), stdscr, 5, int(column + column_width + 10))


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

def parse_ports(config_file, column_width: int):
    return_lines = []
    server = config_file["server"].get_lines()
    required_lines = ["ip", "port", "protocol"]
    for line in server:
        if line not in config_file._sections:
            return_lines.append(f"Error: [{line}] not in config file")
            continue

        config = config_file[line]._kv_pairs
        protocols = config["protocol"].split(',')
        config["protocol"] = protocols
        return_lines += textwrap.wrap(f"{line}: {config}", column_width, subsequent_indent="    ")

        for req_line in required_lines:
            if req_line not in config:
                return_lines.append(f"  Error: [{line}] is missing {req_line} value")
        for prot in protocols:
            if prot not in accepted_protocols:
                return_lines.append(f"  Error: {prot} not an accepted protocol")
    return return_lines

def parse_peers(config_file):
    return_lines = []
    ip_config = config_file["ips"]
    if "ips" in config_file._sections:
        for line in ip_config.get_lines():
            splt = line.split()
            if len(splt) > 2:
                return_lines.append(f"Error: too many items in this line: {line}")
            elif len(splt) == 2:
                return_lines.append(":".join(splt))
            elif len(splt) == 1:
                return_lines.append(splt[0])
    else:
        return_lines.append("Error: no [ips] section detected")
    
    if "ips_fixed" in config_file._sections:
        ip_fixed_config = config_file["ips_fixed"]
        for line in ip_fixed_config.get_lines():
            splt = line.split()
            if len(splt) > 2:
                return_lines.append(f"Error: too many items in this line: {line}")
            elif len(splt) == 2:
                return_lines.append(":".join(splt) + " (always maintain)")
            elif len(splt) == 1:
                return_lines.append(splt[0] + " (always maintain)")
    
    if "peer_private" in config_file._sections:
        lines = config_file["peer_private"].get_lines
        if len(lines) > 0:
            return_lines.append("Error: too many items under [peer_private]")
        if value == '0':
            return_lines.append("Peers won\'t broadcast address")
        elif value == '1':
            return_lines.append("Peers will broadcast address")
        else:
            return_lines.append("Error: invalid [peer_private] value")
    else:
        return_lines.append("Peers won\'t broadcast IP address")

    return return_lines

def parse_validator(config_file):
    return_lines = []

    is_validator = "validator_token" in config_file._sections
    if not is_validator:
        return ["Node is not a validator (does not have [validator_token] section)"]
    return_lines.append("Validator token:")
    return_lines += config_file["validator_token"].get_lines()

    return return_lines

def parse_amendments(config_file):
    return_lines = []
    if "features" not in config_file._sections:
        return ["Error: no amendments on this node"]

    config_amendments = config_file["features"].get_lines()
    current_directory = pathlib.Path(__file__).parent.resolve()
    with open(current_directory.joinpath('amendments.txt')) as file:
        lines = file.readlines()
        valid_amendments = set(line.rstrip() for line in lines)

    for amendment in valid_amendments:
        if amendment not in config_amendments:
            return_lines.append(f"Error: amendment f{amendment} not in list")
    return return_lines + config_amendments


if __name__ == "__main__":
    print(env_config)