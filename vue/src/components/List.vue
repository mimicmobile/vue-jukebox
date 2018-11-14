<template>
  <div class="scrollbar" ref="Scrollbar" v-on:scroll="onScroll">
    <div class="list-holder no-select">
      <div v-for="(song, index) in songs" :song="song" :key="song.id" class="list-cont" :class="song.color_class"
           ref="songs"
           @click="changeSource(index)">
        <div class="list-row">
          <div class="list-left list-side">
            <img class="list-left list-side" src="../../assets/topleft.png"/>
            <span class="track-num">{{ song.id }}.</span>
          </div>
          <div class="list-middle">
            <span>{{ song.artist }}</span>
          </div>
          <div class="list-right list-side">
            <img class="list-right list-side" src="../../assets/topright.png"/>
            <i class="material-icons material-icons-pos">{{ songIcon(index) }}</i>
          </div>
        </div>
        <div class="list-row">
          <img class="list-side list-left" src="../../assets/bottomleft.png"/>
          <div class="list-middle">
            <span>{{ song.track }}</span>
          </div>
          <div class="list-right list-side">
            <img class="list-side list-right" src="../../assets/bottomright.png"/>
            <span class="remaining-time">{{ song.remainingTime }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import VueTimers from 'vue-timers/mixin'

  const throttle = (func, limit, c) => {
    let inThrottle
    return function () {
      const args = arguments
      const context = c || this
      if (!inThrottle) {
        func.apply(context, args)
        inThrottle = true
        setTimeout(() => inThrottle = false, limit)
      }
    }
  }

  export default {
    name: 'jukeList',
    mixins: [VueTimers],
    props: {
      songs: Array,
      currentIndex: Number,
      isPlaying: Function,
      changeSource: Function,
    },
    created: function () {
      this.throttledLoad = throttle(this.loadMoreSongs, 250, this)
    },
    methods: {
      songIcon(index) {
        if (index === this.currentIndex) {
          return this.isPlaying() ? "volume_up" : "pause"
        }
        return ""
      },
      loadMoreSongs() {
        this.$emit('loadMoreSongs')
      },
      scrollToCurrent(index) {
        this.$refs.songs[index].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'})
      },
      onScroll() {
        let scrollBar = this.$refs.Scrollbar
        if ((scrollBar.scrollHeight - scrollBar.scrollTop) - scrollBar.offsetHeight - 125 <= 0) {
          this.throttledLoad()
        }
      }
    }
  }
</script>

<style>
  .scrollbar {
    margin: 4px;
    min-width: 280px;
    overflow-y: scroll;
    overflow-x: hidden;
    display: flex;
    flex: 1;
    position: relative;
    height: inherit;
  }

  ::-webkit-scrollbar {
    width: 4px;
    background: transparent;
  }

  ::-webkit-scrollbar-thumb {
    background: rgba(100, 100, 100, 0.5);
  }

  .list-holder {
    position: absolute;
    width: 100%;
  }

  .list-cont {
    position: relative;
    padding: 4px;
    margin: 4px;
    border-radius: 2px;
    cursor: pointer;
  }

  .track-num {
    position: absolute;
    font-family: 'Arcade', 'Avenir', Helvetica, Arial, sans-serif;
    left: 7px;
    font-size: 1em;
  }

  .remaining-time {
    position: absolute;
    font-family: 'Arcade', 'Avenir', Helvetica, Arial, sans-serif;
    margin-top: 9px;
    right: 1px;
    font-size: 1em;
  }

  .material-icons-pos {
    position: absolute;
    margin-top: 2px;
  }

  .list-row {
    position: relative;
    height: 30px;
    margin: 3px 0 3px 0;
    opacity: 0.9;
  }

  .list-left {
    position: absolute;
    left: 0;
  }

  .list-middle {
    position: absolute;
    display: flex;
    white-space: normal;
    background-color: #FFFFFF;
    left: 36px;
    right: 36px;
    height: 100%;
    justify-content: center;
    align-items: center;
  }

  .list-middle span {
    font-family: 'Arcade', 'Avenir', Helvetica, Arial, sans-serif;
    font-size: 1em;
    text-overflow: ellipsis;
    word-wrap: break-word;
    overflow: hidden;
    max-height: 2em;
    line-height: 1em;
    word-spacing: 3px;
    text-align: center;
  }

  .list-side {
    width: 37px;
    height: 30px;
  }

  .list-right {
    position: absolute;
    right: 0;
  }
</style>
