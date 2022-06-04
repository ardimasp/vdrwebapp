import '@/plugins/vue-composition-api'
import '@/styles/styles.scss'
import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from './router'
import store from './store'
import axios from 'axios'

import VueDraggableResizable from 'vue-draggable-resizable'
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'


// import VueDragResize from 'vue-drag-resize'

Vue.config.productionTip = false

new Vue({
  router,
  axios,
  store,
  vuetify,
  VueDraggableResizable,
  render: h => h(App),
}).$mount('#app')
