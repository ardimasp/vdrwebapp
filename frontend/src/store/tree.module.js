import fileService from '../services/file.service';

export default {
    state: {
        list: [],
        sreeya: [],
    },
    mutations: {
        UPDATE_TREE(state, payload){
            state.list = payload;
        },
        UPDATE_SREEYA(state, payload){
            state.sreeya = payload;
        }
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
        },
        fetchSreeyaList(context){
            return fileService.fetchFilesPointer("sreeya", true).then(
                data => {
                    context.commit('UPDATE_SREEYA', data.data);
                    console.log("fetch sreeya", data.data)
                    return data.data;
                },
                error => {
                    return Promise.reject(error);
                }
            )
        }
    }
}