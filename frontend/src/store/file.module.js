import filedata from '../dummy/filedata'

export default {
    state: {
        list: filedata
    },
    mutations: {
        UPDATE_LIST(state, payload){
            state.list = payload;
          },
          DELETE_LIST(state, index){
            // console.log("del from vuex", index);
            state.list.splice(index, 1);
          }
    },
    actions: {
        addToList(context, data){
            const list = context.state.list;
            list.push(data);
            context.commit('UPDATE_LIST', list);
          },
          removeFromList(context, index){
            context.commit("DELETE_LIST", index);
          }
    }
}