import folderdata from '../dummy/folderdata'

export default {
    state: {
        list: folderdata,
        tab: 1,
    },
    mutations: {
        UPDATE_FOLDER(state, payload){
          state.list = payload;
        },
        DELETE_FOLDER(state, index){
          // console.log("del from vuex", index);
          state.list.splice(index, 1);
        },
        UPDATE_TAB(state, tab_id){
          state.tab = tab_id;
        },
    },
    actions: {
        addToFolders(context, data){
          const list = context.state.list;
          list.push(data);
          context.commit('UPDATE_FOLDER', list);
        },
        removeFromFolders(context, index){
          context.commit("DELETE_FOLDER", index);
        },

        updateTab(context, tab_id){
          context.commit("UPDATE_TAB", tab_id);
        },
    }
}