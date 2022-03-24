import filedata from '../dummy/filedata'

export default {
    state: {
        list: filedata
    },
    mutations: {
        UPDATE_FILE(state, payload){
            state.list = payload;
          },
          DELETE_FILE(state, index){
            state.list.splice(index, 1);
          }
    },
    actions: {
        addToFiles(context, data){
            const list = context.state.list;
            list.push(data);
            context.commit('UPDATE_FILE', list);
          },
          removeFromFiles(context, index){
            context.commit("DELETE_FILE", index);
          }
    }
}