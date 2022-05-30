export default {
    state: {
        id: "",
        permission: "",
        profile: "",
    },
    mutations: {
        UPDATE_TOKEN(state,payload){
            state.id = payload;
        },
        UPDATE_PROFILE(state,payload){
            state.profile = payload;
        }
    },
    actions: {
        setUserToken(context, data){
            localStorage.setItem("token", data);
            context.commit("UPDATE_TOKEN", data);
        },
        setProfile(context, data){
            context.commit("UPDATE_PROFILE", data)
        }
    }
}