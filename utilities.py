import logging
import os


def is_song_file(filename):
    song_extensions = {'.mp3', '.wav', '.m4a', '.flac'}
    return any(filename.lower().endswith(ext) for ext in song_extensions)


def shorten_path(path):
    home_dir = os.path.expanduser("~")
    if path.startswith(home_dir):
        return path.replace(home_dir, "~", 1)
    else:
        return os.path.relpath(path, home_dir)


def expand_path(path):
    home_dir = os.path.expanduser("~")
    if path.startswith("~"):
        return path.replace("~", home_dir, 1)
    else:
        return os.path.abspath(os.path.join(home_dir, path))
    

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
