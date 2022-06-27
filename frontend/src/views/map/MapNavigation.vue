<template>
  <div>
    <div id="mapContainer">
        <l-map ref="myMap" class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
         
          <l-circle
            :key="index"
            v-for="(dataMap,index) in dataMaps"
            :lat-lng="[dataMap.wellLatitude, dataMap.wellLongitude]"
            :radius="Math.sqrt((dataMap.wellArea * 1000000)/Math.PI)*5"
            :color='dataMap.iconColor'
            :fillColor='dataMap.fillIcon'
            :fillOpacity="dataMap.iconfillColor"
            :opacity="dataMap.iconborderColor"
            @click="cardshown(dataMap.wellName)"
            @mouseover="recenterMap(dataMap.id)"
          >
          <l-tooltip
            :options="options"
            :content="iconTooltip()"/>
          </l-circle>
        </l-map>
      <!-- </v-card> -->
    </div>
    <v-overlay v-if="this.dataType === 'showcase'" style="z-index: 9999;" :absolute="true" :value="overlay">
      <ChoiceCard  :dataDetail="this.datacard" v-click-outside="onClickOutside" :windowHeight="this.height" v-on:click="changeOverlay"/>
    </v-overlay>
    <v-overlay v-if="this.dataType === 'visual'" style="z-index: 9999;" :absolute="true" :value="overlay">
      <ChoiceVisual  :dataDetail="this.datacard" v-click-outside="onClickOutside" v-on:click="changeOverlay"/>
    </v-overlay>
    <!-- <v-overlay :absolute="true" :value="overlaymap">
      <MaponFilter  :dataFilter="this.dataFilter"/>
    </v-overlay> -->
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import { LMap, LTileLayer,LCircle,LTooltip } from 'vue2-leaflet'
import ChoiceCard from './ChoiceCard.vue'
import ChoiceVisual from './ChoiceVisual.vue'

// import oilgas from '../../assets/images/oil&gas.svg'

// import Vue from "vue";
import ClickOutside from 'vue-click-outside'

export default {
  name: 'MapNavigation',
  components: {
    LMap,
    LTileLayer,
    ChoiceCard,
    ChoiceVisual,
    LCircle,
    // LCircleMarker,
    LTooltip
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

    }
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
    onClickOutside(val) {
      this.overlay = val
    },

    changeOverlay(over){
      this.overlay = over
    },
    getIcon(item) {
      return L.divIcon({
        className: "my-custom-pin",
        html: `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"  width="${item.iconSize[0]}" height="${item.iconSize[1]}" viewBox="0 0 24 24">
        <path class="new_color" fill="${item.iconColor}" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z" />
      </svg>`,
      tooltipAnchor: [ -10, 20 ]
      });
    },
    iconTooltip(){
      return "<div><img src='https://static.thenounproject.com/png/2946698-200.png' width='30' /></div>"
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

    metersPerPixel(latitude, zoomLevel) {
      var earthCircumference = 40075017;
      var latitudeRadians = latitude * (Math.PI/180);
      return earthCircumference * Math.cos(latitudeRadians) / Math.pow(2, zoomLevel + 8);
    },

    pixelValue(latitude, meters, zoomLevel) {
      return meters / this.metersPerPixel(latitude, zoomLevel);
    }
  },

  mounted() {
     this.height = this.$refs.myMap.$el.clientHeight
    
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
