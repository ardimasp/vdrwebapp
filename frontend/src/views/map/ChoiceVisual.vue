<template>
  <!-- <v-hover v-slot="{ hover }"> -->
      <div>
    <v-card
      style="background-color: #f4f5fa;"

      :loading="loading"
      class="mx-auto my-12"
      max-width="500"
      max-height="500"
      width="500"
      height="300"
    >
      <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>

      <v-row 
      style="background-color: #9155fd;"
      no-gutters>
        <v-col  cols="auto"
                class="mr-auto">
            <v-card-title class="pa-2 ml-2 mt-2">Choose a visualization for {{ this.datacard.wellName }}</v-card-title>
        </v-col>
        
            <v-col  cols="auto">
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">

                    <v-btn class="pa-2 mr-6 mt-2" icon @click="closeOverlay()">
                        <v-icon  v-bind="attrs"
                      v-on="on">{{icons.mdiCloseThick}}</v-icon>

                    </v-btn>
                  </template>
                  <span>Close Overlay</span>
                </v-tooltip>
              </v-col> 
      </v-row>
 
      <v-row>
        <v-col>
         <v-radio-group class="ml-10" v-model="val">
            <v-radio
              v-for="type in visualizationType"
              :key="type"
              :label="type"
              :value="type"
              color="primary"

            ><template v-slot:label>
          <div class="primary--text">{{type}}</div>
        </template></v-radio>
          </v-radio-group>
        </v-col>     
      </v-row>
      <v-card-actions class="justify-center mt-4">
              <v-btn
              style="background-color: #00BFA5; color: white;"
              elevation="10"
              large
              text
              outlined
              :disabled="disabled"
              @click="choseImg()"
            >
              VISUALIZE
            </v-btn>
      </v-card-actions>

    </v-card>
     <v-overlay style="z-index: 99999" :absolute="true" :value="overlayAgain">
      <MapContent :dataD="this.chosenImgPath" :dataTitle="this.datacard.wellName" :allData="this.datacard" :visualType="this.val" v-on:click="changeOverlay"/>
    </v-overlay>
    </div>
</template>

<script>
import {mdiDownload, mdiCloseThick} from "@mdi/js"
// import {getImages} from '../showcase/MapEndPoint.js';

import MapContent from './MapContent.vue'


export default {
  components:{
    MapContent
  },
  name: "ChoiceCard",
  props: {
    dataDetail: Object,
    overlay: String
  },
  data: function(){
    return{
    val: null,
      loading: false,
      datacard: this.dataDetail,
      // info: undefined,
      icons:{
        mdiDownload,
        mdiCloseThick
      },
      overlayAgain: false,
      chosenImg: [],
      chosenImgPath: [],
      visualizationType: ['Viewer', 'Well log', 'Seismic']
    }
  },
  methods: {

    test(){
      var click = false
      this.$emit('input', click)
    },

    closeOverlay:function(){
      var over = false
      this.$emit('click', over)
    },

    choseImg:function(){
        this.chosenImg = this.val
        this.chosenImgPath = []
        this.chosenImgPath.push('/'+this.datacard.wellName+'/'+this.chosenImg)
        this.overlayAgain = true
    },

    changeOverlay(closeover){
      this.overlayAgain = closeover
    }
  },
 
  computed: {
    disabled() {
        return this.val === null; // or === 0   
    }
}
}
</script>
<style scoped>
.black--text /deep/ label {
    color: #777777;
}
</style>
