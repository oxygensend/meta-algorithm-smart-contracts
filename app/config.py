import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, '../data')


def data_dir(filename: str) -> str:
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    return os.path.join(DATA_DIR, filename)


def delete_data_dir():
    if os.path.exists(DATA_DIR):
        for file in os.listdir(DATA_DIR):
            os.remove(os.path.join(DATA_DIR, file))
        # os.rmdir(DATA_DIR)
