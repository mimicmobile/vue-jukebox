import os
import random
import sqlite3
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, send_from_directory, abort, Response
from flask_compress import Compress
from hashids import Hashids

SEED = str(os.getenv('SEED'))
DB_FILE = os.getenv('DB_FILE')
STATIC_URL = os.getenv('STATIC_URL')
STATIC_DIR = os.getenv('STATIC_DIR')
RANDOMIZE = os.getenv('RANDOMIZE')
ENCODE_SONGS = os.getenv('ENCODE_SONGS')
START_TRACK = os.getenv('START_TRACK')

SONGS_PER_PAGE = 10
SESSION_TIMEOUT_HOURS = 4
COLOR_INDEX = 1


def songs_encoded():
    return int(ENCODE_SONGS) == 1


def songs_randomized():
    return int(RANDOMIZE) == 1


STATIC_URL_DEFAULT = '/song' if songs_encoded() else '/static'
STATIC_FOLDER = 'static' if not songs_encoded() else None


def static_url():
    return STATIC_URL or STATIC_URL_DEFAULT


COLORS = ['green', 'orange', 'red', 'purple', 'blue']


def get_color():
    global COLOR_INDEX

    if COLOR_INDEX == len(COLORS) - 1:
        COLOR_INDEX = 0
    else:
        COLOR_INDEX += 1
    return COLORS[COLOR_INDEX]


app = Flask(__name__, static_folder=STATIC_FOLDER)
Compress(app)


def get_db():
    db = getattr(Flask, '_database', None)
    if db is None:
        db = Flask._database = sqlite3.connect(DB_FILE)
        db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), single=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if single else rv


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:filename>')
def custom_static(filename):
    if str(filename).endswith('mp3'):
        abort(403)
    return send_from_directory('static', filename)


@app.route('/song/<key>/<encoded_track>')
def song(key, encoded_track):
    if not key_valid(key):
        abort(403)

    h = Hashids(SEED + key)
    decoded_row = h.decode(encoded_track)
    if len(decoded_row) > 0:
        rowid = h.decode(encoded_track)[0]
    else:
        abort(403)

    selected_row = query_db('select rowid, * from songs WHERE rowid=?', (rowid,), single=True)

    root_dir = os.path.dirname(__file__)
    song_filename = os.path.basename(selected_row['path'])
    subdir = selected_row['path'].replace(song_filename, '')

    print("Serving [{} - {}] to session [{}] expiring [{}]"
          .format(selected_row['artist'], selected_row['track'], key, datetime.fromtimestamp(decode_key(key))
                  + timedelta(hours=SESSION_TIMEOUT_HOURS)))

    return send_from_directory(os.path.join(root_dir, 'static', subdir),  song_filename)


@app.route('/<string:text>', methods=['GET'])
def catch_all(text):
    root_dir = os.path.dirname(__file__)
    real_file = os.path.join(root_dir, 'static', text)
    if os.path.isfile(real_file):
        return send_from_directory(os.path.join(root_dir, 'static'), text)
    else:
        index_file = os.path.join(root_dir, 'static', text, 'index.html')
        if os.path.isfile(index_file):
            return send_from_directory(os.path.join(root_dir, 'static', text), 'index.html')
        else:
            return abort(404)


@app.route('/songs')
@app.route('/songs/<int:offset_param>')
def songs(offset_param=0):
    key = request.headers.get('X-Juke-Key')
    if not key_valid(key):
        h = Hashids(SEED)
        key = generate_key(h)
        print("Generated new key [{}]".format(key))

    list_length = query_db('select count(rowid) from songs', single=True)[0]

    offset_start = min(offset_param, list_length)
    offset_end = min(offset_param + SONGS_PER_PAGE, list_length)

    if offset_param > list_length or offset_start == offset_end:
        return jsonify_response(key, [])

    song_list = query_db('select rowid, * from songs {}'.format(
        offset_sql(key, list_length, offset_start, offset_end))
    )

    rows = [parse_row(song_row, key, index, offset_param) for index, song_row in enumerate(song_list)]
    return jsonify_response(key, rows)


def jsonify_response(key, json):
    response = jsonify(json)
    response.headers['X-Juke-Key'] = key
    return response


def parse_row(song_row, key, index, offset_param):
    d = dict(song_row)

    if songs_encoded():
        h = Hashids(SEED + key)

        d['url'] = "{}/{}/{}".format(static_url(), key, h.encode(d['rowid']))
    else:
        d['url'] = "{}/{}".format(static_url(), d['path'])

    del d['path']
    del d['rowid']

    d['id'] = offset_param + index + 1
    d['color_class'] = get_color()

    return d


def generate_key(h):
    timestamp = int(datetime.timestamp(datetime.now()))
    return h.encode(timestamp)


def decode_key(key):
    h = Hashids(SEED)
    key = h.decode(key)

    if len(key) > 0:
        return key[0]
    return 0


def key_valid(key):
    key = decode_key(key)
    if key:
        return (datetime.fromtimestamp(key)
                + timedelta(hours=SESSION_TIMEOUT_HOURS) > datetime.now())
    return False


def position_start_track(row_order):
    if START_TRACK:
        song = query_db('SELECT rowid FROM songs WHERE path=?', (START_TRACK,), single=True)
        if song:
            row_order.insert(0, row_order.pop(row_order.index(song['rowid'])))
    return row_order


def offset_sql(key, length, start, end):
    if songs_randomized():
        r = random.Random(key)
        row_order = r.sample(range(1, length + 1), length)
        row_order = position_start_track(row_order)
        return "order by {} limit {}".format(", ".join(["rowid={} DESC".format(i) for i in row_order[start:end]]),
                                             end - start)
    else:
        return "limit {}, {}".format(start, SONGS_PER_PAGE)


if __name__ == '__main__':
    app.run()
