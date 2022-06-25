<template>
  <div id="vtkviewer-container" class="vtkviewer-container">
    <div>
      <v-row>
        <v-col
          cols="12"
          sm="4"
          md="4"
        >
          <v-card id="widget-container" ref="widget">
            <v-container>
              <p class="font-weight-bold">Choose VTP file(s)</p>
              <div class="treeview-container">
                <tree-content-2
                  :selectable="load"
                  @changeselected = selectedContent
                  @removedata = removeContent
                >
                  <template>
                    <v-progress-linear
                      v-if="initialLoad"
                      color="secondary"
                      indeterminate
                    ></v-progress-linear>
                  </template>
                </tree-content-2>
              </div>
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
                v-model="gainValue[selectedIndex]"
                type="number"
              ></v-text-field>
              <v-autocomplete
                v-model="colourValue[selectedIndex]"
                :items="items"
                label="Colour Map"
              ></v-autocomplete>
              <v-btn color="primary" @click="applyChanges" :disabled="!checkApply">
                Apply
              </v-btn>
            </v-container>
          </v-card>
        </v-col>

        <v-col
          cols="12"
          sm="8"
          md="8"
          ref="viewer"
        >
          <vtp-card-2 
            v-if="height"
            :x="500"
            :y="13"
            title="VTP Viewer"
            :w="width"
            :h="height"
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
          </vtp-card-2>
        </v-col>
      </v-row>
    </div>

    
  </div>
</template>

<script>
import VtpCard2 from './VtpCard2.vue'
import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import TreeContent2 from './TreeContent2.vue'
import fileService from '../../services/file.service';
import { computed } from '@vue/composition-api';
import store from '../../store';

export default{
  components: {
    VtpCard2,
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
          gainValue: [],
          colourValue: [],
          load: false,

          height: null,
          width: null,
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
    returnSelectedTree() {return this.selectedTree},
    checkApply() {
      if(this.selectedTree == null || this.selectedTree.length <= 0) return false;
      if(this.gainValue[this.selectedIndex] < 1) return false

      return true;
    }
  },
  methods: {
    applyChanges(){
      // this.changeGain();
      this.$refs.vtpcard.changeColorMapName(this.colourValue[this.selectedIndex],this.gainValue[this.selectedIndex])

      // other things considered
    },
    async selectedContent(selected) {
      this.load = true;
      this.selectedTree = selected;
      this.gainValue.push(1);
      this.colourValue.push(this.value);
      if(this.selectedValue == null || this.selectedValue == "") {
        this.selectedValue = this.selectedTree[0]
        this.selectedIndex = 0
      }
      console.log(this.selectedTree)
      const file = await fileService.getFileRaw(selected.slice(-1)) //take the last one in the array

      const fileReader = new FileReader();

        let that = this;
        fileReader.onload = function onLoad() {
          //read data 
          const readerVtp = vtkXMLPolyDataReader.newInstance();
          readerVtp.parseAsArrayBuffer(fileReader.result);
          const data = readerVtp.getOutputData(0);
          console.log("AAAAAAAAAAA", data)
          that.dataVtp = data
          that.load = false
        };
        fileReader.readAsArrayBuffer(file.data);
    },
    removeContent(newArray, removedIndex){
      this.selectedTree = newArray;
      console.log(newArray)
      if(this.selectedTree.length > 0) {
        this.selectedValue = this.selectedTree[0]
        this.selectedIndex = 0
      }
      else {
        this.selectedValue = this.selectedIndex = null
      }
      this.gainValue.splice(removedIndex, 1)
      this.colourValue.splice(removedIndex, 1)
      this.onDelete(removedIndex)
    },

    changeGain(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(removedIndex){
      this.$refs.vtpcard.removeActor(removedIndex)
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
      this.height = this.$refs.widget.$el.clientHeight
      if(window.innerWidth > 1200) this.width = window.innerWidth - this.$refs.widget.$el.clientWidth - 260 - 100
      else if (window.innerWidth > 600) this.width = window.innerWidth - this.$refs.widget.$el.clientWidth - 100
      else this.width = window.innerHeight - 10
    },
  setup(){
    const initialLoad = computed(() => {return store.state.initialLoad})

    return {
      initialLoad
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

<style scoped>
.treeview-container {
  height: 150px;
  overflow-y: auto;
}
@media (min-height: 650px) {
  .treeview-container {
    height: 250px;
  }
}
@media (min-height: 800px) {
  .treeview-container {
    height: 300px;
  }
}
@media (min-height: 1000px){
  .treeview-container {
    height: 500px;
  }
}
@media (min-height: 1200px){
  .treeview-container {
    height: 650px;
  }
}
</style>