<template>
  <!-- <v-hover v-slot="{ hover }"> -->
      <div>
    <v-card
      :loading="loading"
      class="mx-auto my-12"
      max-width="400"
      max-height="400"
      width="400"
      height="400"
    >
      <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>

      <v-row no-gutters>
        <v-col  cols="auto"
                class="mr-auto">
            <v-card-title class="pa-2 ml-2 mt-4">{{ this.datacard.title }}</v-card-title>
        </v-col>
        
            <v-col  cols="auto">
                <v-btn class="pa-2 mr-6 mt-4" icon @click="closeOverlay()">
                    <v-icon>{{icons.mdiCloseThick}}</v-icon>

                </v-btn>
              </v-col> 
      </v-row>
 <!-- <v-row no-gutters>
    <p class="font-weight-bold mr-2 mt-0 mb-0">
      Bold text.
    </p>
 </v-row> -->

      <v-row >
        <v-col>
          <v-checkbox class="shrink ml-5 mr-0 mt-0" v-for="item in images" v-model="val" :key="item" :label="item" :value="item" ></v-checkbox>
        </v-col>     
      </v-row>
      <v-card-actions class="justify-center">
              <v-btn
              color="blue lighten-1"
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
      <CardContent :dataD="this.chosenImg" :dataTitle="this.datacard.title" v-on:click="changeOverlay"/>
    </v-overlay>
    </div>
  <!-- </v-hover> -->
</template>

<script>
import {mdiDownload, mdiCloseThick} from "@mdi/js"

import CardContent from './CardContent.vue'


export default {
  components:{
    CardContent
  },
  name: "ChoiceCard",
  props: {
    dataDetail: Object,
    overlay: String
  },
  data: function(){
    return{
    val: [],
      loading: false,
      selection: 1,
      datacard: this.dataDetail,
      images: this.dataDetail.images,
    //   imgsort: null,
      sortitems: ['Oil Volume', 'Gas Volume', 'Mix oil & gas volume'],
      icons:{
        mdiDownload,
        mdiCloseThick
      },
      overlayAgain: false,
      chosenImg: []
    }
  },
  methods: {
    selectedImg:function(){
      var chosensort = this.imgsort
      console.log(chosensort)
      const prev = this.images
      var lucky = prev.filter(function(prev) {
        return prev != chosensort;
      });
      var imag = []
      imag.push(chosensort)
      imag.push(...lucky)
      this.images = imag
      console.log(this.images)

    },

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
        console.log(this.chosenImg)
        this.overlayAgain = true
    },

    changeOverlay(closeover){
      this.overlayAgain = closeover
      console.log(closeover);
    }
  },
  mounted: function() {
    this.images = this.datacard.images
    // console.log(this.images)

  },
  computed: {
    disabled() {
        return this.val < 1; // or === 0   
    }
}
}
</script>
