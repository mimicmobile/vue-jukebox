# Vue Jukebox

`vue-jukebox` is a project that is part web component jukebox and part Python backend service.

It can be used as either a standalone web component or as a vue component

## Features
- Run directly as a web component in any project, vue or otherwise.
- Encode mp3 links to help obfuscate
- Randomize list of songs
- Keyboard shortcuts to control playback (right, left, space)

## Screenshots
<a href="screenshot.png"><img src="screenshot.png" width="400"></a>

## TODO
- Instantiate component with configuration props
- Customize colors, logo and background, etc
- Allow JSON path to be provided for users not intending to use backend service

## Web component - Getting started 
- Build web component
`cd vue && ./build_wc.sh`
- Copy necessary files and directories from dist/ (`juke-box.min.js` `fonts/` `img/`) into your project
- If embedding in existing project, you use `demo.html` as a "basis".  Make sure to include the required fonts, `juke-box.js`, the jukebox image and optionally the `polyfill webcomponents` javascript library.

## Vue component - Getting started
TODO

## Backend service - Testing
Service can be started in Docker Compose: `docker-compose up` or by running `./start.sh`.  The static volume is by default mounted under `/tmp/vue-jukebox/static/`

## Backend service - Docker (prod)
Optionally modify `server/variables.env` and then build your container
```bash
docker run --rm \
--env-file server/variables.env \
--name flask-vue-jukebox mimicmobile/flask-vue-jukebox:latest
```

Make sure to provide a static files volume to the container under `/usr/local/app/static`

_You can serve your entire project from the backend service by creating `/usr/local/app/index.html`_


## Backend service - MP3s
Songs should be put in the static files volume/directory under `/usr/local/app/static/mp3s/`

## License

    Copyright 2018 Mimic Mobile Limited

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
