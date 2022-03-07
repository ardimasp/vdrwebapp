<template>
  <div>
    <div class="container">
       <vtk-card 
      :x="600"
      :y="0"
      title="3D View"
      :w="400"
      :h="500"
    >
    </vtk-card>

    <regular-card 
      :x="0"
      :y="0"
      title="Select Wells"
      :w="400"
      :h="200"
    >
     <template>
       <test-content></test-content>
     </template>
    </regular-card>
    
      <v-row>
          <MapSort v-on:input="sortSelected" />

          <MapList :dataMaps="dataMaps" v-on:input="placeSelected"/>
      </v-row>
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
import MapList from './MapList.vue'
import MapSort from './MapSort.vue'

import RegularCard from '../viewer/RegularCard.vue'
import TestContent from '../viewer/TestContent.vue'
import VtkCard from '../viewer/VtkCard.vue'

import oilgas from '../../assets/images/oil&gas.png'

export default {
  components: {
    MapNavigation,
    MapList,
    MapSort,
    RegularCard,
    TestContent,
    VtkCard
  },
    data: function() {
    return {
      dataMaps: cardData,
      value: [],
      selectedP: null,
      normalIcon: [50, 50],
      largeIcon: [100,100],
      datas: [],
      previousSelection: [],
      sortby: null,
      heatmap: [],
      opacity: 1,
      lessopacity: 0.8,
      defaulticon: oilgas
    }
  },
  mounted:function(){

    this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, opac: this.lessopacity, iconImg: this.defaulticon}))
    // console.log(datas)
  },

  methods: {
    placeSelected(point){
      let dataSelect
      this.selectedP = point
      console.log('prev =',this.previousSelection)

      let arrayD = null

      if (this.previousSelection.length < this.selectedP.length) {
        arrayD = this.selectedP.filter(x => !this.previousSelection.includes(x))[0] 
        dataSelect = this.datas.findIndex(dataC => dataC.title === arrayD) 
        this.datas[dataSelect].iconSize = this.largeIcon

      } else if (this.previousSelection.length > this.selectedP.length) {
        arrayD = this.previousSelection.filter(x => !this.selectedP.includes(x))[0]
        dataSelect = this.datas.findIndex(dataC => dataC.title === arrayD) 
        this.datas[dataSelect].iconSize = this.normalIcon

      }
      console.log('selected = ', arrayD)
      
      this.previousSelection = this.selectedP
      console.log('selection = ', this.selectedP)


      // for (let i in this.selectedP){
      //   console.log(this.selectedP[i])
      //   dataSelect = this.datas.findIndex(dataC => dataC.title === this.selectedP[i]) 
      //   arrayD.push(dataSelect)
      // }
      // this.tempA = arrayD
      // console.log(arrayD)
      // for (let j in arrayD){
      //   this.datas[arrayD[j]].iconSize = this.largeIcon
      // }
      // if (this.selectedP === undefined || this.selectedP.length == 0){
      //   console.log(this.tempA)
      //   this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon}))

      // }
    },

    funcVol(arrayGas){
          let sortedarrayGas = arrayGas.sort(function(a,b) {
            return a[3]-b[3]
          });

          console.log(sortedarrayGas)
          var intensity = 1/sortedarrayGas.length
          for(let i in sortedarrayGas){
            sortedarrayGas[i].push(intensity)
            intensity = intensity + 1/sortedarrayGas.length;
          }
          this.heatmap = sortedarrayGas
          console.log(sortedarrayGas)

          for (let s in sortedarrayGas){
            var sortSelect = this.datas.findIndex(dataC => dataC.id === sortedarrayGas[s][0]) 
            console.log(sortSelect)
            console.log(sortedarrayGas[s][3])

            this.datas[sortSelect].opac = sortedarrayGas[s][4]
          }
    },
    
    sortSelected(sortp){
      let arrayGas = []
      alert(sortp);

      if(sortp == "Gas Volume"){
        for (let i in this.dataMaps){
          arrayGas.push([this.dataMaps[i].id, this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1], this.dataMaps[i].size])
          // alert(arrayGas)
        }
        this.funcVol(arrayGas)
      
      }
      else if(sortp == "Oil Volume"){
        for (let i in this.dataMaps){
          arrayGas.push([this.dataMaps[i].id, this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1], this.dataMaps[i].oilvolume])
          // alert(arrayGas)
        }
        this.funcVol(arrayGas)
      }
      else if(sortp == null){
        for (let i in this.dataMaps){
          this.datas[i].opac = this.lessopacity
        }
      }
      
      // let arrayGas = []
      // alert(sortp);
      // var size;
      // if(sortp == "Gas Volume"){
      //   for (let i in this.dataMaps){
      //     size = this.dataMaps[i].size;
      //     arrayGas.push([this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1], this.dataMaps[i].size])
      //     // alert(arrayGas)

      //   }
      // }
      // let sortedarrayGas = arrayGas.sort(function(a,b) {
      //     return a[2]-b[2]
      // });

      // let x = sortedarrayGas.map(function(val) {
      //   return val.slice(0, -1);
      // });
      // console.log(sortedarrayGas)
      // var intensity = 50
      // for(let i in x){
      //   x[i].push(intensity)
      //   intensity = intensity * 2;
      // }
      // this.heatmap = x
      // console.log(x)

    }
  }
}
</script>
<style lang="scss" scoped>

.container{
    z-index: 9998;
    position: absolute;
    margin-top: 10px;
    left: 50%;
    transform: translate(-50%, 0);
  }

/* // .fixedcontainer {
//   position: absolute;
//   left: 0px;
//   top: 0px;
// } */
</style>