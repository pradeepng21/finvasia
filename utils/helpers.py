from configparser import ConfigParser
import json


def read_config_v1(cfgfile):
    parser = ConfigParser()
    parser.read(cfgfile)
    output = {}
    for section in parser.sections():
        output[section] = {}
        for key, _ in parser.items(section):
            output[section][key] = json.loads(parser.get(section, key))

    return output