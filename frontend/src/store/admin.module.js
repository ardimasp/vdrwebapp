import adminService from '../services/admin.service';

export default {
    state: {
        userList: [],
    },
    mutations: {
        UPDATE_USERLIST(state, payload) {
            state.userList = payload;
        }
    },
    actions: {
        fetchUserList(context){
            console.log("admin get user");
            return adminService.fetchUsers().then(
                data => {
                    context.commit('UPDATE_USERLIST', data.data)
                    return data.data;
                },
                error => {
                    return Promise.reject(error)
                }
            )
        }
    }
}
