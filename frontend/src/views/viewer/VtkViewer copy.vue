<template>
  <div id="vtkviewer-container" class="vtkviewer-container">

    <vtp-card 
      :x="800"
      :y="0"
      title="VTP Viewer"
      :w="600"
      :h="600"
      :dataVtp="dataVtp"
      ref="vtpcard"
    >
    </vtp-card>

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
              @keydown.enter.prevent="onPressEnter"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            class="d-flex"
            cols="12"
            sm="6"
          >
            <v-select
              v-model="value"
              :items="items"
              label="Standard"
            ></v-select>
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

export default{
  components: {
    VtpCard,
  },
  data(){
      return {
          selectedFile: null,
          dataVtp: null,
          gain: 1,
          items: [],
          value: '2hot',
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