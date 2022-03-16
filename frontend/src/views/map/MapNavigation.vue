<template>
  <div>
    <div id="mapContainer">
      <!-- <h6>{{dataMaps}}</h6> -->
      <!-- <v-card> -->
        <l-map class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-marker 
            :key="index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="latLng(dataMap.data.coordinates.pos[0], dataMap.data.coordinates.pos[1])"
            :opacity="dataMap.opac"
            @mouseover="markeronhover(dataMap.id)"
            @mouseleave="markeronleave(dataMap.id)"
            @click="cardshown(dataMap.id)"
            id="maptry" >
            >
            <l-icon class="iconcolor" :icon-size="dataMap.iconSize" :icon-url="dataMap.iconImg"> </l-icon>
    
          </l-marker>
          <l-circle
          :lat-lng="circle.center"
      :radius="circle.radius"
      :color="circle.color"
          />
        </l-map>
      <!-- </v-card> -->
    </div>
    <v-overlay style="z-index: 9999" :absolute="true" :value="overlay">
      <Card  :dataDetail="this.datacard" v-click-outside="onClickOutside"/>
    </v-overlay>
    <!-- <div style="height: 800px" id="maptryit"></div> -->
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer, LMarker, LIcon, LCircle } from 'vue2-leaflet'
import Card from './Card.vue'
// import {heatLayer} from './heatmap/dist/leaflet-heat'
// import { Icon } from 'leaflet';

// delete Icon.Default.prototype._getIconUrl;
// Icon.Default.mergeOptions({
//   iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//   iconUrl: require('leaflet/dist/images/marker-icon.png'),
//   shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });
import oilgas from '../../assets/images/oil&gas.svg'
import oilgasonhover from '../../assets/images/oil&gashover.png'
// import Vue from "vue";
import ClickOutside from 'vue-click-outside'

export default {
  name: 'MapNavigation',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LCircle,
    Card
  },
  props:{
    dataMaps: Array,
    heatmap: Array
  },

  data: function() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 6,
      center: [-3.092642, 115.283758],
      marker: [-3.092642, 115.283758],
      icon: oilgas,
      iconSize: [50, 50],
      circle: {
        center: [-3.092642, 115.283758],
        radius: 5000,
        color: 'red'
      },
      iconhover: oilgasonhover,
      datacard: {},
      overlay: false
    }
  },
  methods: {
    latLng: function(lat,lng){
      return L.latLng(lat,lng)
    },
    // heatt(){
    //   if(this.heatmap != 0){
    //       var heat = L.heatLayer(this.heatmap, {radius: 50}).addTo(maptryit);
    //   }
    //   return heat
    // },

    markeronhover(key){
      // console.log(key)
      var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      this.dataMaps[data].iconImg = this.iconhover
    },
    markeronleave(key){
    
      // console.log(key)
      var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      this.dataMaps[data].iconImg = this.icon
    },
    cardshown(key){
      var filteredResult = this.dataMaps.find((e) => e.id == key);
      this.datacard = filteredResult
      console.log(this.datacard.image)
      this.overlay = true
      // var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      // this.dataMaps[data].iconImg = this.icon
    },
    onClickOutside(val) {
      this.overlay = val
      console.log("clicked outside");
    },
  },

  mounted: function() {
    this.popupItem = this.$el

    // var maptryit = L.map('maptryit').setView([-3.092642, 115.283758], 5)
    var maptryit = L.map('maptryit').setView([-3.092642, 115.283758], 5)
    
    L.tileLayer(
      'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
      {
        maxZoom: 18,
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
          'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
      },
    ).addTo(maptryit)
    var greenIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });

    for(let i in this.dataMaps){
      L.marker([this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1]],{icon: greenIcon})
            .addTo(maptryit)
            .setOpacity(this.dataMaps[i].opac)
    }
      // L.marker([dataMap.data.coordinates.pos[0], dataMap.data.coordinates.pos[1]])
      // .addTo(maptryit)
      // .bindPopup('A pretty CSS3 popup.<br> Easily customizable.')
      // .openPopup()

    // if(this.heatmap != 0){
    //   var heat = L.heatLayer(
    //   this.heatmap
    // , {radius: 50}).addTo(maptryit);
        
    // heatt()
    // maptryit.removeLayer(heat)

    
    // var  

    // var testData = {
    //   max: 8,
    //   data: [{lat: -0.847199, lng:117.015818, count: 3},{lat: -3.092642, lng:115.283758, count: 1}]
    // };
    // var baseLayer = L.tileLayer(
    //   'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    //     attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    //     maxZoom: 18
    //   }
    // );
    
    // var cfg = {
    //   // radius should be small ONLY if scaleRadius is true (or small radius is intended)
    //   // if scaleRadius is false it will be the constant radius used in pixels
    //   "radius": 2,
    //   "maxOpacity": .8,
    //   // scales the radius based on map zoom
    //   "scaleRadius": true,
    //   // if set to false the heatmap uses the global maximum for colorization
    //   // if activated: uses the data maximum within the current map boundaries
    //   //   (there will always be a red spot with useLocalExtremas true)
    //   "useLocalExtrema": true,
    //   // which field name in your data represents the latitude - default "lat"
    //   latField: 'lat',
    //   // which field name in your data represents the longitude - default "lng"
    //   lngField: 'lng',
    //   // which field name in your data represents the data value - default "value"
    //   valueField: 'count'
    // };

    // var heatmapLayer = new HeatmapOverlay(cfg);
    // heatmapLayer.setData(testData);

    // var maptryit = L.map('maptryit', {
    //   center: [-3.092642, 115.283758],
    //   zoom: 5,
    //   layers: [baseLayer, heatmapLayer]
    // });

  },
   // do not forget this section
  directives: {
    ClickOutside
  }
}
</script>

<style lang="scss" scoped>
/* // .tab-index {
//   position: relative;
//   z-index: 1;
// }*/
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
</style>
