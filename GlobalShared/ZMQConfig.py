import configparser

config = configparser.ConfigParser()

config["CONNECT"] = {
    'ip': "127.0.0.1",
    'trackPort': "8030",
    'EventPort': "8088"
}

config.read('config.ini')


def create_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def set_config(section, option, val):
    config.set(section, option, val)


def read_config(section, option):
    val = config.get(section, option)
    return val
