<template>
  <vue-draggable-resizable 
    :grid=[10,10]  
    :h="h"
    :w="w"
    :resizable="isShown"
    :drag-handle="'.drag-handle'"
    :style="{border: 'none'}"
    :x="x"
    :y="y"
    @resizing="onResize"
    >
    <v-system-bar
      class="drag-handle"
      color="primary"
      style="border-radius: 5px 5px 0px 0px; "
      window
    >
      <span class="white--text text-subtitle-1">{{ title }}</span>
      <v-spacer></v-spacer>

      <v-icon 
        color="white"
        @click="isShown = !isShown"
        small
      >
        {{ isShown ? icons.mdiWindowMinimize:icons.mdiWindowMaximize }}
      </v-icon>

    </v-system-bar>
    <div 
        v-show="isShown" 
        :style="styleContainer"
        class='overflow-auto'
    >
        <vtk-content
            :divWidthProp="divWidth"
            :divHeightProp="divHeight"
        ></vtk-content>
    </div>
    
  </vue-draggable-resizable>
</template>

<script>
import {
  mdiWindowMinimize,
  mdiWindowMaximize,
} from '@mdi/js'
import VueDraggableResizable from 'vue-draggable-resizable'

import VtkContent from './VtkContent.vue'

export default {
  data: function () {
    return {
      isShown: true,
      height: null,
      width: null,
      styleContainer: {
        border: '2px solid grey',
        borderTopStyle: 'none',
        borderRadius: '0px 0px 5px 5px',
        width: null,
        height: 'auto',
        backgroundColor: 'white' 
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
  },
  components: {
    VueDraggableResizable,
    VtkContent
  },
  methods: {
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
</style>