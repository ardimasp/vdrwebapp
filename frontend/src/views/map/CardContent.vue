<template>
     <v-card
     style="background-color:rgb(145, 85, 253);"
      class="mx-auto my-12"
      max-width="900"
      max-height="this.heightWindow"
      width="900"
      height="this.heightWindow"
      ref="cardContent"
    >
     <template slot="progress">
        <v-progress-linear color="#BB86FC" height="10" indeterminate></v-progress-linear>
      </template>
      <v-row class="mt-2">
        <!-- <v-col class="ml-5 mt-5"> -->
                <v-card-title style="color: white!important;" class="ml-4 mb-3">{{ this.dataTitle }}</v-card-title>
        <!-- </v-col> -->
                  <!-- <v-spacer></v-spacer> -->
          <v-spacer></v-spacer>

        <!-- <v-col md="auto" class="mt-7"> -->
          <!-- <v-btn icon>
              <v-icon>{{icons.mdiDownload}}</v-icon>

          </v-btn> -->
          <div class="mr-10 mt-2">
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">

                  <v-btn icon @click="wH()"  class="mr-4" style="color: white!important;">
                      <v-icon  v-bind="attrs"
                    v-on="on">{{icons.mdiDownload}}</v-icon>

                  </v-btn>
                </template>
                <span>Download Data</span>
              </v-tooltip>

            <!-- </v-col> -->
            <!-- <v-col lg="2" class="mt-7"> -->
              <v-tooltip top>
                <template v-slot:activator="{ on, attrs }">

                  <v-btn icon @click="closeOverlay()" style="color: white!important;">
                      <v-icon  v-bind="attrs"
                    v-on="on">{{icons.mdiCloseThick}}</v-icon>

                  </v-btn>
                </template>
                <span>Close</span>
              </v-tooltip>
          </div>
          <!-- <v-btn icon @click="closeOverlay()">
              <v-icon>{{icons.mdiCloseThick}}</v-icon>

          </v-btn> -->
        <!-- </v-col> -->
      </v-row>
        <!-- <VtkContent
            :divWidthProp="800"
            :divHeightProp="500"
        /> -->
        <div ref="content">
      <v-carousel height="400">
        <v-carousel-item min-width="500" max-height="400"
          v-for="(item, i) in this.images"
          :key="i"
          :src="item"
          reverse-transition="fade-transition"
          transition="fade-transition"
          @contextmenu.prevent="handler(item)"
        ></v-carousel-item>
      </v-carousel>
      <v-simple-table class="pl-4" style="background-color: #EDE7F6;" height="300px">
        <template v-slot:default>
        <tbody>
          
            <tr
                v-for="(item,i) in dataKeys"
                :key="i"
            >

                <td style="color:black!important">{{ item }}</td>
                <td style="color:black!important"> {{ dataValues[i] }} </td>
            </tr>
        </tbody>
        </template>
    </v-simple-table>
        </div>
    </v-card>
<!-- style="color: #2D1F54;" -->
</template>

<script>

// import VtkCard from '../viewer/VtkCard.vue'
// import VtkContent from '../viewer/VtkContent.vue'
import {displayImages} from '../showcase/MapEndPoint.js';
import {mdiDownload, mdiCloseThick} from "@mdi/js"
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable';


// import html2canvas from "html2canvas"


export default {
  components:{
    // VtkContent,

  },
  name: "CardContent",
  props: {
    dataD: Array,
    dataTitle: String,
    details: Object,
    windowHeight: Number
  },
  data: function(){
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
      dataValues: [],
      size: [],
      stateS: [],
      widthHeight :[],
      heightWindow: 0
    }
  },

  watch: {
    stateS(nstateS) {
      // alert(nstateS)
      if(nstateS.length == this.images.length){
        this.widthHeight.push(nstateS)

        this.downloadData(this.widthHeight)
      }
    }
  },
  methods: {

     closeOverlay:function(){
      var over = false
      this.images.length = 0
      this.$emit('click', over)
    },

    wH(){
      
      for(let x in this.images){
        let that = this

        const img = new Image()
        img.src = this.images[x]
        img.onload = function(r) {
          that.stateS.push([r.path[0].width, r.path[0].height])  
        }  
      }
    },

    downloadData(widHei){
      var doc = new jsPDF();
      doc.text(10, 10, this.dataTitle);
      // let space = 20
      // for(let i=0; i < this.dataKeys.length;i++){
      //   doc.text(15, space, this.dataKeys[i])
      //   doc.text(15, space, this.dataValues[i])
      //   space = space + 10
      // }
      autoTable(doc,{
        theme: 'grid',
        header: this.dataTitle,
        head: [this.dataKeys],
        body: [
          this.dataValues
        ],
        margin: {horizontal: 7},
        styles: {overflow: 'linebreak', cellWidth: 'auto'},
        columnStyles: {5:{cellWidth: 20}, 6: {cellWidth: 20}, 7: {cellWidth: 30}, 8: {cellWidth: 30}}
      })
      doc.addPage()

      let init = [0, 0, 90, 90]
      let initialX = init[0]
      let initialY = init[1]
      for(let x in this.images){
        var hratio =  widHei[widHei.length - 1][x][1]/widHei[widHei.length - 1][x][0]
        if(widHei[widHei.length - 1][x][0] > doc.internal.pageSize.getWidth() && widHei[widHei.length - 1][x][1] > doc.internal.pageSize.getHeight() ){
          doc.addImage(this.images[x], 'JPEG', initialX, initialY, doc.internal.pageSize.getWidth(), doc.internal.pageSize.getWidth()*hratio);
        }
        else if(widHei[widHei.length - 1][x][0] > doc.internal.pageSize.getWidth() && widHei[widHei.length - 1][x][1] < doc.internal.pageSize.getHeight()){
          // doc.addImage(this.images[x], 'JPEG', initialX, initialY, doc.internal.pageSize.getWidth(),widHei[widHei.length - 1][x][1]);
          doc.addImage(this.images[x], 'JPEG', initialX, initialY, doc.internal.pageSize.getWidth(), doc.internal.pageSize.getWidth()*hratio);

        }
        else if(widHei[widHei.length - 1][x][0] < doc.internal.pageSize.getWidth() && widHei[widHei.length - 1][x][1] > doc.internal.pageSize.getHeight()){
          doc.addImage(this.images[x], 'JPEG', initialX, initialY, widHei[widHei.length - 1][x][0],doc.internal.pageSize.getHeight());
        }
        else if(widHei[widHei.length - 1][x][0] < doc.internal.pageSize.getWidth() && widHei[widHei.length - 1][x][1] < doc.internal.pageSize.getHeight()){
          doc.addImage(this.images[x], 'JPEG', initialX, initialY, widHei[widHei.length - 1][x][0], widHei[widHei.length - 1][x][1]);
        }

        if(this.images.length > (x)){
          doc.addPage()
        }
        else {
          continue        
        }
      }
      doc.save(`${this.dataTitle}.pdf`);

    },
    handler(imgSrc){
      window.open(imgSrc);

    }
    
  },
  async mounted() {
    for (let i in this.datacard){

      var valI = await displayImages(this.datacard[i])
      this.images.push(valI)
    }
    this.showcaseDetails = this.sD
    this.dataKeys = Object.keys(this.showcaseDetails)
    this.dataValues = Object.values(this.showcaseDetails)
    this.heightWindow  = this.windowHeight / 1.4
  }
}

// https://stackoverflow.com/questions/62245699/html2canvas-and-jspdf-add-1-image-per-page
// https://stackoverflow.com/questions/36472094/how-to-set-image-to-fit-width-of-the-page-using-jspdf
// https://stackoverflow.com/questions/60953089/how-to-fit-an-image-in-the-center-of-a-page-using-jspdf
// https://github.com/simonbengtsson/jsPDF-AutoTable/issues/273
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
