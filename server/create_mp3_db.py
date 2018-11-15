import os
import re
import sqlite3
import sys

import mutagen

count = 0
new = 0
error = 0
root_dir = None
conn = None


def create_table():
    c = conn.cursor()

    # Create table
    c.execute('CREATE TABLE IF NOT EXISTS songs (path TEXT, artist TEXT, track TEXT, album TEXT, label TEXT, songwriter TEXT)')
    c.execute('CREATE INDEX IF NOT EXISTS song_album ON songs (album)')
    c.execute('CREATE INDEX IF NOT EXISTS song_artist ON songs (artist)')
    conn.commit()


def parse_song(final_node):
    global count, new, error
    count += 1

    relative_filename = final_node.replace(root_dir, '')

    m = mutagen.File(final_node, easy=True)

    c = conn.cursor()

    c.execute('SELECT COUNT(path) FROM songs WHERE PATH=?', (str(relative_filename), ))
    exists = c.fetchone()[0] > 0

    print("[{}] {}. {}".format("!" if exists else "N", count, relative_filename))

    if exists:
        return

    try:
        c.execute('INSERT INTO songs (path, artist, track, album, label, songwriter) VALUES (?,?,?,?,?,?)',
                  (relative_filename, m['artist'][0], m['title'][0],
                   m['album'][0] if 'album' in m else '',
                   m['organization'][0] if 'organization' in m else '',
                   m['composer'][0] if 'composer' in m else ''))
        conn.commit()
        new += 1
    except KeyError:
        error += 1
        print("Error parsing [{}]".format(relative_filename))
        pass


def parse_dir(path):
    dir_files = []
    try:
        dir_files = os.listdir(path)
    except OSError:
        pass

    for final_node in [os.path.join(path, node) for node in dir_files]:
        if os.path.isdir(final_node):
            parse_dir(final_node)
        elif final_node.lower().endswith(('.mp3', 'm4a')):
            parse_song(final_node)


def init():
    global conn
    conn = sqlite3.connect("{}/songs.sqlite".format(os.path.dirname(sys.argv[0])))

    create_table()
    parse_dir(root_dir)

    conn.close()


if len(sys.argv) > 1:
    root_dir = re.sub(r'([^/])$', r'\1/', os.path.abspath(sys.argv[1]))
    init()

    print("")
    print("Added files relative to root dir: {}".format(root_dir))
    print("")
    print("Total mp3s: {}".format(count))
    print("Total new: {}".format(new))
    print("Total skipped: {}".format(error))
else:
    print("")
    print("Creates a SQLite db of each mp3 recursively in directory\n")
    print("    python {} DIRECTORY".format(sys.argv[0]))
