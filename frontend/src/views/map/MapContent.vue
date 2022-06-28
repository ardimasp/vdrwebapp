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
      <v-row>
          <div class="mt-8 ml-2">
                <v-card-title>{{ this.dataTitle }}</v-card-title>
          </div>
          <v-spacer></v-spacer>

          <div class="mt-10 mr-10">
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">

               <v-btn icon @click="wH()"  class="mr-4">
                  <v-icon  v-bind="attrs"
                v-on="on">{{icons.mdiDownload}}</v-icon>

              </v-btn>
            </template>
            <span>Download Data</span>
          </v-tooltip>

          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">

               <v-btn icon @click="closeOverlay()">
                  <v-icon  v-bind="attrs"
                v-on="on">{{icons.mdiCloseThick}}</v-icon>

              </v-btn>
            </template>
            <span>Close</span>
          </v-tooltip>
          </div>
      </v-row>
      <v-row v-if="this.visualType === 'Well log'">
        <v-col><div class="px-4 text-no-wrap" >

            <v-select
                  v-model="value"
                  :items="items"
                  label="Standard"
                ></v-select>
                </div>
            </v-col>
            <v-col>
            <v-btn class="ml-2 mt-2"
            
            color="primary"
            @click="onUploadFile"
          >
            Upload VTP
          </v-btn>
          <input
            id="seismic"
            multiple="true"
            style="display:none"
            type="file"
            accept=".vtp" 
            ref="uploader" 
            @change="onFileChanged"
            >
            <v-btn class="ml-2 mt-2"
            
            color="error"
            @click="onDelete"
          >
            Delete
          </v-btn>
        </v-col>
        
      </v-row>
          <smooth-scrollbar id="scroll-area">
            <div id="example-content">
                <VtkContent v-if="this.visualType === 'Viewer'"
                    :divWidthProp="900"
                    :divHeightProp="600"
                />

                <chart-content v-if="this.visualType === 'Viewer'" :id="this.idTesting">
                </chart-content>
            </div>
          </smooth-scrollbar>
       

        <vtp-content v-if="this.visualType === 'Well log'"
        :divWidthProp="900"
            :divHeightProp="700"
            :dataVtp="dataVtp"
            ref="vtpcontent"
            ></vtp-content>
   
    </v-card>
<!-- style="color: #2D1F54;" -->
</template>

<script>

// import VtkCard from '../viewer/VtkCard.vue'
import VtkContent from '../viewer/VtkContent.vue'
// import VtkCard from '../viewer/VtkCard.vue'

import {mdiDownload, mdiCloseThick} from "@mdi/js"
// import VtkViewer from '../viewer/VtkViewer.vue';

import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import VtpContent from '../viewer/VtpContent.vue';
// import html2canvas from "html2canvas"
import ChartContent from '../viewer/ChartContent.vue';
import SmoothScrollbar from 'vue-smooth-scrollbar'

export default {
  components:{
    VtkContent,
    VtpContent,
    ChartContent,
    SmoothScrollbar
// VtkCard,
    // VtkViewer
  },
  name: "CardContent",
  props: {
    dataD: Array,
    dataTitle: String,
    visualType: String,
    allData: Object

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

      selectedFile: null,
      dataVtp: null,
      gain: 1,
      items: [],
      value: '2hot',

      idTesting: 1,
    }
  },
  watch: { 
    value: function(newVal) { // watch it
      this.$refs.vtpcontent.changeColorMapName(newVal,this.gain)
    },
  },
  methods: {

    closeOverlay:function(){
      var over = false
      this.images.length = 0
      this.$emit('click', over)
    },

      changeColorMapName(colormapname,gain){
       this.$refs.vtpcontent.changeColorMapName(colormapname,gain)
    },
    setGain(gain) {
      this.$refs.vtpcontent.setGain(gain)
    },
    removeActor() {
      this.$refs.vtpcontent.removeActor()
    },
    
    onPressEnter(){
      this.$refs.vtpcontent.setGain(this.gain)
    },
    onDelete(){
      this.$refs.vtpcontent.removeActor()
    },
    onUploadFile(){
      this.$refs.uploader.click();
    },
    onFileChanged(e) {
        this.selectedFile = e.target.files[0];

        const fileReader = new FileReader();

        let that = this;
        fileReader.onload = function onLoad() {
          //read data 
          const readerVtp = vtkXMLPolyDataReader.newInstance();
          readerVtp.parseAsArrayBuffer(fileReader.result);
          const data = readerVtp.getOutputData(0);
          that.dataVtp = data
        };
        fileReader.readAsArrayBuffer(this.selectedFile);
    },
  },
  mounted() {

      this.items = vtkColorMaps.rgbPresetNames
      this.height = this.$refs.myMap.$el.clientWidth
    },
  setup(){

    return {
    };
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

#scroll-area {
  width: 900px;
  height: 700px;
}

#example-content {
  width: 900px;
  height: 1000px;
}
</style>
