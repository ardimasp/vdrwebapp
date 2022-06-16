<template>
  <div id="vtkviewer-container" class="vtkviewer-container">

    <vtp-card 
      :x="500"
      :y="0"
      title="VTP Viewer"
      :w="600"
      :h="600"
      :dataVtp="dataVtp"
      ref="vtpcard"
    >
    </vtp-card>
    <regular-card 
        :x="0"
        :y="200"
        title="Files"
        :w="400"
        :h="350"
      >
        <template>
          <tree-content-2
            @changeselected = selectedContent
            @removedata = removeContent
          ></tree-content-2>
        </template>
      </regular-card>

    <div>
      <v-btn
        depressed
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

      <v-btn
        depressed
        color="error"
        @click="onDelete"
      >
        Delete
      </v-btn>

      <v-container>
        <v-row>
          <v-col
            cols="12"
            sm="6"
            md="4"
          >
            <v-text-field
              dense
              label="Gain"
              v-model="gain"
              type="number"
              @keydown.enter.prevent="onPressEnter"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            sm="6"
            md="4"
          >
            <v-autocomplete
              v-model="value"
              :items="items"
              label="Standard"
            ></v-autocomplete>
          </v-col>
        </v-row>
      </v-container>
      
    </div>

    
  </div>
</template>

<script>
import VtpCard from './VtpCard.vue'
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import RegularCard from './RegularCard.vue'
import TreeContent2 from './TreeContent2.vue'
import fileService from '../../services/file.service';

export default{
  components: {
    VtpCard,
    RegularCard,
    TreeContent2,
  },
  data(){
      return {
          selectedFile: null,
          dataVtp: null,
          gain: 1,
          items: [],
          value: '2hot',

          dataVtpTest: null,
      }
  },
  props:{
  },
  watch: { 
    value: function(newVal) { // watch it
      this.$refs.vtpcard.changeColorMapName(newVal,this.gain)
    }
  },
  methods: {
    async selectedContent(selected) {
      console.log("at selected", selected[0])
      const file = await fileService.getFileRaw(selected[0])
      console.log(file.data);

      const fileReader = new FileReader();

        let that = this;
        fileReader.onload = function onLoad() {
          //read data 
          // console.log("at file reader", fileReader.result)
          const readerVtp = vtkXMLPolyDataReader.newInstance();
          readerVtp.parseAsArrayBuffer(fileReader.result);
          const data = readerVtp.getOutputData(0);
          // console.log("AAAAAAAAAAA", data)
          that.dataVtp = data
        };
        fileReader.readAsArrayBuffer(file.data);
    },
    removeContent(){
      this.onDelete()
    },

    onPressEnter(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(){
      this.$refs.vtpcard.removeActor()
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
          console.log("at file reader", fileReader.result)
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
    },
  setup(){

    return {
    };
  }
}
</script>

<style>
  .vtkviewer-container {
    width: 100%;
    min-height: 600px;
  }
</style>