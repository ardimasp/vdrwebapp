import '@/plugins/vue-composition-api'
import '@/styles/styles.scss'
import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'

import VueDraggableResizable from 'vue-draggable-resizable'
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'

import "leaflet/dist/leaflet.css";
import "leaflet-geosearch/dist/geosearch.css";
// import VueDragResize from 'vue-drag-resize'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  VueDraggableResizable,
  render: h => h(App),
}).$mount('#app')
