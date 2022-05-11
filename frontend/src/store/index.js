import Vue from 'vue'
import Vuex from 'vuex'

import FileModule from './file.module'
import folderModule from './folder.module'
import treeModule from './tree.module'
import viewerModule from './viewer.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {},
  actions: {},
  modules: {
    files: FileModule,
    folder: folderModule,
    tree: treeModule,
    viewer: viewerModule,
  },
})
