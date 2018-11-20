#!/bin/bash

SONG_DB="songs.sqlite"
SERVER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [[ -e "./variables.env" ]]; then
    set -a; . ./variables.env
fi

if [[ -z "$RANDOMIZE" ]]; then
    RANDOMIZE=1
fi

if [[ -z "$ENCODE_SONGS" ]]; then
    ENCODE_SONGS=1
fi

if ! [[ -z "$DOCKER_BUILD_DATE" ]]; then
    echo ""
    echo "Build date ($DOCKER_BUILD_DATE) VCS ref ($DOCKER_VCS_REF)"
fi

SEED=$(date +'%s')

STATIC_DIR="${SERVER_DIR}/static/"

if ! [[ -d "$STATIC_DIR" ]]; then
  echo "  $STATIC_DIR does not exist!  Creating directory.."
  mkdir $STATIC_DIR
fi

if ! [[ -d "$STATIC_DIR" ]]; then
    echo ""
    echo "STATIC_DIR '$STATIC_DIR' does not exist!  Aborting launch.."
    exit 1
else
    SCRIPT_PATH="${SERVER_DIR}/create_mp3_db.py"
    if ! [[ -e "$SCRIPT_PATH" ]]; then
        echo ""
        echo "Couldn't find db creation script at '$SCRIPT_PATH'!  Aborting!"
        exit 1
    else
        python $SCRIPT_PATH $STATIC_DIR

        DB_FILE=${SERVER_DIR}/${SONG_DB}
        if ! [[ -e "$DB_FILE" ]]; then
            echo "Could not find song db: $DB"
            echo "Aborting!"
            exit 1
        fi
    fi
fi

# Setup default port
if [[ -z "$PORT" ]]; then
  PORT=5001
fi


cd $SERVER_DIR

echo ""
gunicorn \
  -w 1 \
  -k gevent \
  -e SEED="$SEED" \
  -e DEBUG="$DEBUG" \
  -e RANDOMIZE="$RANDOMIZE" \
  -e ENCODE_SONGS="$ENCODE_SONGS" \
  -e DB_FILE="$DB_FILE" \
  -e STATIC_URL="$STATIC_URL" \
  -e STATIC_DIR="$STATIC_DIR" \
  -e START_TRACK="$START_TRACK" \
  -b 0.0.0.0:$PORT \
  main:app

cd ..
