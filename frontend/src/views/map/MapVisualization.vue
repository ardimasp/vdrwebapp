<template>
  <div>
     <div class="container">
      <regular-card  v-if="chosenValue.length != 0"
       :x="0"
      :y="50"
      title="Select VTP"
      :w="800"
      :h="100"
      >
        <template>
          <div class="pa-4 text-no-wrap ">

            <v-row
              no-gutters
            >
            <v-col>
                <v-autocomplete 
                    dense
                    v-model="selectedValue"
                    :items="this.chosenValue"
                    label="Selected"
                  ></v-autocomplete>
            </v-col>
            <v-col class="ml-4">
                  <!-- <v-text-field
                      label="Gain"
                      v-model="gain"
                      type="number"
                    ></v-text-field> -->
                  <!-- <v-subheader class="pl-0 pt-0">
                    Gain
                  </v-subheader> -->
                  <v-slider class="pl-0 mt-1"
                  label="Gain"
                    :disabled="selectedValue == null"
                    dense
                    :max="max"
                    :min="min"
                    v-model="gainValue[selectedIndex]"
                    :thumb-size="24"
                    thumb-label="always"
                    @change="applyChanges"
                  ></v-slider>
            </v-col>
            <v-col class="ml-4">
                  <v-autocomplete
                    :disabled="selectedValue == null"
                    dense
                    v-model="colourValue[selectedIndex]"
                    :items="items"
                    label="Colour Map"
                    @change="applyChanges"

                  ></v-autocomplete>
            </v-col>
            </v-row>
          </div>

        </template>
      </regular-card>
      
      <vtp-card-2
      v-if="chosenValue.length != 0"
        :x="0"
        :y="200"
        title="VTP Viewer"
        :w="800"
        :h="800"
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
      <p>hel {{wellV[0]}} </p>
        <l-map ref="myMap" class="map-size" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>

          <l-rectangle :key="'r'+index"
            v-for="(surface,index) in surfaceV" 
            :color='rectangleColor'
            :bounds="surface.geodata"
            @click="chosenClick(surface.geodata, surface.type)"
            ></l-rectangle>

            <l-polyline :key="'p1'+index"
            v-for="(seismic,index) in seismicV" 
            :lat-lngs="seismic.geodata" 
            :color='polylineColor'
            @click="chosenClick(seismic.filename, seismic.type)"
            ></l-polyline>

            <!-- <l-polyline :key="'p2'+index"
            v-for="(dataMap,index) in dataMaps" 
            :color='polylineColor2'
            :lat-lngs="[[(dataMap.wellLatitude+0.028236-0.1), (dataMap.wellLongitude+(-0.077651)+0.16)], 
            [(dataMap.wellLatitude-0.009319+0.015), (dataMap.wellLongitude+0.075669+(-0.09))]]" 
            @click="chosenClick(dataMap.wellName, visual[3])"

            ></l-polyline> -->

          <l-circle
            :key="'c'+index"
            v-for="(wel,index) in wellV"
            :lat-lng="wel.center"
            :radius="wel.radius*10000"
            :color='wel.iconColor'
            :fillColor='circleColor'
            :fillOpacity="wel.iconfillColor"
            :opacity="wel.iconborderColor"
            @click="chosenClick(wel.filename, wel.type)"
          >
          </l-circle>
            <!-- <l-circle           
            :lat-lng="wellV[0].center"
            :radius="wellV[0].radius * 10000"
            :color='wellV[0].iconColor'
            :fillColor='circleColor'
            :fillOpacity="wellV[0].iconfillColor"
            :opacity="wellV[0].iconborderColor"
          >
          </l-circle> -->
        </l-map>
      <!-- </v-card> -->
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
import {getVTPdata} from '../showcase/MapEndPoint.js';
import fileService from '../../services/file.service';
import VtpCard2 from '../viewer/VtpCard.vue';

import RegularCard from '../viewer/RegularCard.vue'


import vtkXMLPolyDataReader from '@kitware/vtk.js/IO/XML/XMLPolyDataReader'
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';

// import VtpCard from '../viewer/VtpCard.vue';


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

      prevColor: [],
      options: { permanent: true, direction:'top' },

      figVisualize:[],
      rectangleColor: 'blue',
      polylineColor: 'blue',
      polylineColor2: 'blue',

      circleColor: 'blue',
      unchosenColor: 'blue',
      dataVtp: null,
      chosenValue: [],
      visual:["surface-vtp", "well-vtp", "line-vtp"],
      click:0,
      gain: 1,
      items: [],
      value: '2hot',
      max:100,
      min:1,
      selectedValue: null, //value selected based on the array
      selectedIndex: null, //the index of the selected value
      load: false,
      gainValue: [],
      colourValue: [],
      height: null,
      width: null,

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
      // console.log(this.datacard.image)
      this.overlay = true
      // var data = this.dataMaps.findIndex(dataC => dataC.id === key) 
      // this.dataMaps[data].iconImg = this.icon
    },

    async chosenClick(chosenWell, visualizeType){
      this.load = true;

      if(visualizeType == this.visual[0]){
        if(this.rectangleColor=="blue"){
          this.shapeClick(chosenWell, visualizeType)
        }else if(this.rectangleColor=="red"){
          this.removeContent(chosenWell, visualizeType)
        }
      }else if(visualizeType == this.visual[1]){
        if(this.circleColor == "blue"){
          this.shapeClick(chosenWell, visualizeType)
        }else if(this.circleColor== "red"){
          this.removeContent(chosenWell, visualizeType)

        }
      }else if(visualizeType == this.visual[2]){
        if(this.polylineColor == "blue"){
          this.shapeClick(chosenWell, visualizeType)
        }else if(this.polylineColor== "red"){
          this.removeContent(chosenWell, visualizeType)
        }
      }else if (visualizeType == this.visual[3]){
        if(this.polylineColor2 == "blue"){
          this.shapeClick(chosenWell, visualizeType)
        }else if(this.polylineColor2== "red"){
          this.removeContent(chosenWell, visualizeType)
        }}
       
        // if((this.rectangleColor||this.circleColor||this.polylineColor||this.polylineColor2)=="blue"){
        //   this.shapeClick(chosenWell, visualizeType)
        // }else if((this.rectangleColor||this.circleColor||this.polylineColor||this.polylineColor2)=="blue"){
        //   this.removeContent(visualizeType)
        // }
    },
    async shapeClick(chosenWell, visualizeType){
      this.click += 1
      console.log('test', this.figVisualize)
            console.log('chosenWell', chosenWell)
      // const arrChosenwell = chosenWell.split('/')
      // console.log(arrChosenwell)
      var well = chosenWell.replace('%20', ' ')
      console.log('choosen', well)

      // var cW = this.figVisualize.find((e) => e.name == well)
      // console.log(cW.children)
      // var t= cW.children.find((e) => e.name == arrChosenwell[2])
      // var t= cW.children.find((e) => e.name.includes(visualizeType))
      // console.log(t)

      // console.log(t)
      this.gainValue.push(1);
      this.colourValue.push(this.value);
      if(this.selectedValue == null || this.selectedValue == "") {
        this.selectedValue = this.chosenValue[0]
        this.selectedIndex = 0
      }
      const file = await fileService.getFileRaw(well)

      // const file = await fileService.getFileRaw('/'+chosenWell+'/'+t.name)
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
          that.load = false

        };
        fileReader.readAsArrayBuffer(file.data);
        // console.log(this.dataVtp)
        this.chosenValue.push(well)

        // this.chosenValue.push('/'+t.name)
      console.log('arr:', this.chosenValue)

  // if(this.click > 1){
        if(visualizeType == this.visual[0]){
        this.rectangleColor = "red";

        }else if(visualizeType == this.visual[1]){
          this.circleColor= "red";
        }
        else if(visualizeType == this.visual[2]){
          this.polylineColor= "red";
        }else if( visualizeType == this.visual[3]){
          this.polylineColor2= "red";
        }
        // this.unchosenColor = "blue"
        var visual = true
        this.$emit('click', visual)
      // }
    },

     removeContent(chosenWell, visualizeType){
      var replaceW = chosenWell.replace('%20', ' ')
      for(let i=0; i<this.chosenValue.length;i++){
        if (this.chosenValue[i] == replaceW){
          var unclickedIndex = i
        }
        // if (this.chosenValue[i].includes(visualizeType)){
        //   var unclickedIndex = i
        // }
      }
      console.log(unclickedIndex)
      this.gainValue.splice(unclickedIndex, 1)
      this.colourValue.splice(unclickedIndex, 1)
      this.onDelete(unclickedIndex)
      if (unclickedIndex > -1) {
        this.chosenValue.splice(unclickedIndex, 1); // 2nd parameter means remove one item only
      }
      console.log('arr after delete:', this.chosenValue)
      if(this.chosenValue.length > 0) {
        this.selectedValue = this.chosenValue[0]
        this.selectedIndex = 0
      }
      else {
        this.selectedValue = this.selectedIndex = null

        var visual = false
        this.$emit('click', visual)
      }
      // this.unchosenColor = "blue"
      if(visualizeType == this.visual[0]){
        this.rectangleColor = "blue";

        }else if(visualizeType == this.visual[1]){
          this.circleColor= "blue";
        }else if(visualizeType == this.visual[2]){
          this.polylineColor= "blue";
        }else if( visualizeType == this.visual[3]){
          this.polylineColor2= "blue";
        }
        this.load = false;

    },

    applyChanges(){
      // this.changeGain();
            console.log("penting:",this.value, this.gain, this.selectedIndex, this.colourValue[this.selectedIndex],this.gainValue[this.selectedIndex])
      this.$refs.vtpcard.changeColorMapName(this.colourValue[this.selectedIndex],this.gainValue[this.selectedIndex])
      // this.$refs.vtpcard.changeColorMapName(this.value,this.gain)

      // other things considered
    },

    onPressEnter(){
      this.$refs.vtpcard.setGain(this.gain)
    },
    onDelete(unclickedIndex){
      this.$refs.vtpcard.removeActor(unclickedIndex)
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
    this.items = vtkColorMaps.rgbPresetNames
    // console.log(this.dataMaps)

    // this.figVisualize = await getImages("visualization");
    this.figVisualize = await getVTPdata();

    console.log(this.figVisualize)
        // console.log(document.getElementsByClassName('container').clientWidths)
    // this.height = this.$refs.myMap.$el.clientWidth
    // console.log(this.height)
    // console.log(window.innerWidth)
    // if(window.innerWidth > 1200) this.width = window.innerWidth - this.$refs.myMap.$el.clientWidth - 260 - 100
    //   else if (window.innerWidth > 600) this.width = window.innerWidth - this.$refs.myMap.$el.clientWidth - 100
    //   else this.width = window.innerHeight - 10
    // console.log('vtp', this.vtpMaps)
    // this.wellVtp = this.vtpMaps.find(e => e.type === 'well-vtp');
    // console.log('well', this.wellVtp)

 
    // console.log(this.lineVtp)
    // console.log(this.surfaceVtp)

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
    wellV(){
      var wellAvai = []
      if(Object.keys(this.vtpMaps).length > 0){
        var w = this.vtpMaps.find(e => e.type === 'well-vtp');
        console.log(w)
        wellAvai.push(w)
      }
      return wellAvai

    },

    surfaceV(){
      var surfaceAvai = []
      if(Object.keys(this.vtpMaps).length > 0){
        var w = this.vtpMaps.find(e => e.type === 'surface-vtp');
        console.log(w)
        surfaceAvai.push(w)
      }
      return surfaceAvai
    },

    seismicV(){
      var seismicAvai = []
      if(Object.keys(this.vtpMaps).length > 0){
        var w = this.vtpMaps.find(e => e.type === 'line-vtp');
        console.log(w)
        seismicAvai.push(w)
      }
      return seismicAvai
    }
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

.container{
    z-index: 999;
    position: relative;
    margin-top: -40px;
    left: 50%;
    transform: translate(-50%, 0);
  }
</style>
