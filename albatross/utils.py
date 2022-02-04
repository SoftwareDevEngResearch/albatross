import pkgutil
from yaml import load, Loader

WTK_FILE = './wtk.yml'


def _load_wtk(file=WTK_FILE):
    data = pkgutil.get_data(__name__, "wtk.yml")
    return load(data, Loader=Loader)
