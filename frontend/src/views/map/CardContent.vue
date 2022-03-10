<template>
  <!-- <v-hover v-slot="{ hover }"> -->
    <v-card
      :loading="loading"
      class="mx-auto my-12"
      max-width="900"
      max-height="900"
    >
      <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>
 
      <!-- <v-card-title class="ml-2">{{ this.datacard.title }}</v-card-title> -->
      <v-row class="ml-2">
        <v-col md='4'>
            <v-card-title class="ml-2">{{ this.datacard.title }}</v-card-title>

        </v-col>
        <v-col md="1"
          class="ml-md-auto mt-1 mr-8">
          <v-btn icon>
              <v-icon>{{icons.mdiDownload}}</v-icon>

          </v-btn>
        </v-col>
      </v-row>
    
      <v-carousel height="600">
        <v-carousel-item min-width="500"
          v-for="(item, i) in this.images"
          :key="i"
          :src="item"
          reverse-transition="fade-transition"
          transition="fade-transition"
        ></v-carousel-item>
      </v-carousel>

      <!-- <v-card-actions>
      <v-btn
        color="deep-purple lighten-2"
        text
        @click="reserve"
      >
        Reserve
      </v-btn>
    </v-card-actions> -->

    </v-card>
  <!-- </v-hover> -->
</template>

<script>
import {mdiDownload} from "@mdi/js"
// import VtkContent from '../viewer/VtkContent.vue'
import VtkCard from '../viewer/VtkCard.vue'


export default {
  component:{
    // VtkContent,
    VtkCard
  },
  name: "Card",
  props: {
    dataDetail: Object,
  },
  data: function(){
    return{
      loading: false,
      selection: 1,
      datacard: this.dataDetail,
      images: [],
      imgsort: null,
      sortitems: ['Oil Volume', 'Gas Volume', 'Mix oil & gas volume'],
      icons:{
        mdiDownload
      }
    }
  },
  methods: {
    // reserve() {
    //   console.log(this.details)
    // },
    selectedImg:function(){
      var chosensort = this.imgsort
      console.log(chosensort)
      const prev = this.images
      var lucky = prev.filter(function(prev) {
        return prev != chosensort;
      });
      this.images = []
      this.images.push(chosensort)
      this.images.push(...lucky)
      console.log(this.images)
      this.$forceUpdate();
    },
  },
  mounted: function() {
    this.images = this.datacard.images
    console.log(this.images)

  }
}
</script>
