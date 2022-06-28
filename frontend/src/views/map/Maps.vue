<template>
  <div>
    <div class="container try">
       <!-- <vtk-card 
      :x="600"
      :y="0"
      title="3D View"
      :w="400"
      :h="500"
    >
    </vtk-card> -->

    <regular-card v-if="v==false"
      :x="10 - wss"
      :y="50"
      title="Select Wells"
      :w="300"
      :h="200"
    >
     <template>
       <map-filter :dataMaps="correctData" :value="value" :mapfilterPage="'visualization'" v-on:input="placeSelected"></map-filter>
     </template>
    </regular-card>


    </div>
    <MapVisualization :dataMaps="datas" :vtpMaps="vtpInfo" :heatmap="heatmap" :dataType="visualData" v-on:click="visualSelected"> </MapVisualization>
    <!-- :wellVtp="wellVtp" :lineVtp="lineVtp" :surfaceVtp="surfaceVtp" -->
    <!-- <MapNavigation :dataMaps="datas" :heatmap="heatmap" :dataType="visualData"></MapNavigation> -->
    <!-- <br>
    <br> -->
  </div>
</template>

<script>
// import MapNavigation from './MapNavigation.vue'
import 'leaflet/dist/leaflet.css'
// import L from 'leaflet'
import { cardData } from './Dummy.js'
import { colorRange } from './Color.js'
// import MapList from './MapList.vue'
// import MapSort from './MapSort.vue'

import MapFilter from './MapFilter.vue'

import RegularCard from '../viewer/RegularCard.vue'

// import axios from 'axios';
import {getDatafromDB, getDB, getVTPdata, getVTPinfo} from '../showcase/MapEndPoint.js'
import MapVisualization from './MapVisualization.vue'
// import oilgas from '../../assets/images/oil&gas.svg'
// import oilgas from '../../assets/images/map-marker.svg'
import store from '../../store'

export default {
  components: {
    // MapNavigation,
    // MapList,
    // MapSort,
    MapFilter,
    RegularCard,
    MapVisualization,
  },
    data: function() {
    return {
      dataMaps: cardData,
      colorSort: colorRange,
      value: [],
      selectedP: [],
      normalIcon: [50, 50],
      largeIcon: [100,100],
      datas: [],
      previousSelection: [],
      sortby: null,
      heatmap: [],
      opacity: 0.8,
      lessopacity: 0.4,
      deffillcolor: '#6200EE',
      defcolor: '#018786',

      filldefcolor: '#004E40',
      dataDB: [],
      token:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaXJiYWd1cyIsImV4cCI6MTY1MzU3MzIwNH0.it5-5UVWULRRNlGsF8kXbnacjXiHzrHKlG6Wz1Z1Zno',
      allData:[],
      tempD: [],
      transparent: 0,
      correctData:[],
      vtpInfo:[],
      tmpVTP: [],
      visualData: 'visual',
      v: false,
      wellVtp:[],
      lineVtp:[],
      surfaceVtp:[]
    }
  },
  

  methods: {

    placeSelected(point){
      this.selectedP = point
      for (var s in this.selectedP){

        this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename.includes(this.selectedP[s]))].iconfillColor = this.opacity
        // this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename.includes(this.selectedP[s]))].fillIcon = this.defcolor
        this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename.includes(this.selectedP[s]))].iconborderColor = 1

      }

      const myArrayFiltered = this.vtpInfo.filter( el => {
        return this.selectedP.every( f => {
          return !el.filename.includes(f);
        });
      });
      for (var ns in myArrayFiltered){
 
        this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename === myArrayFiltered[ns].filename)].iconfillColor = this.lessopacity
        // this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename === myArrayFiltered[ns].filename)].fillIcon = this.deffillcolor
        this.vtpInfo[this.vtpInfo.findIndex(dataC => dataC.filename === myArrayFiltered[ns].filename)].iconborderColor = this.transparent

        // this.datas[nsid].iconborderColor = this.transparent

      }
    },
     visualSelected(vis){
        this.v = vis
      },

    funcVol(arrayGas){
          let sortedarrayGas = arrayGas.sort(function(a,b) {
            return a[3]-b[3]
          });
          // HERE COLOR
          // this.colorSort = colorRange
          // OPACITY SORT
          var totalColor
          var intensity = 1/sortedarrayGas.length
          for(let i in sortedarrayGas){
            sortedarrayGas[i].push(intensity)
            intensity = intensity + 1/sortedarrayGas.length;
          }
          this.heatmap = sortedarrayGas

          var newtotalC = []
          if (this.colorSort.length >= sortedarrayGas.length){
            for(let i in sortedarrayGas){
              sortedarrayGas[i].push(this.colorSort[i])
            }
          }else if (this.colorSort.length < sortedarrayGas.length){
            if (Math.round(sortedarrayGas.length / this.colorSort.length) <= 1){
              totalColor = 2
            }else{
              totalColor = Math.round(sortedarrayGas.length / this.colorSort.length)
            }
            for(let i in this.colorSort){
              var tempAr = Array(totalColor).fill(this.colorSort[i])
              newtotalC = newtotalC.concat(tempAr)
            }
            for(let i in sortedarrayGas){
              sortedarrayGas[i].push(newtotalC[i])
            }
          }
          for (let s in sortedarrayGas){
            var sortSelect = this.datas.findIndex(dataC => dataC.wellName === sortedarrayGas[s][0]) 
            
            this.datas[sortSelect].iconborderColor = this.opacity
            this.datas[sortSelect].iconColor = sortedarrayGas[s][5]
          }

    },
    
  },
  async mounted(){
    this.correctData = await getVTPdata();
    var children
    for(let i =0; i <this.correctData.length; i++){
      children = this.correctData[i].children
      for (var j = 0; j < children.length; j++) {
      let infochildVTP = await getVTPinfo(children[j].id)
      if(infochildVTP != undefined){
        this.tmpVTP.push(infochildVTP)
      }else{
        continue
      }
    }
    }
    this.vtpInfo = this.tmpVTP.map(v => ({...v, iconSize: this.normalIcon, iconColor: this.defcolor,  iconfillColor: this.lessopacity, iconborderColor: this.transparent, fillIcon: this.deffillcolor}))


    this.tempD = await getDatafromDB();
    this.allData = await getDB(this.tempD)
    this.datas = this.allData.map(v => ({...v, iconSize: this.normalIcon, iconColor: this.defcolor,  iconfillColor: this.lessopacity, iconborderColor: this.transparent, fillIcon: this.deffillcolor}))
    
  },

  computed:{
    wss(){
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
    }

  }
}
</script>
<style lang="scss" scoped>

.container{
    z-index: 999;
    position: relative;
    margin-top: -40px;
    left: 50%;
    transform: translate(-50%, 0);
  }

</style>