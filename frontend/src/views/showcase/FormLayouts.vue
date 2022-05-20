<template>
  <v-row class="match-height">

    <!-- Multiple Column -->
    <v-col cols="12">
      <v-card>
        <v-card-title>Multiple Column</v-card-title>
        <v-card-text>
          <FormToBeFill/>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
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
}
</script>

<style scoped>

.match-height{
  margin-top: 50px;
}
</style>
