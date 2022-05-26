export default {
    state: {
        id: "",
        permission: "",
    },
    mutations: {
        UPDATE_TOKEN(state,payload){
            state.id = payload;
        }
    },
    actions: {
        setUserToken(context, data){
            localStorage.setItem("token", data);
            context.commit("UPDATE_TOKEN", data);
        }
    }
}