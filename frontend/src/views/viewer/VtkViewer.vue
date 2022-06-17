<template>
  <div id="vtkviewer-container" class="vtkviewer-container">
    <vtp-card 
      :x="500"
      :y="13"
      title="VTP Viewer"
      :w="600"
      :h="600"
      :dataVtp="dataVtp"
      :vtpIndex="selectedIndex"
      ref="vtpcard"
    >
      <template>
        <v-progress-linear
          v-if="load"
          indeterminate
          color="secondary"
        ></v-progress-linear>
      </template>
    </vtp-card>

    <div>
      <v-row>
        <v-col
          cols="12"
          sm="6"
          md="4"
        >
          <v-card>
            <v-container>
              <p class="font-weight-bold">Choose VTP file(s)</p>
              <tree-content-2
                :selectable="load"
                @changeselected = selectedContent
                @removedata = removeContent
              ></tree-content-2>
            </v-container>
            <v-divider></v-divider>
            <v-card-text class="font-weight-bold">Configurations:</v-card-text>
            <v-container class="pl-5 pr-5 pb-5">
              <v-autocomplete
                v-model="selectedValue"
                :items="returnSelectedTree"
                label="Select VTP"
              ></v-autocomplete>
              <v-text-field
                label="Gain"
                v-model="gain"
                type="number"
              ></v-text-field>
              <v-autocomplete
                v-model="value"
                :items="items"
                label="Standard"
              ></v-autocomplete>
              <v-btn color="primary" @click="applyChanges">
                Apply
              </v-btn>
            </v-container>
          </v-card>
        </v-col>
      </v-row>
    </div>

    
  </div>
</template>

<script>
import VtpCard from './VtpCard.vue'
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import TreeContent2 from './TreeContent2.vue'
import fileService from '../../services/file.service';

export default{
  components: {
    VtpCard,
    TreeContent2,
  },
  data(){
      return {
          selectedFile: null,
          dataVtp: null,
          gain: 1,
          items: [],
          value: '2hot',

          selectedTree: null, //selected array in treeview
          selectedValue: null, //value selected based on the array
          selectedIndex: null, //the index of the selected value
          load: false,
      }
  },
  props:{
  },
  watch: { 
    // value: function(newVal) { // watch it
    //   this.$refs.vtpcard.changeColorMapName(newVal,this.gain)
    // }
    selectedValue: function(newVal) {
      if(this.selectedTree == null || this.selectedTree.length == 0) return

      this.selectedIndex = this.selectedTree.indexOf(newVal)
    }
  },
  computed:{
    returnSelectedTree() {return this.selectedTree}
  },
  methods: {
    applyChanges(){
      this.changeGain();
      this.$refs.vtpcard.changeColorMapName(this.value,this.gain)

      // other things considered
    },
    async selectedContent(selected) {
      console.log("at selected", selected)
      this.load = true;
      this.selectedTree = selected;
      if(this.selectedValue == null || this.selectedValue == "") {
        this.selectedValue = this.selectedTree[0]
        this.selectedIndex = 0
      }
      const file = await fileService.getFileRaw(selected.slice(-1)) //take the last one in the array
      // console.log(file.data);

      const fileReader = new FileReader();

        let that = this;
        fileReader.onload = function onLoad() {
          //read data 
          const readerVtp = vtkXMLPolyDataReader.newInstance();
          readerVtp.parseAsArrayBuffer(fileReader.result);
          const data = readerVtp.getOutputData(0);
          that.dataVtp = data
          that.load = false
        };
        fileReader.readAsArrayBuffer(file.data);
    },
    removeContent(newArray, removedIndex){
      this.selectedTree = newArray;
      if(this.selectedTree.length > 0) {
        this.selectedValue = this.selectedTree[0]
        this.selectedIndex = 0
      }
      else {
        this.selectedValue = this.selectedIndex = null
      }
      // console.log("at removed", removedIndex)
      this.onDelete(removedIndex)
    },

    changeGain(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(removedIndex){
      this.$refs.vtpcard.removeActor(removedIndex)
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