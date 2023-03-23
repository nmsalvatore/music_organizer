import os
import shutil
from collections import defaultdict

from metadata import get_song_metadata
from utilities import is_song_file


def group_songs_by_album(songs):
    album_groups = defaultdict(list)
    for song in songs:
        artist, _, album, track, year = get_song_metadata(song)
        if artist and album:
            if year:
                album_key = f"{artist} - {album} ({year})".lower()
            else:
                album_key = f"{artist} - {album}".lower()
            album_groups[album_key].append((song, track))
        else:
            album_groups[None].append((song, track))
    return album_groups


def move_songs_to_album_directory(album_key, album_songs, album_dirs, albums_path):
    for song, track in album_songs:
        _, title, _, _, _ = get_song_metadata(song)
        file_ext = os.path.splitext(song)[1]
        new_song_name = f"{track.zfill(2)} {title}{file_ext}".lower()

        if album_key not in album_dirs:
            album_dir = os.path.join(albums_path, album_key)
            os.makedirs(album_dir, exist_ok=True)
            album_dirs[album_key] = album_dir
        shutil.move(song, os.path.join(album_dirs[album_key], new_song_name))


def move_songs_to_miscellaneous_directory(album_songs, miscellaneous_path):
    for song, _ in album_songs:
        artist, title, _, _, _ = get_song_metadata(song)
        file_ext = os.path.splitext(song)[1]
        new_song_name = f"{artist} - {title}{file_ext}".lower()
        shutil.move(song, os.path.join(miscellaneous_path, new_song_name))


def move_songs_to_albums(songs, albums_path, miscellaneous_path):
    album_dirs = {}
    album_groups = group_songs_by_album(songs)

    for album_key, album_songs in album_groups.items():
        if len(album_songs) > 1 and album_key:  # Move to the album directory
            move_songs_to_album_directory(album_key, album_songs, album_dirs, albums_path)
        else:  # Move to the miscellaneous directory
            move_songs_to_miscellaneous_directory(album_songs, miscellaneous_path)


def gather_song_files(directory):
    song_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if is_song_file(file):
                song_files.append(os.path.join(root, file))
    return song_files