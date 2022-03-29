<template>
<v-card>
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
  <v-treeview
    selectable
    color="#9155fd"
    :search="search"
    v-model="val"
    :items="mapData"
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
    },

    data: function() {
        return {
            val: this.value,
            mapTitle: [],
            search: null,
            caseSensitive: false,

            mapData: [
                {
                id: 1,
                name: 'Applications :',
                children: [
                    { id: 2, name: 'Dayana Lead' },
                ],
                },
                {
                id: 3,
                name: 'Documents :',
                children: [
                    {
                    id: 4,
                    name: 'Fiki Lead',
                    
                    },
                    
                ],
                },
                {
                id: 5,
                name: 'Downloads :',
                children: [
                    { id: 6, name: 'Jambal Lead' },
                 
                ],
                },
                {
                id: 7,
                name: 'Videos :',
                children: [
                    {
                    id: 8,
                    name: 'Kabaena Carbonate Lead',
                    
                    },
                    {
                    id: 9,
                    name: 'Delta Utara Lead',
                    
                    },
                    {
                    id: 10,
                    name: 'Maniang Lead',
                    
                    },
                ],
                },
            ],

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
          var matches = [];
          for(var i in this.val){
            console.log(this.val[i])
            var idfind = this.val[i]
 
            this.mapData.forEach(function(e) {
                matches = matches.concat(e.children.filter(function(c) {
                    return (c.id === idfind);
                }));
            });

            // place.push(temp)
          }
        var result = matches.map(a => a.name);

        console.log(Object.values(result))


        this.$emit('input', result)
      }
    }
  }
</script>

<style lang="scss" scoped>
button + button.v-treeview-node__checkbox{ display: none !important; }


</style>