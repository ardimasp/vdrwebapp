import Vue from 'vue'
import Vuex from 'vuex'
import adminModule from './admin.module'

import treeModule from './tree.module'
import viewerModule from './viewer.module'
import authModule from './auth.module'
import testModule from './test.module'
Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tree: treeModule,
    viewer: viewerModule,
    admin: adminModule,
    auth: authModule,
    test: testModule
  },
  state: {
    initialLoad: false,
    alert: false,
  },
  mutations: {
    SET_LOAD(state, data){
      state.initialLoad = data;
    },
    SET_ALERT(state, data){
        state.alert = data;
    }
  },
  actions: {
    setLoad(context, data){
      context.commit('SET_LOAD', data)
    },
    setAlert(context, data){
        context.commit("SET_ALERT", data);
    }
  },
})
