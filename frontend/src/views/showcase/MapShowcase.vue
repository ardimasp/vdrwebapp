<template>
  <div>
    <div class="container">
       <!-- <vtk-card 
      :x="600"
      :y="0"
      title="3D View"
      :w="400"
      :h="500"
    >
    </vtk-card> -->

    <regular-card 
      :x="400"
      :y="50"
      title="Select Wells"
      :w="300"
      :h="200"
    >
     <template>
       <map-filter :dataMaps="correctData" :value="value" :mapfilterPage="'showcase'" v-on:input="placeSelected"></map-filter>
     </template>
    </regular-card>

     <regular-card 
      :x="10"
      :y="50"
      title="Sort By"
      :w="300"
      :h="140"
    >
     <template>
          <MapSort v-on:input="sortSelected" />
     </template>
    </regular-card>
<!-- <regular-card  -->
  <draggable-button style="z-index: 999; left: 22px; top: 215px;" :isClick.sync="btnIsClick">
            <v-btn
              elevation="2"
              x-large
              color="primary"
              @click="addData"
              width="300px"
            >
              Add Wells
              <v-icon style="z-index: 999;" class="ml-4" right dark>
                {{ mdiMapMarkerPlus }}
              </v-icon>
            </v-btn>   

    </draggable-button>
            <!-- </regular-card> -->

    </div>

    <MapNavigation ref="myMap" :dataMaps="datas" :heatmap="heatmap" :dataType="dT"></MapNavigation>
    <!-- <br>
    <br> -->
  </div>
</template>

<script>
import MapNavigation from '../map/MapNavigation.vue'
import 'leaflet/dist/leaflet.css'
// import L from 'leaflet'
// import { cardData } from './Dummy.js'
import { colorRange } from '../map/Color.js'
// import MapList from './MapList.vue'
import MapSort from '../map/MapSort.vue'

import MapFilter from '../map/MapFilter.vue'

import RegularCard from '../viewer/RegularCard.vue'
import draggableButton from 'vue-draggable-button';
import { mdiMapMarkerPlus } from '@mdi/js';
// import axios from 'axios';
import {getDatafromDB, getDB, restructureData} from './MapEndPoint.js'
// import oilgas from '../../assets/images/oil&gas.svg'
// import oilgas from '../../assets/images/map-marker.svg'

export default {
  components: {
    MapNavigation,
    // MapList,
    MapSort,
    MapFilter,
    RegularCard,
    draggableButton,
  },
    data: function() {
    return {
      // dataMaps: cardData,
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
      defcolor: '#00796B',

      filldefcolor: '#004E40',
      dataDB: [],
      // token:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaXJiYWd1cyIsImV4cCI6MTY1MzU3MzIwNH0.it5-5UVWULRRNlGsF8kXbnacjXiHzrHKlG6Wz1Z1Zno',
      allData:[],
      tempD: [],
      transparent: 0,
      correctData:[],
      btnIsClick: false,
      dT: 'showcase',
      width: undefined,
      xResponsive: undefined
    }
  },
  setup() {
    return {
        mdiMapMarkerPlus
    }
  },

  methods: {

    placeSelected(point){
      this.selectedP = point
      for (var s in this.selectedP){

        // this.datas[this.datas.findIndex(dataC => dataC.title === this.selectedP[s])].iconSize = this.largeIcon
        this.datas[this.datas.findIndex(dataC => dataC.wellName === this.selectedP[s])].iconfillColor = this.opacity
        this.datas[this.datas.findIndex(dataC => dataC.wellName === this.selectedP[s])].fillIcon = this.defcolor
        // this.datas[this.datas.findIndex(dataC => dataC.title === this.selectedP[s])].iconborderColor = this.opacity


      }

      const myArrayFiltered = this.datas.filter( el => {
        return this.selectedP.every( f => {
          return f !== el.wellName;
        });
      });

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
    
    sortSelected(sortp){
      let arrayGas = []
      // alert(sortp);
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
     
    },

    addData(){
            if (this.btnIsClick) {

      this.$router.push('/showcase')}
    }
  },
  async mounted(){
    this.tempD = await getDatafromDB();
    this.allData = await getDB(this.tempD)
    this.correctData = await restructureData(this.allData)

    this.datas = this.allData.map(v => ({...v, iconSize: this.normalIcon, iconColor: this.defcolor,  iconfillColor: this.lessopacity, iconborderColor: this.transparent, fillIcon: this.deffillcolor}))
    this.width = this.$refs.myMap.$el.clientWidth
      // console.log(this.$refs.myMap.$el.clientWidth)
    // if(this.width > 1200){
    //     this.xResponsive = 0
    //   }else{
    //     this.xResponsive = 200
    //   }

  },
  // computed:{
  //   wss(){
  //     // this.width = this.$refs.myMap.$el.clientWidth
  //     // console.log(this.width)
  //     console.log(this.$refs.myMap)
  //     if(this.$refs.myMap.$el.clientWidth > 1000){
  //       return 200
  //     }else{
  //       return 0
  //     }
  //     // return this.xResponsive
  //   }
  // },

  
  // watch:{
  //   width:function(n){
  //     if(n > 1200){
  //       this.xResponsive = 0
  //     }else{
  //       this.xResponsive = 200
  //     }
  //     // console.log('w', this.xResponsive)
  //   },
    // xResponsive:function(newW){
    //   console.log('width', newW)

    // }
  // },
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