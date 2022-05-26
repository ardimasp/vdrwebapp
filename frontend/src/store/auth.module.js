import authService from "../services/auth.service";

const user = localStorage.getItem('user');
const initialState = user ? {logged: true, user, username:"", permission:""} : {logged:false, user:null, username:null, permission:null};

export default {
    state: initialState,
    mutations:{
        LOGIN_SUCCESS(state, data){
            state.logged = true;
            state.user = data
        },
        LOGIN_FAIL(state){
            state.logged = false;
            state.user = null;
        },
        LOGOUT(state){
            state.logged = false;
            state.username = null;
            state.user = null;
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
                    commit('LOGIN_SUCCESS', data.data.access_token);
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