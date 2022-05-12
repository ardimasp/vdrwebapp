<template>
     <v-card
      style="background-color: #9155fd;"
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
        <v-col class="ml-2">
                <v-card-title class="ml-2">{{ this.dataTitle }}</v-card-title>
        </v-col>
        <v-col md="auto" class="mt-3">
          <v-btn icon>
              <v-icon>{{icons.mdiDownload}}</v-icon>

          </v-btn>
        </v-col>
        <v-col lg="2" class="mt-3">
          <v-btn icon @click="closeOverlay()">
              <v-icon>{{icons.mdiCloseThick}}</v-icon>

          </v-btn>
        </v-col>
      </v-row>
        <!-- <VtkContent
            :divWidthProp="800"
            :divHeightProp="500"
        /> -->
      <v-carousel height="800">
        <v-carousel-item min-width="500"
          v-for="(item, i) in this.images"
          :key="i"
          :src="item"
          reverse-transition="fade-transition"
          transition="fade-transition"
        ></v-carousel-item>
      </v-carousel>
    </v-card>

</template>

<script>

// import VtkCard from '../viewer/VtkCard.vue'
// import VtkContent from '../viewer/VtkContent.vue'

import {mdiDownload, mdiCloseThick} from "@mdi/js"


export default {
  components:{
    // VtkContent,

  },
  name: "CardContent",
  props: {
    dataD: Array,
    dataTitle: String
  },
  data: function(){
    return{
      loading: false,
      selection: 1,
      datacard: this.dataD,
      images: [],
      imgsort: null,
      sortitems: ['Oil Volume', 'Gas Volume', 'Mix oil & gas volume'],
      icons:{
        mdiDownload,
        mdiCloseThick
      }
    }
  },
  methods: {

     closeOverlay:function(){
      var over = false
      this.$emit('click', over)
    },
  },
  mounted: function() {
    this.images = this.datacard
    console.log(this.images)

  }
}
</script>

<style lang="css" scoped>
.v-card{
  background-color: #9155FD;
}
</style>
