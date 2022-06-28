<template>
  <div>
     <div class="container">
      <regular-card  v-if="chosenValue.length != 0"
       :x="0 - coorX"
      :y="50"
      title="Select VTP"
      :w="850"
      :h="120"
      >
        <template>
          <div class="pa-2 text-no-wrap mt-4 ">

            <v-row
              no-gutters
            >
            <v-col cols="3">
                <v-autocomplete 
                    dense
                    v-model="selectedValue"
                    :items="this.chosenValue"
                    label="Selected"
                  ></v-autocomplete>
            </v-col>
            <v-col cols="3" class="ml-4">
                 
                  <v-slider class="pl-0 mt-1"
                  label="Gain"
                    :disabled="selectedValue == null"
                    dense
                    :max="max"
                    :min="min"
                    :step="sliderStep"
                    v-model="gainValue[selectedIndex]"
                    thumb-label="always"
                    @change="applyChanges"
                  >
                  <template v-slot:append>
                    <v-text-field
                      v-model="max"
                      hide-details
                      single-line
                      type="number"
                      style="width: 60px; margin-top: -20px"
                      label="Max Gain"
                      placeholder="Max Gain"
                    ></v-text-field>
                  </template>
                  </v-slider>
            </v-col>
            <v-col cols="4" class="ml-4">
                  <v-autocomplete
                    :disabled="selectedValue == null"
                    dense
                    v-model="colourValue[selectedIndex]"
                    :items="items"
                    label="Colour Map"
                    @change="applyChanges"

                  ></v-autocomplete>
            </v-col>
            <v-col class="ml-4">
               <v-btn
                  color="primary"
                  small
                  @click="addVTP"
                >
                  Add VTP
                </v-btn>
            </v-col>
            </v-row>
          </div>

        </template>
      </regular-card>
      
      <vtp-card-2
      v-if="chosenValue.length != 0"
        :x="0 - coorX"
        :y="200"
        title="VTP Viewer"
        :w="850"
        :h="this.height"
        :dataVtp="dataVtp"
        :vtpIndex="selectedIndex"
        ref="vtpcard">
        <template>
          <v-progress-linear
            v-if="load"
            indeterminate
            color="secondary"
          ></v-progress-linear>
        </template>
      </vtp-card-2>
      <!-- </vtp-card> -->
    </div>
    <div id="mapContainer">
      <!-- <p>hel {{this.surfaceV[0].geodata}} {{this.seismicV.length}} {{this.wellV.length}}</p> -->
        <l-map ref="myMap" class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
           
           <div :key="index" v-for="(wel,index) in wss">
              <l-circle
                v-if="wel.type=='well-vtp'"
                :lat-lng="wel.center"
                :radius="wel.radius*1000"
                :color='wel.iconColor'
                :fillColor='wel.fillIcon'
                :fillOpacity="wel.iconfillColor"
                :opacity="wel.iconborderColor"
                @click="chosenClick(wel.filename)"
              >
              </l-circle>
              <l-polygon
                v-if="wel.type=='surface-vtp'"
              :color='wel.fillIcon'
              :lat-lngs="wel.geodata"
              :opacity="wel.iconfillColor"
              @click="chosenClick(wel.filename)"
              ></l-polygon>
              <l-polyline
                v-if="wel.type=='line-vtp'"
              :lat-lngs="wel.geodata" 
              :color='wel.fillIcon'
              :opacity="wel.iconfillColor"

              @click="chosenClick(wel.filename)"
              ></l-polyline>
           </div>
        </l-map>
      <!-- </v-card> -->
    </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer,LCircle,LPolyline,LPolygon } from 'vue2-leaflet'

import ClickOutside from 'vue-click-outside'
import {getVTPdata} from '../showcase/MapEndPoint.js';
import fileService from '../../services/file.service';
import VtpCard2 from '../viewer/VtpCard.vue';

import RegularCard from '../viewer/RegularCard.vue'


import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import store from '../../store'

// import VtpCard from '../viewer/VtpCard.vue';


export default {
  name: 'MapVisualization',
  components: {
    LMap,
    LTileLayer,
    // ChoiceCard,
    // ChoiceVisual,
    LCircle,
    LPolygon,
    // LCircleMarker,
    // LTooltip,
    LPolyline,
    // VtpCard,
    VtpCard2,
    RegularCard
  },
  props:{
    dataMaps: Array,
    vtpMaps: Array,
    heatmap: Array,
    dataType: String,

      // wellVtp: Array,
      // lineVtp: Array,
      // surfaceVtp: Array
  },

  data: function() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 6,
      center: [-3.092642, 115.283758],
      marker: [-3.092642, 115.283758],
      iconSize: [50, 50],
     
      iconhover: '#00000',
      datacard: {},
      dataFilter: {},
      overlay: false,
      overlaymap: false,

      curColor: ['#6200EE', 'red', '#018786'],
      options: { permanent: true, direction:'top' },

      figVisualize:[],
      dataVtp: null,
      chosenValue: [],
      click:0,
      gain: 1,
      items: [],
      value: '2hot',
      max:100,
      min:1,
      sliderStep:0.01,
      selectedValue: null, //value selected based on the array
      selectedIndex: null, //the index of the selected value
      load: false,
      gainValue: [],
      colourValue: [],
      height: null,
      width: null,
      lessopacity: 0.4,
      transparent: 0

      // windowContaine
    }
  },
  watch: { 
    // value: function(newVal) { // watch it
    //   this.$refs.vtpcard.changeColorMapName(newVal,this.gain)
    // }
    selectedValue: function(newVal) {
      if(this.chosenValue == null || this.chosenValue.length == 0) return

      this.selectedIndex = this.chosenValue.indexOf(newVal)
    },
  },
  methods: {
    latLng: function(lat,lng){
      return L.latLng(lat,lng)
    },

    cardshown(keyName){
      var filteredResult = this.dataMaps.find((e) => e.wellName == keyName);
      this.datacard = filteredResult
      this.overlay = true
    },

    async chosenClick(chosenWell){
      this.load = true;

      if(this.vtpMaps.find((e) => e.filename == chosenWell).fillIcon == this.curColor[0] || this.vtpMaps.find((e) => e.filename == chosenWell).fillIcon == this.curColor[2]){
        this.shapeClick(chosenWell)
      }else if(this.vtpMaps.find((e) => e.filename == chosenWell).fillIcon==this.curColor[1]){
        this.removeContent(chosenWell)
      }
    },
    async shapeClick(chosenWell){
      this.click += 1
      var well = chosenWell.replace('%20', ' ')

      this.gainValue.push(1);
      this.colourValue.push(this.value);
      if(this.selectedValue == null || this.selectedValue == "") {
        this.selectedValue = this.chosenValue[0]
        this.selectedIndex = 0
      }
      const file = await fileService.getFileRaw(well)

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
        this.chosenValue.push(well)
  
      this.vtpMaps[this.vtpMaps.findIndex(dataC => dataC.filename === chosenWell)].fillIcon = this.curColor[1]
       
        var visual = true
        this.$emit('click', visual)
    },

     removeContent(chosenWell){
      var replaceW = chosenWell.replace('%20', ' ')
      for(let i=0; i<this.chosenValue.length;i++){
        if (this.chosenValue[i] == replaceW){
          var unclickedIndex = i
        }
       
      }
      this.gainValue.splice(unclickedIndex, 1)
      this.colourValue.splice(unclickedIndex, 1)
      this.onDelete(unclickedIndex)
      if (unclickedIndex > -1) {
        this.chosenValue.splice(unclickedIndex, 1); // 2nd parameter means remove one item only
      }
      if(this.chosenValue.length > 0) {
        this.selectedValue = this.chosenValue[0]
        this.selectedIndex = 0
      }
      else {
        this.selectedValue = this.selectedIndex = null

        var visual = false
        this.$emit('click', visual)
      }
     
      this.vtpMaps[this.vtpMaps.findIndex(dataC => dataC.filename === chosenWell)].fillIcon = this.curColor[0]
      this.vtpMaps[this.vtpMaps.findIndex(dataC => dataC.filename === chosenWell)].iconfillColor = this.lessopacity
      this.vtpMaps[this.vtpMaps.findIndex(dataC => dataC.filename === chosenWell)].iconborderColor = this.transparent
      this.load = false;

    },

    applyChanges(){
      this.$refs.vtpcard.changeColorMapName(this.colourValue[this.selectedIndex],this.gainValue[this.selectedIndex])

    },

    onPressEnter(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(unclickedIndex){
      this.$refs.vtpcard.removeActor(unclickedIndex)
    },
    
    onClickOutside(val) {
      this.overlay = val
    },

    changeOverlay(over){
      this.overlay = over
    },
   
    recenterMap(key) {
      var filteredResult = this.dataMaps.find((e) => e.id == key);

      this.$refs.myMap.mapObject.flyTo([filteredResult.wellLatitude, filteredResult.wellLongitude], 9)
    },
    markeronhover(key){
      var filteredResult = this.dataMaps.find((e) => e.id == key);
      this.dataFilter = filteredResult
      this.overlaymap = true
    },

    addVTP(){
      this.$router.push('/vtp-form')
    }

  },
  async mounted() {
    this.items = vtkColorMaps.rgbPresetNames

    this.figVisualize = await getVTPdata();

    this.height = (this.$refs.myMap.$el.clientHeight) / 1.4
    

  },
   computed:{
    // wellRule(){
    //   if(Object.keys(this.childrens).length > 0){
    //     var usedWells = this.childrens.map(a => a.wellName);

    //   const wellRule = 
    //    v => (usedWells.includes(v) === false) || 'Well name exist!'
    //     this.wellRules.push(wellRule)
    //   }
    // },

    wss(){
      return this.vtpMaps
    },

    coorX(){
      if(store.state.test.isDrawerOpen == true){
        return 0
      }else{
        return 300

      }
    },

    wleft(){
      if(store.state.test.isDrawerOpen == true){
        return 22+'px'
      }else{
        return -280+'px'

      }
    },
  },
   // do not forget this section
  directives: {
    ClickOutside
  }
}
</script>

<style lang="css" scoped>

.leaflet-marker-icon {
  fill: green;
  filter: hue-rotate(120deg);
    
} 
.mapContainer {
  position: fixed;
  left: 0px;
  top: 0px;
  z-index: 1;
}

.map-size{
  min-width: 87vw; 
  min-height: 88vh;
  height: auto;
  max-width: 100vw;
  max-height: 100vh;
}

.v-application .pa-6 {
    padding: 0px !important;
}

@media (max-height:855px){
.map-size{
  min-width: 86vw; 
  min-height: 83vh;
  height: auto;
  max-width: 100vw;
  max-height: 90vh;
}
}

.new_color{
  fill: green;
}

.svg-icon path {
  fill: crimson;
}

#maptryit { height: 800px; }

.container{
    z-index: 999;
    position: relative;
    margin-top: -40px;
    left: 50%;
    transform: translate(-50%, 0);
  }
</style>
