<template>
  <div>
    <div class="container">
<v-row>
    <MapSort v-on:input="sortSelected" />

    <MapList :dataMaps="dataMaps" v-on:input="placeSelected"/>
</v-row>
    </div>

    <MapNavigation :dataMaps="datas" :heatmap="heatmap"></MapNavigation>
  </div>
</template>

<script>
import MapNavigation from './MapNavigation.vue'
import 'leaflet/dist/leaflet.css'
// import L from 'leaflet'
import { cardData } from './Dummy.js'
import MapList from './MapList.vue'
import MapSort from './MapSort.vue'

export default {
  components: {
    MapNavigation,
    MapList,
    MapSort
  },
    data: function() {
    return {
      dataMaps: cardData,
      value: [],
      selectedP: null,
      normalIcon: [30, 30],
      largeIcon: [60,60],
      datas: [],
      previousSelection: [],
      sortby: null,
      heatmap: [],
      opacity: 1,
      lessopacity: 0.5
    }
  },
  mounted:function(){

    this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, opac: this.lessopacity}))
    console.log(datas)
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
        this.datas[dataSelect].opac = this.opacity

      } else if (this.previousSelection.length > this.selectedP.length) {
        arrayD = this.previousSelection.filter(x => !this.selectedP.includes(x))[0]
        dataSelect = this.datas.findIndex(dataC => dataC.title === arrayD) 
        this.datas[dataSelect].iconSize = this.normalIcon
        this.datas[dataSelect].opac = this.lessopacity

      }
      console.log('selected = ', arrayD)
      
      this.previousSelection = this.selectedP
      console.log('selection = ', this.selectedP)
    },

    sortSelected(sortp){
      let arrayGas = []
      alert(sortp);
      if(sortp == "Gas Volume"){
        for (let i in this.dataMaps){
          arrayGas.push([this.dataMaps[i].id, this.dataMaps[i].data.coordinates.pos[0], this.dataMaps[i].data.coordinates.pos[1], this.dataMaps[i].size])
          // alert(arrayGas)

        }
          let sortedarrayGas = arrayGas.sort(function(a,b) {
            return a[3]-b[3]
          });

          let x = sortedarrayGas.map(function(val) {
            return val.slice(0, -1);
          });
          console.log(sortedarrayGas)
          var intensity = 1/x.length
          for(let i in x){
            x[i].push(intensity)
            intensity = intensity + 1/x.length;
          }
          this.heatmap = x
          console.log(x)

          for (let s in x){
            var sortSelect = this.datas.findIndex(dataC => dataC.id === x[s][0]) 
            console.log(sortSelect)
                    console.log(x[s][3])

            this.datas[sortSelect].opac = x[s][3]
        
        }
      }else if(sortp == null){
        this.datas = this.dataMaps.map(v => ({...v, iconSize: this.normalIcon, opac: this.lessopacity}))
      }
      
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


</style>