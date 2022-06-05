<template>
     <v-card
      style="background-color: #00796B;"
      class="mx-auto my-12"
      max-width="900"
      max-height="900"
      width="900"
      height="800"
    >
     <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>
      <v-row class="mb-2">
        <v-col class="ml-5 mt-5">
                <v-card-title class="ml-2">{{ this.dataTitle }}</v-card-title>
        </v-col>
        <v-col md="auto" class="mt-7">
          <!-- <v-btn icon>
              <v-icon>{{icons.mdiDownload}}</v-icon>

          </v-btn> -->

          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">

               <v-btn icon>
                  <v-icon  v-bind="attrs"
                v-on="on">{{icons.mdiDownload}}</v-icon>

              </v-btn>
            </template>
            <span>Download Data</span>
          </v-tooltip>

        </v-col>
        <v-col lg="2" class="mt-7">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">

               <v-btn icon @click="closeOverlay()">
                  <v-icon  v-bind="attrs"
                v-on="on">{{icons.mdiCloseThick}}</v-icon>

              </v-btn>
            </template>
            <span>Close Overlay</span>
          </v-tooltip>

          <!-- <v-btn icon @click="closeOverlay()">
              <v-icon>{{icons.mdiCloseThick}}</v-icon>

          </v-btn> -->
        </v-col>
      </v-row>
        <!-- <VtkContent
            :divWidthProp="800"
            :divHeightProp="500"
        /> -->
      <v-carousel height="400">
        <v-carousel-item min-width="500"
          v-for="(item, i) in this.images"
          :key="i"
          :src="item"
          reverse-transition="fade-transition"
          transition="fade-transition"
        ></v-carousel-item>
      </v-carousel>
      <v-simple-table class="ml-4" style="background-color: #00796B;" height="300px">
        <template v-slot:default>
        <tbody>
          
            <tr
                v-for="(item,i) in dataKeys"
                :key="i"
            >

                <td>{{ item }}</td>
                <td> {{ dataValues[i] }} </td>
            </tr>
        </tbody>
        </template>
    </v-simple-table>
    </v-card>
<!-- style="color: #2D1F54;" -->
</template>

<script>

// import VtkCard from '../viewer/VtkCard.vue'
// import VtkContent from '../viewer/VtkContent.vue'
import {displayImages} from '../showcase/MapEndPoint.js';

import {mdiDownload, mdiCloseThick} from "@mdi/js"


export default {
  components:{
    // VtkContent,

  },
  name: "CardContent",
  props: {
    dataD: Array,
    dataTitle: String,
    details: Object
  },
  data: function(){
    // console.log(this.details)
    return{
      loading: false,
      selection: 1,
      datacard: this.dataD,
      sD: this.details,
      showcaseDetails: [],
      images: [],
      imgsort: null,
      sortitems: ['Oil Volume', 'Gas Volume', 'Mix oil & gas volume'],
      icons:{
        mdiDownload,
        mdiCloseThick
      },
      dataKeys: [],
      dataValues: []
    }
  },
  methods: {

     closeOverlay:function(){
      var over = false
      // this.images = []
      this.images.length = 0
      this.$emit('click', over)
    },

    async imagesTake(imgInfo){
      let ims = []
      for (let i in imgInfo){

      ims.push(await displayImages(imgInfo[i]))
      }
      return ims
      
    }
  },
  async mounted() {
    // this.images = this.datacard
    var d = []
    for (let i in this.datacard){

      var valI = await displayImages(this.datacard[i])
      console.log(valI)
      d.push(valI)
    }

    this.images = d

    // this.images = this.imagesTake(this.datacard)
    //   console.log(valI)
    // this.images = valI
    console.log(this.images)
    this.showcaseDetails = this.sD
    console.log(this.showcaseDetails)
    this.dataKeys = Object.keys(this.showcaseDetails)
    console.log(this.dataKeys)
    this.dataValues = Object.values(this.showcaseDetails)
    console.log(this.dataValues)

  }
}
</script>

<style lang="scss" scoped>
.v-card{
  background-color: #9155FD;
    display: flex !important;
  flex-direction: column;
}

.v-simple-table{
   flex-grow: 1;
  overflow: auto;
}
</style>
