<template>
  <div class="juke-base" tabindex="-1" @keyup.space="playPauseToggle" @keyup.right="ffToggle" @keyup.left="frToggle">
    <juke-player
        :is-playing="isPlaying"
        :current-song="currentSong"
        :player-play="playPauseToggle"
        :player-fr="frToggle"
        :player-ff="ffToggle"
        ref="jukePlayer"
        @remaining-time-update="updateRemainingTime"
        @player-track-ended="ffToggle"
        @network-error="reloadSongs">
    </juke-player>
    <juke-list
        :songs="songs"
        :current-index="currentIndex"
        :is-playing="isPlaying"
        ref="jukeList"
        @loadMoreSongs="loadMoreSongs"
        @changeSource="changeSource"></juke-list>
  </div>
</template>

<script>
  import Vue from "vue"

  import List from './components/List.vue?shadow'
  import Player from './components/Player.vue?shadow'

  Vue.component('juke-list', List)
  Vue.component('juke-player', Player)

  import axios from "axios"

  const SONG_URI = '/songs'

  let axiosInstance

  export default {
    name: 'app',
    methods: {
      updateRemainingTime(time) {
        Vue.set(this.songs[this.computedIndex], 'remainingTime', time)
      },
      frToggle() {
        this.computedIndex = Math.max(0, this.currentIndex - 1)
      },
      ffToggle() {
        if ((this.currentIndex + 1) === this.songs.length) {
          // Hit the last song, stop playing
          this.stopPlaying()
        } else {
          this.computedIndex += 1
        }

      },
      playPauseToggle() {
        this.isPlaying = !this.isPlaying

        this.startPlaying()
        if (this.isPlaying) {
          this.$refs.jukePlayer.playAudio()
        } else {
          this.$refs.jukePlayer.pauseAudio()
        }
      },
      changeSource(index) {
        this.startPlaying()

        if (this.isPlaying && index === this.currentIndex) {
          // Pause when same track is double tapped
          this.isPlaying = false
        } else {
          this.computedIndex = index

          this.isPlaying = true
        }
      },
      startPlaying() {
        if (this.currentIndex === -1) this.computedIndex = 0
      },
      stopPlaying() {
        this.computedIndex = -1
        this.isPlaying = false
      },
      loadMoreSongs() {
        if (this.busy) return
        this.busy = true

        this.getSongs(SONG_URI + "/" + this.page)
      },
      parseSongs(response) {
        let key = response.headers['x-juke-key']

        if (this.jukeKey !== key) {
          this.setJukeKey(key)
        }


        this.page += 10
        this.songs = this.songs.concat(response.data)
      },
      reloadSongs() {
        if (this.busy) return

        this.isPlaying = false
        this.page = 0
        this.currentIndex = -1
        this.songs = []

        this.getSongs()
      },
      getSongs(url = SONG_URI) {
        axiosInstance.get(url)
          .then(response => this.parseSongs(response)).then(() => this.busy = false)
      },
      setJukeKey(key) {
        this.jukeKey = key
        axiosInstance.defaults.headers['X-Juke-Key'] = this.jukeKey
      }
    },
    data: () => ({
      songs: [],
      isPlaying: false,
      currentIndex: -1,
      remainingTime: "",
      page: 0,
      jukeKey: null,
      busy: true
    }),
    mounted() {
      axiosInstance = axios.create()
      this.getSongs()
    },
    computed: {
      currentSong() {
        return this.currentIndex === -1 ? {} : this.songs[this.currentIndex]
      },
      computedIndex: {
        get: function () {
          return this.currentIndex
        },
        set: function (index) {
          let previousIndex = this.currentIndex
          if (index === previousIndex) return

          if (previousIndex !== null && previousIndex !== -1) {
            Vue.set(this.songs[previousIndex], 'remainingTime', "")
          }

          this.currentIndex = index

          if (index === -1) return

          Vue.set(this.songs[index], 'remainingTime', "")
          this.$refs.jukeList.scrollToCurrent(index)
        },
      }

    }
  }

</script>

<style>
  body {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #000;
  }

  @font-face {
    font-family: 'Arcade';
    src: url('../assets/fonts/arcade_classic.ttf') format('truetype');
  }

  @font-face {
    font-family: 'Material Icons';
    font-style: normal;
    font-weight: 400;
    src: local('Material Icons'), local('MaterialIcons-Regular'), url('../assets/fonts/material-icons.woff2') format('woff2');
  }

  .material-icons {
    font-family: 'Material Icons' !important;
    font-weight: normal;
    font-style: normal;
    font-size: 18px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
  }

  .juke-base {
    font-family: 'Arcade', 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-between;
    outline-style: none;
    box-shadow: none;
    border-color: transparent;
    height: inherit;
  }

  .red {
    transition: all 0.5s linear;
    background-color: #930d28;
    border-color: #930d28;
  }

  .green {
    transition: all 0.5s linear;
    background-color: #1f7a34;
    border-color: #1f7a34;
  }

  .purple {
    transition: all 0.5s linear;
    background-color: #331256;
    border-color: #331256;
  }

  .orange {
    transition: all 0.5s linear;
    background-color: #a54d00;
    border-color: #a54d00;
  }

  .blue {
    transition: all 0.5s linear;
    background-color: #1b34ad;
    border-color: #1b34ad;
  }

  .no-select {
    -webkit-user-select: none; /* webkit (safari, chrome) browsers */
    -moz-user-select: none; /* mozilla browsers */
    -khtml-user-select: none; /* webkit (konqueror) browsers */
    -ms-user-select: none; /* IE10+ */
  }

</style>
