import Vue from 'vue'
import Vuex from 'vuex'
import adminModule from './admin.module'

import treeModule from './tree.module'
import viewerModule from './viewer.module'
import authModule from './auth.module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tree: treeModule,
    viewer: viewerModule,
    admin: adminModule,
    auth: authModule,
  },
  state: {
    url: "https://ec2-13-250-37-201.ap-southeast-1.compute.amazonaws.com/api/v1/common",
    initialLoad: false,
    alert: false,
  },
  mutations: {
    SET_LOAD(state, data){
      state.initialLoad = data;
      console.log("at set load commit", state.initialLoad)
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
