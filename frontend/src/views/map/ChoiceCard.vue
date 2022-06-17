<template>
  <!-- <v-hover v-slot="{ hover }"> -->
      <div>
    <v-card
      style="background-color: #f4f5fa;"

      :loading="loading"
      class="mx-auto my-12"
      max-width="500"
      max-height="500"
      width="400"
      height="400"
    >
      <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>

      <v-row 
      style="background-color: #9155fd;"
      no-gutters>
        <v-col  cols="auto"
                class="mr-auto">
            <v-card-title class="pa-2 ml-2 mt-2">{{ this.datacard.wellName }}</v-card-title>
        </v-col>
        
            <v-col  cols="auto">
                <!-- <v-btn class="pa-2 mr-6 mt-2" icon @click="closeOverlay()">
                    <v-icon>{{icons.mdiCloseThick}}</v-icon>

                </v-btn> -->
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">

                    <v-btn class="pa-2 mr-6 mt-1" icon @click="closeOverlay()">
                        <v-icon  v-bind="attrs"
                      v-on="on">{{icons.mdiCloseThick}}</v-icon>

                    </v-btn>
                  </template>
                  <span>Close Overlay</span>
                </v-tooltip>
              </v-col> 
      </v-row>
 <!-- <v-row no-gutters>
    <p class="font-weight-bold mr-2 mt-0 mb-0">
      Bold text.
    </p>
 </v-row> -->

      <v-row>
        <v-col>
          <!-- <v-checkbox border-color="#000000" color="primary" class="black--text shrink ml-5 mr-0 mt-0" v-for="item in images" v-model="val" :key="item" :label="item" :value="item" ></v-checkbox> -->
          <v-list-item-group
            v-model="val"
            multiple
          >
            <v-virtual-scroll
              :items="this.takeImages"
              :item-height="50"
              height="260"
            >
              <template v-slot="{ item }">
                <v-list-item :key="item.name" :value="item.name">
                  <v-list-item-action>
                    <v-checkbox
                      :input-value="val.includes(item.name)"

                      color="primary"
                    />
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title class="black--text">
                      {{ item.name }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </template>
            </v-virtual-scroll>
          </v-list-item-group>
        </v-col>     
      </v-row>
      <v-card-actions class="justify-center">
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
      <CardContent :dataD="this.chosenImgPath" :dataTitle="this.datacard.wellName" :details="this.info" v-on:click="changeOverlay"/>
    </v-overlay>
    </div>
  <!-- </v-hover> -->
  <!-- style="background-color: #E0F2F1; color: #9155fd;" -->
</template>

<script>
import {mdiDownload, mdiCloseThick} from "@mdi/js"
import {getImages} from '../showcase/MapEndPoint.js';

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
      takeImages: [],
      imgShowcase: undefined,
      info: undefined,
      images: this.dataDetail.images,
    //   imgsort: null,
      icons:{
        mdiDownload,
        mdiCloseThick
      },
      overlayAgain: false,
      chosenImg: [],
      chosenImgPath: [],
      chosenData: []
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
        this.chosenImgPath = []
        // let imgD = this.takeImages.filter(tImg => this.chosenImg.includes(tImg.name))
        // console.log(imgD)
        for(let i in this.chosenImg){
          this.chosenImgPath.push('/'+this.datacard.wellName+'/'+this.chosenImg[i])
        }
        console.log(this.chosenImgPath)
        // console.log(this.chosenImg)
        this.overlayAgain = true
    },

    changeOverlay(closeover){
      this.overlayAgain = closeover
      console.log(closeover);
    }
  },
  async mounted() {
    this.images = this.datacard.images

    var copy = Object.assign({}, this.datacard)
    delete copy.fieldName;
    delete copy.wellName;
    delete copy.iconSize;
    delete copy.iconColor;
    delete copy.iconfillColor;
    delete copy.iconborderColor;
    delete copy.fillIcon;
    delete copy.id;

    this.info = copy
    var pointer = "showcase"
    this.imgShowcase = await getImages(pointer);
    // console.log(this.imgShowcase)
    let result = this.imgShowcase.filter(obj => {
      return obj.name === this.datacard.wellName
    })
    // console.log(result[0].children)
    for (let i in result[0].children){
      this.takeImages.push(result[0].children[i])
    }
    console.log(this.takeImages)


    // for (let i in result){
    //   for(let j=0; j <result[i].children.length; j++){

    //   }
    //   console.log(result.children[])
    //   this.takeImages.push(result.children[i].name)
    // }

  },
  computed: {
    disabled() {
        return this.val < 1; // or === 0   
    }
}
}
</script>
<style scoped>
.black--text /deep/ label {
    color: #777777;
}
</style>
