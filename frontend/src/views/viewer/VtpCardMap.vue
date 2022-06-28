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

    :draggable="true"
    style="z-index: 9999;"
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
    
    <!-- for progresss bar -->
    <slot></slot>
    <div 
        v-show="isShown" 
        :style="styleContainer"
        class='overflow-auto'
    >
    <div class="pa-4 text-no-wrap ">

          <v-row
        :align="align"
        no-gutters
        style="height: 150px;"
      >
      <v-col>
           <v-autocomplete 
              dense
              v-model="selectedValue"
              :items="chosenValue"
              label="Selected"
            ></v-autocomplete>
      </v-col>
      <v-col class="ml-4">
            <!-- <v-text-field
                label="Gain"
                v-model="gain"
                type="number"
              ></v-text-field> -->
            <!-- <v-subheader class="pl-0 pt-0">
              Gain
            </v-subheader> -->
            <v-slider class="pl-0 mt-1"
            label="Gain"
              :disabled="selectedValue == null"
              dense
              :max="max"
              :min="min"
              v-model="gain"
              :thumb-size="24"
              thumb-label="always"
              @change="changeColorMapName"
            ></v-slider>
      </v-col>
      <v-col class="ml-4">
            <v-autocomplete
              :disabled="selectedValue == null"
              dense
              v-model="value"
              :items="items"
              label="Standard"
              @change="changeColorMapName"

            ></v-autocomplete>
      </v-col>
          </v-row>
        </div>
        <vtp-content
            :divWidthProp="divWidth"
            :divHeightProp="divHeight"
            :dataVtp="dataVtp"
            :vtpIndex="vtpIndex"
            ref="vtpcontent"
        ></vtp-content>
    </div>
    
  </vue-draggable-resizable>
</template>

<script>
import {
  mdiWindowMinimize,
  mdiWindowMaximize,
} from '@mdi/js'
import VueDraggableResizable from 'vue-draggable-resizable'

import VtpContent from './VtpContent.vue'

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
      gain:1,
      value:"2hot"
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
    },
    chosenValue:{
      type:Array,
      default:null
    }
  },
  watch: { 
    // dataVtp: function(newVal, oldVal) { // watch it
    //   console.log('Prop changed: ', newVal, ' | was: ', oldVal)
    // },
    selectedValue: function(newVal) {
      if(this.chosenValue == null || this.chosenValue.length == 0) return

      this.selectedIndex = this.chosenValue.indexOf(newVal)
    }
  },

  components: {
    VueDraggableResizable,
    VtpContent
  },
  methods: {
    // changeColorMapName(colormapname,gain){
    //    this.$refs.vtpcontent.changeColorMapName(colormapname,gain)
    // },
    changeColorMapName(){
       this.$refs.vtpcontent.changeColorMapName(this.value,this.gain)
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
  },
  // mounted(){
  //   console.log(this.dataVtp)
  // }
}
</script>

<style scoped>
.shown {
  border: 'none';
  background-color: 'white';
}
</style>