<template>
  <div>
    <div id="mapContainer">
      <v-card>
        <l-map style="height: 800px" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-marker 
            :key="index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="latLng(dataMap.data.coordinates.pos[0], dataMap.data.coordinates.pos[1])"
            :opacity="dataMap.opac"
            >
            <l-icon :icon-size="dataMap.iconSize" :icon-url="icon"> </l-icon>
    
          </l-marker>
          <l-circle
          :lat-lng="circle.center"
      :radius="circle.radius"
      :color="circle.color"
          />
        </l-map>
      </v-card>
    </div>
    <div style="height: 800px" id="maptryit"></div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer, LMarker, LIcon, LCircle } from 'vue2-leaflet'
// import {heatLayer} from './heatmap/dist/leaflet-heat'
// import { Icon } from 'leaflet';

// delete Icon.Default.prototype._getIconUrl;
// Icon.Default.mergeOptions({
//   iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//   iconUrl: require('leaflet/dist/images/marker-icon.png'),
//   shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
// });
import oilgas from '../../assets/images/oil&gas.png'

export default {
  name: 'MapNavigation',
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LIcon,
    LCircle,
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
      iconSize: [30, 30],
      circle: {
        center: [-3.092642, 115.283758],
        radius: 5000,
        color: 'red'
      }
    }
  },
  methods: {
    latLng: function(lat,lng){
      return L.latLng(lat,lng)
    },
   
  },

  mounted: function() {
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

    
    // var heat = L.heatLayer([
    //   [-0.847199, 117.015818, 80], // lat, lng, intensity
    //   [-3.092642, 115.283758, 500],
    // ], {radius: 50}).addTo(maptryit);

  },
}
</script>

<style lang="scss" scoped>

.mapContainer {
  position: relative;
  left: 0px;
  top: 0px;
  z-index: 1;
}

.v-application .pa-6 {
    padding: 0px !important;
}

</style>
