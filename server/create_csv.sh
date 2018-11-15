#!/bin/bash
sqlite3 -header -csv ./songs.sqlite "select artist,track,album,songwriter,label,path from songs order by path asc" > songs.csv
