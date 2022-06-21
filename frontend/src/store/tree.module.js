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
            return fileService.fetchFilesPointer("sreeya", true).then(
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
            var list;
            return fileService.fetchFilesPointer("vtp-well", true).then(
                data => {
                    list = data.data

                    return fileService.fetchFilesPointer("vtp-line", true).then(
                        data1 => {
                            for(let i = 0; i<data1.data.length;i++) list.push(data1.data[i])

                            return fileService.fetchFilesPointer("vtp-surface", true).then(
                                data2 => {
                                    for(let j = 0; j<data2.data.length;j++) list.push(data2.data[j])
                                    context.commit('UPDATE_VTP', list)
                                },
                                error2 => {
                                    return Promise.reject(error2)
                                }
                            )
                        },
                        error1 => {
                            return Promise.reject(error1)
                        }
                    )

                    
                    // return data.data;
                },
                error => {
                    return Promise.reject(error)
                }
            )
        }
    }
}