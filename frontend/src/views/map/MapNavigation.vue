<template>
  <div>
    <div id="mapContainer">
      <!-- <h6>{{dataMaps}}</h6> -->
      <!-- <v-card> -->
        <l-map ref="myMap" class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <!-- <l-marker 
            :key="index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="latLng(dataMap.data.coordinates.pos[0], dataMap.data.coordinates.pos[1])"
            :opacity="dataMap.opac"
            @click="cardshown(dataMap.id)"
            id="maptry"
            :icon ="getIcon(dataMap)"
           >
                <l-tooltip>{{dataMap.title}}</l-tooltip>
          </l-marker> -->
          <l-circle
            :key="index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="[dataMap.wellLatitude, dataMap.wellLongitude]"
            :radius="dataMap.wellArea * 1000"
            :color='dataMap.iconColor'
            :fillColor='dataMap.fillIcon'
            :fillOpacity="dataMap.iconfillColor"
            :opacity="dataMap.iconborderColor"
            @click="cardshown(dataMap.wellName)"
            @mouseover="recenterMap(dataMap.id)"
          />
        </l-map>
      <!-- </v-card> -->
    </div>
    <v-overlay style="z-index: 9999;" :absolute="true" :value="overlay">
      <ChoiceCard  :dataDetail="this.datacard" v-click-outside="onClickOutside" v-on:click="changeOverlay"/>
    </v-overlay>
  <!-- <v-card style="height: 400px; width:500px; z-index: 9999;"> -->
    <v-overlay :absolute="true" :value="overlaymap">
      <MaponFilter  :dataFilter="this.dataFilter"/>
    </v-overlay>
  <!-- </v-card> -->
    <!-- <div style="height: 800px" id="maptryit"></div> -->
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer, LCircle } from 'vue2-leaflet'
import ChoiceCard from './ChoiceCard.vue'
// import MaponFilter from './MaponFilter.vue'
// LMarker, LTooltip
// import oilgas from '../../assets/images/oil&gas.svg'
// import oilgasonhover from '../../assets/images/oil&gashover.png'
// import oilgas from '../../assets/images/map-marker.svg'
// import oilgasonhover from '../../assets/images/map-marker-onhover.svg'


// import Vue from "vue";
import ClickOutside from 'vue-click-outside'

export default {
  name: 'MapNavigation',
  components: {
    LMap,
    LTileLayer,
    // LMarker,
    // LIcon,
    // Card,
    ChoiceCard,
    // MaponFilter,
    LCircle
    // LTooltip
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
      iconSize: [50, 50],
     
      iconhover: '#00000',
      datacard: {},
      dataFilter: {},
      overlay: false,
      overlaymap: false,

      prevColor: []
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

    // markeronhover(key){
    //   var data = this.dataMaps.find(dataC => dataC.id === key) 
    //   this.prevColor.push(data.iconColor)
    //   console.log(this.prevColor)
    //   data.iconColor = this.iconhover
    //   this.getIcon(data)

    //   // var data = this.dataMaps.find(dataC => dataC.id === key) 
    //   // data.iconSize = [150, 150]
    //   // this.getIcon(data)

    // },
    // markeronleave(key){
    
    //   console.log(this.prevColor)
    //   var data = this.dataMaps.find(dataC => dataC.id === key) 
    //   data.iconColor = this.prevColor[0]
    //   this.getIcon(data)
    //   this.prevColor = []

    //   // var data = this.dataMaps.find(dataC => dataC.id === key) 
    //   // data.iconSize = [50, 50]
    //   // this.getIcon(data)
    // },

    cardshown(keyName){
      var filteredResult = this.dataMaps.find((e) => e.wellName == keyName);
      this.datacard = filteredResult
      // console.log(this.datacard.image)
      this.overlay = true
      // var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      // this.dataMaps[data].iconImg = this.icon
    },
    onClickOutside(val) {
      this.overlay = val
      console.log("clicked outside");
    },

    changeOverlay(over){
      this.overlay = over
      console.log(over);
    },
    getIcon(item) {
      // console.log(item.iconColor)
      return L.divIcon({
        className: "my-custom-pin",
        html: `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="${item.iconSize[0]}" height="${item.iconSize[1]}" viewBox="0 0 24 24">
        <path class="new_color" fill="${item.iconColor}" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" />
      </svg>`,
      tooltipAnchor: [ -10, 20 ]
      });
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

  mounted() {

    // this.popupItem = this.$el

    // var maptryit = L.map('maptryit').setView([-3.092642, 115.283758], 5)

    // IF NEED VUE
    // var maptryit = L.map('maptryit').setView([-3.092642, 115.283758], 5)
    
    // L.tileLayer(
    //   'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw',
    //   {
    //     maxZoom: 18,
    //     attribution:
    //       'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
    //       'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    //     id: 'mapbox/streets-v11',
    //     tileSize: 512,
    //     zoomOffset: -1,
    //   },
    // ).addTo(maptryit)

    // var greenIcon = new L.Icon({
    //   iconUrl: require('../../assets/images/map-marker.svg'),
    //   shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    //   iconSize: [25, 41],
    //   iconAnchor: [12, 41],
    //   popupAnchor: [1, -34],
    //   shadowSize: [41, 41]
    // });

    // for(let i in this.dataMaps){
    //   console.log(this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1])
    //   L.marker([this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1]],{icon: greenIcon})
    //         .addTo(maptryit)
    //         .setOpacity(this.dataMaps[i].opac)
    //         // .on('click', this.cardshown(this.dataMaps[i].id))
    //         .on('mouseover', this.markeronhover(this.dataMaps[i].id))
    //         // .on('mouseleave', this.markeronleave(this.dataMaps[i].id))

    // }

    // this.svgIcon = L.divIcon({
    //     html: `
    //        {{ <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="24" height="24" viewBox="0 0 24 24">
    //     <path class="new_color" fill="currentColor" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" />
    //   </svg>}}`,
    //     className: "svg-icon",
    //     iconSize: [24, 40],
    //     iconAnchor: [12, 40],
    //   })

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

<style lang="css" scoped>
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

.new_color{
  fill: green;
}

.svg-icon path {
  fill: crimson;
}

#maptryit { height: 800px; }

      /* :radius="Math.sqrt((dataMap.wellArea * 1000000)/Math.PI)" */

</style>
