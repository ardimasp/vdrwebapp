<template>
<v-card>
  <!-- <v-row> -->
    <div class="d-flex justify-space-between">
    <!-- <v-col> -->
    <v-text-field
        color="black"
        v-model="search"
        label="Search Wells"
        dark
        flat
        solo-inverted
        hide-details
        clearable
    ></v-text-field>
    <!-- <v-spacer></v-spacer> -->
    <!-- </v-col> -->
    <!-- <spacer/> -->

    <!-- <v-col class="mt-2" v-if="mapfilterPage=='visualization'"> -->
    <v-btn v-if="mapfilterPage=='visualization'"
            color="primary"
            small
            @click="addVTP"
          class="mt-2 mr-3"
          >
            Add VTP
          </v-btn>
    <!-- </v-col> -->
    </div>
  <!-- </v-row> -->
  <v-treeview v-if="mapfilterPage=='visualization'"
    selectable
    color="#9155fd"
    :search="search"
    v-model="val"
    :items="dataMaps"
    item-key="id"
    @input="selectedPlace()"

  ></v-treeview>

  <v-treeview v-if="mapfilterPage=='showcase'"
    selectable
    color="#9155fd"
    :search="search"
    v-model="val"
    :items="dataMaps"
    item-key="name"
    @input="selectedPlace()"

  ></v-treeview>

</v-card>
</template>

<script>
// import { mdiCloseCircle } from '@mdi/js'

  export default {
    //   components:{
    //           mdiCloseCircle

    //   },
   name: "MapFilter",
    props:{
        dataMaps: Array,
        value: Array,
        mapfilterPage: String
    },

    data: function() {
        return {
            val: this.value,
            mapData: this.dataMaps,
            search: null,
            caseSensitive: false,
        }
    },
    
    methods:{
   
      selectedPlace: function(){

        var result = this.val

        this.$emit('input', result)
      },

      addVTP(){
        this.$router.push('/vtp-form')
      }
    }
  }
</script>

<style lang="scss" scoped>
button + button.v-treeview-node__checkbox{ display: none !important; }


</style>