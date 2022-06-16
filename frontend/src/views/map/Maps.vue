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

    <regular-card 
      :x="10"
      :y="50"
      title="Select Wells"
      :w="300"
      :h="200"
    >
     <template>
       <map-filter :dataMaps="correctData" :value="value" v-on:input="placeSelected"></map-filter>
     </template>
    </regular-card>

     <regular-card 
      :x="400"
      :y="50"
      title="Sort By"
      :w="250"
      :h="150"
    >
     <template>
          <MapSort v-on:input="sortSelected" />
     </template>
    </regular-card>

    </div>

    <MapNavigation :dataMaps="datas" :heatmap="heatmap"></MapNavigation>
    <!-- <br>
    <br> -->
  </div>
</template>

<script>
import MapNavigation from './MapNavigation.vue'
import 'leaflet/dist/leaflet.css'
// import L from 'leaflet'
import { cardData } from './Dummy.js'
import { colorRange } from './Color.js'
// import MapList from './MapList.vue'
import MapSort from './MapSort.vue'

import MapFilter from './MapFilter.vue'

import RegularCard from '../viewer/RegularCard.vue'

// import axios from 'axios';
import {getDatafromDB, getDB, restructureData} from '../showcase/MapEndPoint.js'
// import oilgas from '../../assets/images/oil&gas.svg'
// import oilgas from '../../assets/images/map-marker.svg'

export default {
  components: {
    MapNavigation,
    // MapList,
    MapSort,
    MapFilter,
    RegularCard,
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
      correctData:[]
    }
  },
  

  methods: {

    placeSelected(point){
      this.selectedP = point
      // console.log(this.selectedP)
      for (var s in this.selectedP){
        // console.log(this.datas[this.datas.findIndex(dataC => dataC.wellName === this.selectedP[s])].fillIcon)

        // this.datas[this.datas.findIndex(dataC => dataC.title === this.selectedP[s])].iconSize = this.largeIcon
        // console.log(this.datas)
        this.datas[this.datas.findIndex(dataC => dataC.wellName === this.selectedP[s])].iconfillColor = this.opacity
        this.datas[this.datas.findIndex(dataC => dataC.wellName === this.selectedP[s])].fillIcon = this.defcolor
        // this.datas[this.datas.findIndex(dataC => dataC.title === this.selectedP[s])].iconborderColor = this.opacity


      }

      const myArrayFiltered = this.datas.filter( el => {
        return this.selectedP.every( f => {
          return f !== el.wellName;
        });
      });
      console.log(myArrayFiltered)
      for (var ns in myArrayFiltered){
        
        this.datas[this.datas.findIndex(dataC => dataC.wellName === myArrayFiltered[ns].wellName)].iconfillColor = this.lessopacity
        this.datas[this.datas.findIndex(dataC => dataC.wellName === myArrayFiltered[ns].wellName)].fillIcon = this.deffillcolor
        // this.datas[nsid].iconborderColor = this.transparent

      }
    },

    funcVol(arrayGas){
          let sortedarrayGas = arrayGas.sort(function(a,b) {
            return a[3]-b[3]
          });
          // HERE COLOR
          // this.colorSort = colorRange
          // console.log(sortedarrayGas)
          // OPACITY SORT
          var totalColor
          var intensity = 1/sortedarrayGas.length
          for(let i in sortedarrayGas){
            sortedarrayGas[i].push(intensity)
            intensity = intensity + 1/sortedarrayGas.length;
          }
          this.heatmap = sortedarrayGas

          console.log(this.colorSort)
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
            // console.log(sortedarrayGas.length)
            // console.log(this.colorSort.length)
            // console.log(totalColor)
            for(let i in this.colorSort){
              var tempAr = Array(totalColor).fill(this.colorSort[i])
              newtotalC = newtotalC.concat(tempAr)
            }
            for(let i in sortedarrayGas){
              sortedarrayGas[i].push(newtotalC[i])
            }
          }
          console.log(sortedarrayGas)
          for (let s in sortedarrayGas){
            var sortSelect = this.datas.findIndex(dataC => dataC.wellName === sortedarrayGas[s][0]) 
            console.log(sortSelect)
            console.log(sortedarrayGas[s][5])

            this.datas[sortSelect].iconborderColor = this.opacity
            this.datas[sortSelect].iconColor = sortedarrayGas[s][5]
          }
          console.log(this.datas)

    },
    
    sortSelected(sortp){
      let arrayGas = []
      alert(sortp);
      if(sortp == "Gas Volume"){
        for (let i in this.datas){
          arrayGas.push([this.datas[i].wellName, this.datas[i].wellLatitude, this.datas[i].wellLongitude, this.datas[i].wellGasVolume])
          // alert(arrayGas)
        }
        this.funcVol(arrayGas)
      
      }
      else if(sortp == "Oil Volume"){
        for (let i in this.datas){
          arrayGas.push([this.datas[i].wellName, this.datas[i].wellLatitude, this.datas[i].wellLongitude, this.datas[i].wellOilVolume])
          // alert(arrayGas)
        }
        this.funcVol(arrayGas)
      }
      else if(sortp == null){
        for (let i in this.datas){
          this.datas[i].iconColor = this.deffillcolor
           this.datas[i].iconborderColor = this.transparent

        }
      }
     
    }
  },
  async mounted(){
    this.tempD = await getDatafromDB();
    // console.log(this.tempD)
    // console.log(this.token)
    this.allData = await getDB(this.tempD)
    // console.log(this.allData)
    this.correctData = await restructureData(this.allData)
    // console.log(this.correctData)

    this.datas = this.allData.map(v => ({...v, iconSize: this.normalIcon, iconColor: this.defcolor,  iconfillColor: this.lessopacity, iconborderColor: this.transparent, fillIcon: this.deffillcolor}))
    // console.log(this.datas)
  
  

    // this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, opac: this.lessopacity, iconImg: this.defaulticon}))
    // console.log(datas)
  },
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

// .try{
//   width: 100%;
//   height: 1000px;
// }  

/* // .fixedcontainer {
//   position: absolute;
//   left: 0px;
//   top: 0px;
// } */
</style>