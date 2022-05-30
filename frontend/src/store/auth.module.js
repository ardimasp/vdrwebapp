import authService from "../services/auth.service";

const user = localStorage.getItem('user');
const initialState = user ? {logged: true, user, username:"", permission:""} : {logged:false, user:null, username:null, permission:null};

export default {
    state: initialState,
    mutations:{
        LOGIN_SUCCESS(state, data){
            state.logged = true;
            state.user = data.access_token;
            state.username = data.name;
            state.permission = data.type;
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
        }
    },
    actions: {
        login({commit}, data){
            return authService.login(data).then(
                data => {
                    commit('LOGIN_SUCCESS', data.data);
                    console.log("logged in", data.status)
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
        }
    }
}