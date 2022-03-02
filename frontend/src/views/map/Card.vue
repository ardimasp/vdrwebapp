<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :loading="loading"
      class="mx-auto my-12"
      :class="{ 'overflow-auto': hover, 'overflow-hidden': !hover }"
      max-width="374"
      max-height="500"
    >
      <template slot="progress">
        <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
      </template>

      <v-carousel height="250">
        <v-carousel-item
          v-for="(item, i) in items"
          :key="i"
          :src="item"
          reverse-transition="fade-transition"
          transition="fade-transition"
        ></v-carousel-item>
      </v-carousel>

      <v-card-title>{{ title }}</v-card-title>

      <!-- <v-card-actions>
      <v-btn
        color="deep-purple lighten-2"
        text
        @click="reserve"
      >
        Reserve
      </v-btn>
    </v-card-actions> -->

      <v-simple-table>
        <template v-slot:default>
          <tbody>
            <tr v-for="(item, i) in details" :key="i">
              <td>{{ item.name }}</td>
              <td>{{ item.data }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  data: () => ({
    loading: false,
    selection: 1,
  }),
  props: {
    title: String,
    details: Array,
    items: Array,
  },
  methods: {
    reserve() {
      console.log(this.details)
    },
  },
}
</script>
