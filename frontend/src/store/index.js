import Vue from 'vue'
import Vuex from 'vuex'
import adminModule from './admin.module'

import treeModule from './tree.module'
import viewerModule from './viewer.module'
import authModule from './auth.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    url: "https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common"
  },
  mutations: {},
  actions: {},
  modules: {
    tree: treeModule,
    viewer: viewerModule,
    admin: adminModule,
    auth: authModule,
  },
})
