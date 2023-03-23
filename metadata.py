import logging
from functools import lru_cache
from tinytag import TinyTag

@lru_cache(maxsize=None)  # Cache song metadata
def get_song_metadata(filepath):
    try:
        tag = TinyTag.get(filepath)
        return tag.artist, tag.title, tag.album, tag.track, tag.year
    except Exception as e:
        logging.error(f"Error reading metadata for file '{filepath}': {e}")
        return None, None, None, None, None