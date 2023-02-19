from time import time
import datetime
import os

from pathlib import Path
import toml

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import h5py


def save_results(data, model, config):
    epochtime = time()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    config['metadata']['timestamp'] =  timestamp
    location = f'./results/{config["title"]}_{timestamp}/'
    os.mkdir(location)
    file = h5py.File(f'{location}data.h5' , 'w')
    file.create_dataset('data', data=data, dtype=np.float64)
    file.create_dataset('columns', data=model.columns)
    file.create_dataset('time', data=epochtime)
    with open(f'{location}config.toml', 'w') as f:
        toml.dump(config, f)

def read_results(h5_file_path):
    with h5py.File('data.h5', 'r') as f:
        data = f['data'][:]
        columns = f['columns'][:]
    df = pd.DataFrame(data=data, columns=[c.decode('utf-8') for c in columns])
    return df

def read_config(config_location: str = None):
    if config_location is None:
        cwd = Path().resolve()
        config_path = list(Path(cwd).glob('*.toml'))[0]
    else:
        config_path = Path(config_location).expanduser().resolve()
    config: dict = toml.load(config_path)
    return config


def save_plot(
    fig: plt.Figure,
    save_path: str,
    titel: str
) -> None:

    fig.savefig(f'{save_path}{"_".join(titel.split())}.pdf')

    fig.patch.set_facecolor('xkcd:mint green')
    fig.savefig(f'{save_path}{"_".join(titel.split())}_green.pdf')
    return None
