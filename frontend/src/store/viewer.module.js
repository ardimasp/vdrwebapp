export default {
    state: {
        list: [],
    },
    mutations: {
        UPDATE_VIEWER_LIST(state, payload){
            state.list = payload;
        }
    },
    actions: {
        addToViewerList(context, data){
            const list = context.state.list;
            data.x_data = [1,3,5,7,0,3,4,6,8,1];
            data.y_data = [0,6,5,3,1,9,7,4,2,3];
            list.push(data);
            context.commit('UPDATE_VIEWER_LIST', list);
        }
    }
}