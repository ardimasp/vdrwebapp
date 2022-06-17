<template>
  <l-map
    style="z-index: 10;"

    ref="map"
    @dblclick="onMapClick"
    :zoom="zoom"
    :center="[
      position.lat || userLocation.lat || defaultLocation.lat,
      position.lng || userLocation.lng || defaultLocation.lng
    ]"
  >
    <l-tile-layer
      :url="tileProvider.url"
      :attribution="tileProvider.attribution"
    />
    <l-geosearch :options="geoSearchOptions"></l-geosearch>
    <l-marker
      v-if="position.lat && position.lng"
      visible
      draggable
      :icon="icon"
      :lat-lng.sync="position"
      @dragstart="dragging = true"
      @dragend="dragging = false"
    >
      <l-tooltip :content="tooltipContent" :options="{ permanent: true }" />
    </l-marker>
  </l-map>
</template>
<script>

import { LMap, LMarker, LTileLayer, LTooltip } from "vue2-leaflet";
import { OpenStreetMapProvider } from "leaflet-geosearch";
import LGeosearch from "vue2-leaflet-geosearch";
import { icon } from "leaflet";

export default {
    name: 'SearchLocation',

  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LGeosearch
  },
  props: {
    ind: Number,
    value: {
      type: Object,
      required: true
    },
    defaultLocation: {
      type: Object,
      default: () => ({
        lat: -3.092642,
        lng: 115.283758
      })
    }
  },
  data() {
    return {
      loading: false,
      geoSearchOptions: {
        provider: new OpenStreetMapProvider(),
        showMarker: false,
        autoClose: true
      },
      userLocation: {},
      icon: icon({
        iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
        iconUrl: require("leaflet/dist/images/marker-icon.png"),
        shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
        iconSize: [24,36],
        iconAnchor: [12,36]      
      }),
      position: {},
      address: "",
      tileProvider: {
        // attribution:
        //   '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        // url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
         url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      },
      zoom: 5,
      dragging: false
    };
  },
  mounted() {
    console.log('i', this.ind)
    this.getUserPosition();
    this.$refs.map.mapObject.on("geosearch/showlocation", this.onSearch);
  },

  watch: {
    position: {
      deep: true,
      async handler(value) {
        this.address = await this.getAddress();
        this.$emit("input", { position: value, address: this.address, index: this.ind });
      }
    }
  },
  computed: {
    tooltipContent() {
      if (this.dragging) return "...";
      if (this.loading) return "Loading...";
      return `<strong style="font-family: "Inter", sans-serif;">${this.address.replace(
        ",",
        "<br/>"
      )}</strong> <hr/><strong class="toolTip" style="font-family: "Inter", sans-serif;">lat:</strong> ${
        this.position.lat
      }<br/> <strong style="font-family: "Inter", sans-serif;">lng:</strong> ${this.position.lng}`;
    }
  },
  methods: {
    async getAddress() {
      this.loading = true;
      let address = "Unresolved address";
      try {
        const { lat, lng } = this.position;
        const result = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`
        );
        if (result.status === 200) {
          const body = await result.json();
          address = body.display_name;
        }
      } catch (e) {
        console.error("Reverse Geocode Error->", e);
      }
      this.loading = false;
      return address;
    },
    async onMapClick(value) {
      // place the marker on the clicked spot
      this.position = value.latlng;
      // this.$emit("input", { position: t, address: this.address, indexMap: this.ind });

    },
    onSearch(value) {
      const loc = value.location;
      this.position = { lat: loc.y, lng: loc.x };
    },
    async getUserPosition() {
      if (navigator.geolocation) {
        // get GPS position
        navigator.geolocation.getCurrentPosition(pos => {
          // set the user location
          this.userLocation = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
          };
        });
      }
    },
  }
};
// https://medium.com/swlh/create-an-interactive-location-selector-with-vue-js-and-leaflet-5808c55b4636
</script>

<style scoped>
.toolTip{
  font-family: "Inter", sans-serif;
}

.leaflet-container {
    font: 12px/1.5 "Helvetica Neue", Arial, Helvetica, sans-serif;
    font-style: normal;
    font-variant-ligatures: normal;
    font-variant-caps: normal;
    font-variant-numeric: normal;
    font-variant-east-asian: normal;
    font-weight: normal;
    font-stretch: normal;
    font-size: 12px;
    line-height: 1.5;
    font-family: "Inter", sans-serif;
}
</style>