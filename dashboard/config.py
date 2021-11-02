from pprint import pprint

from .config_file import ConfigFile


def parse_config(filename):
    config_file = ConfigFile(filename)
    pprint(config_file)


if __name__ == "__main__":
    filename = '/Users/mvadari/Documents/sidechain_config/main.no_shards.dog/rippled.cfg'
    parse_config(filename)