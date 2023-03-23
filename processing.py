import configparser
import os

from organization import gather_song_files, move_songs_to_albums

def process_directory(directory, albums_path, miscellaneous_path):
    song_files = gather_song_files(directory)
    move_songs_to_albums(song_files, albums_path, miscellaneous_path)

def remove_empty_directories(path):
    if os.path.isdir(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            remove_empty_directories(item_path)

        if not os.listdir(path):
            os.rmdir(path)

def save_config(config, config_file):
    with open(config_file, 'w') as f:
        config.write(f)

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config