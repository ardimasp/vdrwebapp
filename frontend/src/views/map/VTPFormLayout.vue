<template>
  <v-row class="match-height">

    <!-- Multiple Column -->
    <v-col cols="12">
      <v-card>
        <v-card-title>Add VTP Data</v-card-title>
        <v-card-text>
          <VTPForm/>
        </v-card-text>
        <div id="app">
        <!-- <input type="text" v-model="query" /> -->
        <!-- <button type="button" v-on:click="search()">Search</button> -->
        <!-- <HereMap ref="map2" lat="-3.092642" lng="115.283758"/> -->
    </div>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>

import VTPForm from './VTPForm.vue'
export default {
  components: {
    VTPForm,
  },
  setup() {
    return {}
  },
  data() {
            return {
                query: "Starbucks"
            }
        },
  methods: {
      search() {
          this.$refs.map2.places(this.query);
      }
  }
}
</script>

<style scoped>

.match-height{
  margin-top: 0px;
}

</style>
