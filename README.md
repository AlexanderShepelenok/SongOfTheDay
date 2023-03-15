# SongOfTheDay script

This is a Python script that searches for a song on Spotify, YouTube, Yandex.Music and returns the links to the song and album cover.
I use it to generate posts to my Telegram channel.

### Requirements

To use this script, you will need:

- Python 3.6 or later
- `spotipy`, `googleapiclient`, `requests` and `urllib` libraries

You can install missing libraries with pip, like this:

```
pip install spotipy
```

### Usage

You can run the script from the command line with the artist and track title as arguments, like this:

```
python songoftheday.py "Radiohead" "Paranoid Android"
```

The script will print the links and album cover link for the song, if it is found on resources mentioned earlier.
Note that Spotify, Yandex.Music and YouTube may not have all songs in their databases, so the script may not find a match for some songs.

### License

This script is released under the MIT License. Feel free to use, modify, and distribute it as you wish.