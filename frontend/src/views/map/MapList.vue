<template> 
    <v-col md="3">

        <div class="pa-4 text-no-wrap rounded-xl borderfilter" >

        <v-autocomplete
            v-model="val"
            :items="mapTitle"
            label="Select Item"
            multiple
            class=" white--text dropdown-filter"
            @input="selectedPlace()"
            color="white"
            clearable
            chips
            >
         
            <template v-slot:selection="{ item, index }">
                    <v-chip v-if="index === 0">
                    <span class="white--text">{{ item }}</span>
                    </v-chip>
                    <span
                    v-if="index === 1"
                    class="white--text text-caption"
                    >
                    (+{{ val.length - 1 }} others)
                    </span>
                </template>
          </v-autocomplete>
        </div>
    </v-col>
</template>

<script>

export default {
    name: "MapList",
    props:{
        dataMaps: Array,
        value: Array,
    },

    data: function() {
        return {
            val: this.value,
            mapTitle: [],
        }
    },

    mounted: function() {
        var temp = []
        for (let i = 0; i < this.dataMaps.length; i++) {
        temp.push(this.dataMaps[i].title);
        }
        this.mapTitle = temp
        console.log(temp)
    },
    
    methods:{
   
      selectedPlace: function(){
        var place = this.val
        this.$emit('input', place)
      }
    }
}
// https://vuetifyjs.com/en/components/selects/#selection
</script>
<style lang="scss" scoped>
  .borderfilter {
    // border: thin solid #df3131;
    border-radius:50px;
    background-color: #b365f2;

  }

  .dropdown-filter{
    background-color: #b365f2;
color: white;

  }

  // .container{
  //   z-index: 9998;
  //   position: absolute;
  //   margin-top: 10px;
  //   left: 50%;
  //   transform: translate(-50%, 0);
  // }

</style>