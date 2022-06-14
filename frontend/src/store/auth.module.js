import authService from "../services/auth.service";

const user = localStorage.getItem('user');
// user = token, username = userid, alert = login alert when access expire
const initialState = user ? {logged: true, user, username:"", permission:"", string:""} : {logged:false, user:null, username:null, permission:null, string:null};

export default {
    state: initialState,
    mutations:{
        LOGIN_SUCCESS(state, data){
            state.logged = true;
            
            state.user = data.access_token;
            state.username = data.name;
            state.permission = data.type;
            console.log("at login",state.user, state.username)
        },
        LOGIN_FAIL(state){
            state.logged = false;
            state.user = null;
            state.username = null;
            state.permission = null;
        },
        LOGOUT(state){
            state.logged = false;
            state.user = null;
            state.username = null;
            state.permission = null;
        },
        SET_USER(state, data){
            state.username = data;
        },
        SET_PERMISSION(state, data){
            state.permission = data;
        },
        SET_STRING(state, data){
            state.string = data;
        },
        SET_TOKEN(state, data){
            state.user = data
        }
    },
    actions: {
        login({commit}, data){
            return authService.login(data).then(
                data => {
                    commit('LOGIN_SUCCESS', data.data);
                    // console.log("logged in", data.status)
                    return data.status;
                },
                error => {
                    commit('LOGIN_FAIL', data);
                    return Promise.reject(error);
                }
            )
        },
        logout(context){
            authService.logout();
            context.commit('LOGOUT');
        },
        setUsername(context, data){
            context.commit('SET_USER', data);
        },
        setPermission(context, data){
            context.commit('SET_PERMISSION', data)
        },
        setString(context, data){
            context.commit('SET_STRING', data)
        },
        setToken(context, data){
            context.commit("SET_TOKEN", data)
        }
    }
}