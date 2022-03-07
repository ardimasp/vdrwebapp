import Vue from 'vue'
import Vuex from 'vuex'

import FileModule from './file.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {},
  actions: {},
  modules: {
    files: FileModule
  },
})
