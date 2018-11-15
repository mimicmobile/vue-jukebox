import csv
import os
import re
import sys

import mutagen

count = 0
new = 0
error = 0
root_dir = None
csv_data = {}


def parse_song(final_node):
    global count, new, error
    count += 1

    relative_filename = final_node.replace(root_dir, '')

    m = mutagen.File(final_node, easy=True)

    if relative_filename in csv_data:
        data = csv_data[relative_filename]
    else:
        return

    print("Matched [{}]".format(relative_filename))

    artist = data['artist'] if 'artist' in data else ""
    title = data['track'] if 'track' in data else ""
    album = data['album'] if 'album' in data else ""
    label = data['label'] if 'label' in data else ""
    songwriter = data['songwriter'] if 'songwriter' in data else ""

    if artist:
        m['artist'] = [artist]
    if title:
        m['title'] = [title]
    if album:
        m['album'] = [album]
    if label:
        m['organization'] = [label]
    if songwriter:
        m['composer'] = [songwriter]

    if artist or title or album or label or songwriter:
        print("Updating [{}] | Artist: {} | Track: {} | Album: {} | Label: {} | Composer: {}"
              .format(relative_filename, artist, title, album, label, songwriter))
        m.save()


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


def parse_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data[row['path']] = row

    print('csv size: {} lines'.format(len(csv_data)))


def init():
    parse_csv("songs.csv")
    parse_dir(root_dir)


if len(sys.argv) > 1:
    print("")
    print("Sync MP3 metadata from CSV file: ".format(root_dir))
    print("")

    root_dir = re.sub(r'([^/])$', r'\1/', os.path.abspath(sys.argv[1]))
    init()

else:
    print("")
    print("Syncs CSV data (songs.csv) with each mp3 recursively in directory\n")
    print("    python {} DIRECTORY".format(sys.argv[0]))
