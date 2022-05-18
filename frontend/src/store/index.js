import Vue from 'vue'
import Vuex from 'vuex'

import treeModule from './tree.module'
import userModule from './user.module'
import viewerModule from './viewer.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {},
  actions: {},
  modules: {
    tree: treeModule,
    viewer: viewerModule,
    user: userModule
  },
})
