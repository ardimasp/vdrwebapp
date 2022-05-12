<template> 
    <!-- <v-col md="3"> -->
        <div class="pa-4 text-no-wrap rounded-xl borderfilter" >

        <v-autocomplete
            v-model="bysort"
            :items="sortitems"
            label="Sort By"
            clearable
            @input="selectedSort()"

            >
         
          </v-autocomplete>
        </div>
    <!-- </v-col> -->
</template>

<script>

export default {
    name: "MapSort",
    props:{
        sortby: String
    },

    data: function() {
        return {
            bysort: this.sortby,
            mapTitle: [],
            sortitems: ['Oil Volume', 'Gas Volume', 'Mix oil & gas volume'],
        }
    },

    methods:{
      selectedSort:function(){
        var chosensort = this.bysort
        this.$emit('input', chosensort)
      },
      
    }
}
// https://vuetifyjs.com/en/components/selects/#selection
</script>

<style lang="scss" scoped>
  .borderfilter {
    // border: thin solid #df3131;
    border-radius:50px;
    // background-color: #b365f2;
    // width: 40%;
  }

  // .dropdown-filter{
  //   // background-color: #b365f2;
  //   // color: white;

  // }

</style>