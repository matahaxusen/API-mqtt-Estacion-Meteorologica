import yaml

def load_env():
    with open('env.yaml', 'rb') as env:
        loadout = yaml.load(env.read(), Loader=yaml.FullLoader)
    return loadout