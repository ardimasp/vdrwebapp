<template>
  <div>
    <div id="mapContainer">
        <l-map ref="myMap" class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-rectangle :key="'r'+index"
            v-for="(dataMap,index) in dataMaps" 
            :color='rectangleColor'
            :bounds="[[dataMap.wellLatitude+0.028236, dataMap.wellLongitude+(-0.077651)], 
            [dataMap.wellLatitude-0.009319, dataMap.wellLongitude+0.075669]]"
            @click="chosenClick(dataMap.wellName, visual[0])"
            ></l-rectangle>

            <l-polyline :key="'p1'+index"
            v-for="(dataMap,index) in dataMaps" 
            :lat-lngs="[[(dataMap.wellLatitude+0.028236-0.1), (dataMap.wellLongitude+(-0.077651))], 
            [(dataMap.wellLatitude-0.009319+0.015), (dataMap.wellLongitude+0.075669+(-0.06))]]" 
            :color='polylineColor'
            @click="shapeClick(dataMap.wellName, visual[2])"
            ></l-polyline>

            <l-polyline :key="'p2'+index"
            v-for="(dataMap,index) in dataMaps" 
            :color='polylineColor'
            :lat-lngs="[[(dataMap.wellLatitude+0.028236-0.1), (dataMap.wellLongitude+(-0.077651)+0.16)], 
            [(dataMap.wellLatitude-0.009319+0.015), (dataMap.wellLongitude+0.075669+(-0.09))]]" 
            @click="shapeClick(dataMap.wellName, visual[3])"

            ></l-polyline>

          <l-circle
            :key="'c'+index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="[dataMap.wellLatitude+0.05, dataMap.wellLongitude]"
            :radius="Math.sqrt((dataMap.wellArea * 1000000)/Math.PI)/2"
            :color='dataMap.iconColor'
            :fillColor='dataMap.fillIcon'
            :fillOpacity="dataMap.iconfillColor"
            :opacity="dataMap.iconborderColor"
            @click="shapeClick(dataMap.wellName, visual[1])"
          >
          
          </l-circle>
        </l-map>
      <!-- </v-card> -->
       <vtp-card v-if="dataVtp != null" style="z-index: 9999;"
      :x="500"
      :y="0"
      title="VTP Viewer"
      :w="600"
      :h="600"
      :dataVtp="dataVtp"
      ref="vtpcard"
    >
    </vtp-card>
    </div>
   
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer,LCircle, LRectangle,LPolyline } from 'vue2-leaflet'
// import ChoiceCard from './ChoiceCard.vue'
// import ChoiceVisual from './ChoiceVisual.vue'

// import oilgas from '../../assets/images/oil&gas.svg'

// import Vue from "vue";
import ClickOutside from 'vue-click-outside'
import {getImages} from '../showcase/MapEndPoint.js';
import fileService from '../../services/file.service';


import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
// import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';

import VtpCard from '../viewer/VtpCard.vue';


export default {
  name: 'MapVisualization',
  components: {
    LMap,
    LTileLayer,
    // ChoiceCard,
    // ChoiceVisual,
    LCircle,
    LRectangle,
    // LCircleMarker,
    // LTooltip,
    LPolyline,
    VtpCard
  },
  props:{
    dataMaps: Array,
    heatmap: Array,
    dataType: String
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

      prevColor: [],
      options: { permanent: true, direction:'top' },

      figVisualize:[],
      rectangleColor: 'red',
      polylineColor: 'blue',

      dataVtp: null,
      visual:["surface", "well", "seismic_C06", "seismic_C08"],
      click:0
    }
  },
  methods: {
    latLng: function(lat,lng){
      return L.latLng(lat,lng)
    },

    cardshown(keyName){
      var filteredResult = this.dataMaps.find((e) => e.wellName == keyName);
      this.datacard = filteredResult
      // console.log(this.datacard.image)
      this.overlay = true
      // var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      // this.dataMaps[data].iconImg = this.icon
    },

    async chosenClick(chosenWell, visualizeType){
      if(this.rectangleColor=="red"){
        this.shapeClick(chosenWell, visualizeType)
      }else if(this.rectangleColor=="green"){
        this.removeContent()
      }
    },
    async shapeClick(chosenWell, visualizeType){
      this.click += 1
      if(this.click > 2){
        this.rectangleColor = "green";
      }

      var cW = this.figVisualize.find((e) => e.name == chosenWell)
      console.log(cW)
      var t= cW.children.find((e) => e.name.includes(visualizeType))
      console.log('/'+t.name)

      const file = await fileService.getFileRaw('/'+t.name)
      console.log(file.data);

      const fileReader = new FileReader();

        let that = this;
        fileReader.onload = function onLoad() {
          //read data 
          // console.log("at file reader", fileReader.result)
          const readerVtp = vtkXMLPolyDataReader.newInstance();
          readerVtp.parseAsArrayBuffer(fileReader.result);
          const data = readerVtp.getOutputData(0);
          console.log("AAAAAAAAAAA", data)
          that.dataVtp = data
        };
        fileReader.readAsArrayBuffer(file.data);
        // console.log(this.dataVtp)

    },

     removeContent(){
      this.onDelete()
      this.rectangleColor = "red";
    },

    onPressEnter(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(){
      this.$refs.vtpcard.removeActor()
    },
    
    onClickOutside(val) {
      this.overlay = val
      console.log("clicked outside");
    },

    changeOverlay(over){
      this.overlay = over
      console.log(over);
    },
   
    recenterMap(key) {
      var filteredResult = this.dataMaps.find((e) => e.id == key);

      this.$refs.myMap.mapObject.flyTo([filteredResult.wellLatitude, filteredResult.wellLongitude], 9)
  },
    markeronhover(key){
      var filteredResult = this.dataMaps.find((e) => e.id == key);
      console.log(filteredResult)
      this.dataFilter = filteredResult
      this.overlaymap = true
    },

  },
  async mounted() {
    this.figVisualize = await getImages("visualization");
    console.log(this.figVisualize)
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

      /* :radius="Math.sqrt((dataMap.wellArea * 1000000)/Math.PI)" */
            /* :radius="pixelValue(dataMap.wellLatitude, dataMap.wellArea, zoom)*200" */

</style>
