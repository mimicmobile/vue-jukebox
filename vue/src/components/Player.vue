<template>
  <div class="player-base">
    <audio
      :src="currentSongUrl"
      id="player"
      ref="player"
      v-on:ended="$emit('player-track-ended')"
    >
    </audio>

    <div :class="playingBg" class="controls-base">
      <div class="controls-box no-select">
        <i @click="playerFr()" class="material-icons">fast_rewind</i>
        <i @click="playerPlay()" class="material-icons">{{ playPauseSrc }}</i>
        <i @click="playerFf()" class="material-icons">fast_forward</i>
      </div>
    </div>
    <div :class="playingBg" class="now-playing">
      <div class="now-playing-inner">
        <div class="now-playing-title">
          <span v-if="currentSong.artist">Now Playing..</span>
          <span v-else>Choose a song</span>
        </div>
        <transition>
          <div v-if="currentSong.artist" class="now-playing-track-info">
            <div>
              Artist: {{ currentSongArtist }}
            </div>
            <div>
              Track: {{ currentSongTrack }}
            </div>
            <div>
              Album: {{ currentSongAlbum || "Unknown" }}
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
  import VueTimers from 'vue-timers/mixin'

  let origTitle = document.title

  export default {
    name: 'jukePlayer',
    mixins: [VueTimers],
    props: {
      currentSong: Object,
      playerPlay: Function,
      playerFf: Function,
      playerFr: Function,
    },
    data: () => ({
      audio: undefined,
      isPlaying: false,
    }),
    timers: {
      remaining: {
        time: 1000,  // 1s
        autostart: false,
        repeat: true,
      }
    },
    computed: {
      playPauseSrc() {
        return this.isPlaying ? "pause" : "play_arrow"
      },

      currentSongUrl() {
        return this.currentSong.url
      },
      currentSongArtist() {
        return this.currentSong.artist
      },
      currentSongTrack() {
        return this.currentSong.track
      },
      currentSongAlbum() {
        return this.currentSong.album
      },
      playingBg() {
        return this.currentSong.color_class !== undefined ? this.currentSong.color_class : "red"
      }
    },
    methods: {
      remaining() {
        if (this.isPlaying) {
          let time = Math.round(this.audio.currentTime - this.audio.duration) * -1
          if (!time) return

          let minutes = Math.floor(time / 60)
          let seconds = ("0" + (time % 60)).slice(-2)

          this.$emit('remaining-time-update', "-" + minutes + ":" + seconds)
        }
      },
      playAudio() {
        this.isPlaying = true
        this.remaining()
        this.audio.play()
        this.$timer.start('remaining')
        document.title = this.currentSong.artist + " - " + this.currentSong.track
      },
      pauseAudio() {
        this.isPlaying = false
        this.audio.pause()
        this.$timer.stop('remaining')
        document.title = origTitle
      },
      playPauseToggle() {
        if (this.isPlaying) {
          this.pauseAudio()
        } else {
          this.playAudio()
        }
      },
    },
    watch: {
      currentSong() {
        let wasPlaying = this.isPlaying;
        console.log('wp', wasPlaying)
        //this.audio.pause()
        //this.audio.load()

        if (wasPlaying) {
          this.playAudio()
        }
      }
    },
    mounted() {
      this.audio = this.$el.querySelectorAll('audio')[0]

      let vm = this
      this.audio.addEventListener('error', function () {
        if (this.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) {
          vm.$emit('network-error')
        }
      }, true);
    }
  }
</script>

<style>
  .now-playing {
    position: relative;
    margin: 8px;
    padding: 6px;
    border-radius: 2px;
    font-family: 'Arcade', 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 1em;
    word-wrap: break-word;
    word-spacing: 3px;
  }

  .now-playing-inner {
    display: flex;
    padding-top: 6px;
    padding-bottom: 6px;
    background-color: #fff;
    flex-direction: column;
    opacity: 0.9;
    align-items: start;
    justify-content: start;
  }

  .now-playing-title {
    font-size: 1.2em;
    max-height: 2.4em;
    line-height: 1.2em;
    margin: 0 20px;
  }

  .now-playing-track-info {
    display: flex;
    flex-direction: column;
    align-items: start;
    justify-content: start;
    margin: 10px 20px 10px;
  }

  .now-playing-track-info div {
    font-size: 1em;
    margin-top: 4px;
    margin-bottom: 4px;
    overflow: hidden;
    max-height: 2em;
    line-height: 1em;
    text-align: start;
  }

  .controls-base {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 2px;
    margin: 8px;
    padding: 6px;
  }

  .controls-box {
    display: flex;
    padding: 2px;
    background-color: #fff;
    justify-content: space-evenly;
    opacity: 0.9;
    width: 100%;
  }

  .controls-box i {
    color: #000;
    cursor: pointer;
    font-size: 40px;
  }

  .controls-box i:active {
    transform: translateY(3px);
  }

  .player-base {
    position: relative;
    display: flex;
    flex-direction: column;
    flex: 1;
    margin-bottom: 20px;
  }

</style>
