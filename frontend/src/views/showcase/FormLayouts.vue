<template>
<div>
  <v-row class="match-height">

    <!-- Multiple Column -->
    <v-col cols="12">
      <v-card>
        <v-card-title>Add Map Data</v-card-title>
        <v-card-text>
          <FormToBeFill/>
        </v-card-text>
        <div id="app">
        <!-- <input type="text" v-model="query" /> -->
        <!-- <button type="button" v-on:click="search()">Search</button> -->
        <!-- <HereMap ref="map2" lat="-3.092642" lng="115.283758"/> -->
    </div>
      </v-card>
    </v-col>
  </v-row>
   <div style="position: absolute;">
      <!-- <v-snackbar
        v-model="snackbar"
        right
        :color="status"
        elevation="24"
        style="position: absolute;"
      >
        {{resultPost}}
      </v-snackbar> -->
      </div>
</div>
</template>

<script>

import FormToBeFill from './FormToBeFill.vue'
export default {
  components: {
    FormToBeFill,
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
