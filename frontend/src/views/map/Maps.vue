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
      :x="10"
      :y="50"
      title="Select Wells"
      :w="300"
      :h="200"
    >
     <template>
       <map-filter :dataMaps="dataMaps" v-on:input="placeSelected"></map-filter>
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
      opacity: 1,
      lessopacity: 0.8,
      defcolor: '#004E40',
    }
  },
  mounted:function(){
    this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, iconColor: this.defcolor}))
    console.log(this.colorSort)

    // this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, opac: this.lessopacity, iconImg: this.defaulticon}))
    // console.log(datas)
  },

  methods: {
    placeSelected(point){
      this.selectedP = point
      console.log(this.selectedP)
      for (var s in this.selectedP){
        this.datas[this.datas.findIndex(dataC => dataC.title === this.selectedP[s])].iconSize = this.largeIcon
      }

      const myArrayFiltered = this.datas.filter( el => {
        return this.selectedP.every( f => {
          return f !== el.title;
        });
      });

      for (var ns in myArrayFiltered){
        var nsid = myArrayFiltered[ns].id
        console.log(nsid)

        this.datas[nsid].iconSize = this.normalIcon
      }
      console.log(myArrayFiltered)
    },

    funcVol(arrayGas){
          let sortedarrayGas = arrayGas.sort(function(a,b) {
            return a[3]-b[3]
          });
          // HERE COLOR
          // this.colorSort = colorRange

          // OPACITY SORT
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
            var totalColor = Math.round(sortedarrayGas.length / this.colorSort.length)
            console.log(totalColor)
            for(let i in this.colorSort){
              var tempAr = Array(totalColor).fill(this.colorSort[i])
              newtotalC = newtotalC.concat(tempAr)
            }
            for(let i in sortedarrayGas){
              sortedarrayGas[i].push(newtotalC[i])
            }
          }

          for (let s in sortedarrayGas){
            var sortSelect = this.datas.findIndex(dataC => dataC.id === sortedarrayGas[s][0]) 
            console.log(sortSelect)
            console.log(sortedarrayGas[s][5])

            // this.datas[sortSelect].opac = sortedarrayGas[s][4]
            this.datas[sortSelect].iconColor = sortedarrayGas[s][5]

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
          this.datas[i].iconColor = this.defcolor
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
    z-index: 999;
    position: relative;
    margin-top: 20px;
    left: 50%;
    transform: translate(-50%, 0);
  }

/* // .fixedcontainer {
//   position: absolute;
//   left: 0px;
//   top: 0px;
// } */
</style>