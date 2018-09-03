<template>
  <div class="player-base">
    <img class="juke-img" src="../../assets/juke.png"/>
    <div class="player-buttons">
      <img @click="$emit('player-fr')" class="icon" src="../../assets/fr.png" />
      <img @click="$emit('player-play')" class="play icon" :src="playPauseSrc" />
      <img @click="$emit('player-ff')" class="icon" src="../../assets/ff.png" />
    </div>
    <audio id="player" ref="player" v-on:ended="$emit('player-track-ended')">
      <source :src="currentSongUrl">
      Your browser does not support the audio element.
    </audio>
  </div>
</template>

<script>
  import VueTimers from 'vue-timers/mixin'

  export default {
    name: 'jukePlayer',
    mixins: [VueTimers],
    props: {
      isPlaying: Boolean,
      currentSong: Object
    },
    timers: {
      remaining: {
        time: 1000,  // 1s
        autostart: false,
        repeat: true,
      }
    },
    computed: {
      playPauseSrc() {
        let file = this.isPlaying ? "pause.png" : "play.png"
        return require(`../../assets/${file}`)
      },
      currentSongUrl() {
        return this.currentSong.url
      }
    },
    methods: {
      remaining() {
        if (this.isPlaying) {
          let time = Math.round(this.$refs.player.currentTime - this.$refs.player.duration) * -1
          if (!time) return

          let minutes = Math.floor(time / 60)
          let seconds = ("0" + (time % 60)).slice(-2)

          this.$emit('remaining-time-update', "-" + minutes + ":" + seconds)
        }
      },
      playAudio() {
        this.remaining()
        this.$refs.player.play()
        this.$timer.start('remaining')
      },
      pauseAudio() {
        this.$refs.player.pause()
        this.$timer.stop('remaining')
      }
    },
    watch: {
      currentSong() {
        this.$refs.player.pause()
        this.$refs.player.load()
        if (this.isPlaying) {
          this.playAudio()
          document.title = this.currentSong.artist + " - " + this.currentSong.track
        }
      },
      isPlaying() {
        if (!this.isPlaying) {
          this.pauseAudio()
          document.title = "vue-jukebox"
        } else {
          this.playAudio()
        }
      }
    },
  }
</script>

<style>
  .player-base {
    position: relative;
    height: 600px;
    width: auto;
  }

  .icon {
    cursor: pointer;
    width: 30px;
    height: 30px;
  }

  .juke-img {
    height: 100%;
  }

  .player-buttons {
    position: absolute;
    overflow: auto;
    left: 172px;
    top: 256px;
    width: 102px;
  }

</style>
