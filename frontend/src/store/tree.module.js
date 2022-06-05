import fileService from '../services/file.service';

export default {
    state: {
        list: [],
        length: 20,
    },
    mutations: {
        UPDATE_TREE(state, payload){
            state.list = payload;
        },
        UPDATE_LENGTH(state, payload){
            state.length = payload;
        },
    },
    actions: {
        fetchTreeList(context){
            return fileService.fetchFiles().then(
                data => {
                    context.commit('UPDATE_TREE', data.data);
                    console.log("fetch files", data.data)
                    return data.data;
                },
                error => {
                    return Promise.reject(error);
                }
            )
        },
        resetFileList(context){
            context.commit('UPDATE_TREE', [])
        }
    }
}