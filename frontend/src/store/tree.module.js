import fileService from '../services/file.service';

export default {
    state: {
        list: [],
        sreeya: [],
        vtp: [],
    },
    mutations: {
        UPDATE_TREE(state, payload){
            state.list = payload;
        },
        UPDATE_SREEYA(state, payload){
            state.sreeya = payload;
        },
        UPDATE_VTP(state, payload){
            state.vtp = payload;
        }
    },
    actions: {
        fetchTreeList(context){
            return fileService.fetchFiles().then(
                data => {
                    context.commit('UPDATE_TREE', data.data);
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
            return fileService.fetchFilesPointer("production", true).then(
                data => {
                    context.commit('UPDATE_SREEYA', data.data);
                    return data.data;
                },
                error => {
                    return Promise.reject(error);
                }
            )
        },
        fetchVtpList(context){
            return fileService.fetchFilesMultiPointer("pointers=well-vtp&pointers=surface-vtp&pointers=line-vtp", true).then(
                data => {
                    context.commit('UPDATE_VTP', data.data)
                    return data.data;
                },
                error => {
                    return Promise.reject(error)
                }
            )
        }
    }
}