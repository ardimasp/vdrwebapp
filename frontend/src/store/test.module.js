export default {
    state: {
        isDrawerOpen: true,
    },
    mutations: {
        UPDATE_DRAWER(state, payload){
            state.isDrawerOpen = payload;
        }
    },
    actions: {
        updateDrawer(context, data){
            context.commit("UPDATE_DRAWER", data)
        }
    }
}