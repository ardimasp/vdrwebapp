<template>
<v-card>
  <v-row>
    <v-col>
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
    </v-col>
    <!-- <spacer/> -->

    <v-col class="mt-2" v-if="mapfilterPage=='visualization'">
    <v-btn
            color="primary"
            small
            @click="addVTP"

          >
            Add VTP
          </v-btn>
    </v-col>
  </v-row>
  <v-treeview
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

    // mounted: function() {
    //   // console.log(this.dataMaps)
    //   //   var temp = []
    //   //   for (let i = 0; i < this.dataMaps.length; i++) {
    //   //   temp.push(this.dataMaps[i].title);
    //   //   }
    //   //   this.mapTitle = temp
    //   //   console.log(temp)
    // },
    
    methods:{
   
  //  perlu ganti yg di send
      selectedPlace: function(){
        //   var matches = [];
        //   for(var i in this.val){
        //     console.log(this.val[i])
        //     var idfind = this.val[i]
 
        //     this.mapData.forEach(function(e) {
        //         matches = matches.concat(e.children.filter(function(c) {
        //             return (c.id === idfind);
        //         }));
        //     });

        //     // place.push(temp)
        //   }
        // var result = matches.map(a => a.name);

        // console.log(Object.values(result))
        var result = this.val
        console.log(result)

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