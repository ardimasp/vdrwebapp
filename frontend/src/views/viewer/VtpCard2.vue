<template>
  <v-card>
    <!-- for progresss bar -->
    <slot></slot>
    <div 
        v-show="isShown" 
        :style="styleContainer"
        class='overflow-auto'
    >
        <vtp-content
            :divWidthProp="divWidth"
            :divHeightProp="divHeight"
            :dataVtp="dataVtp"
            :vtpIndex="vtpIndex"
            ref="vtpcontent"
        ></vtp-content>
    </div>
    
  </v-card>
</template>

<script>
import {
  mdiWindowMinimize,
  mdiWindowMaximize,
} from '@mdi/js'

import VtpContent from './VtpContent.vue'

export default {
  data: function () {
    return {
      isShown: true,
      height: null,
      width: null,
      styleContainer: {
        borderRadius: '0px 0px 5px 5px',
        width: '100%',
        height: 'auto',
      },
      divWidth: 500,
      divHeight: 500,
    }
  },
  props: {
    x: {
      type: Number,
      default: 0,
    },
    y: {
      type: Number,
      default: 0,
    },
    title: {
      type: String,
      default: 'Title',
    },
    w: {
      type: [Number, String],
      default: 'auto',
    },
    h: {
      type: [Number, String],
      default: 'auto',
    },
    dataVtp: {
      type: Object,
      default: null,
    },
    vtpIndex: {
      type: Number,
      default: 0
    }
  },
  watch: { 
    // dataVtp: function(newVal, oldVal) { // watch it
    //   console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    // }
  },
  components: {
    VtpContent
  },
  methods: {
    changeColorMapName(colormapname,gain){
       this.$refs.vtpcontent.changeColorMapName(colormapname,gain)
    },
    setGain(gain) {
      this.$refs.vtpcontent.setGain(gain)
    },
    removeActor(index) {
      this.$refs.vtpcontent.removeActor(index)
    },
    onResize: function (_x, _y, width, height) {
        this.width = width
        this.height = height 
        this.styleContainer.width = width + 'px'
        this.styleContainer.height = height  - 32 + 'px' // see https://vuetifyjs.com/en/api/v-system-bar/#props-window
        this.divWidth = width - 4 // trial and error --> need to be investigated later
        this.divHeight = height - 34 // trial and error --> need to be investigated later
    },
  },
  beforeMount() {
    if (this.w != 'auto'){
      this.styleContainer.width = this.w + 'px'
      this.divWidth = this.w - 4
    }

    if (this.h != 'auto'){
      this.styleContainer.height = this.h - 32 + 'px'
      this.divHeight = this.h - 34
    }
  },
  setup() {
    return {
      icons: {
        mdiWindowMinimize,
        mdiWindowMaximize,
      }
    }
  }
}
</script>

<style scoped>
.shown {
  border: 'none';
  background-color: 'white';
}

.overflow-auto {
  margin: auto;
}
</style>