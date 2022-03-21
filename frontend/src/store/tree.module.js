import treedata from "./../dummy/treedata"
import { searchFile, searchFolder, searchDelFile, searchDelFolder } from "./searchTree";

export default {
    state: {
        list: treedata,
        length: 19,
    },
    mutations: {
        UPDATE_TREE(state, payload){
            state.list = payload;
        },
        UPDATE_LENGTH(state, payload){
            state.length = payload;
        },
        DELETE_FILE_TREE(state, data){
            const list = state.list;
            list.forEach(item => {
                searchDelFile(item, data);
            })
        },
        DELETE_FOLDER_TREE(state, id){
            const list = state.list;
            list.forEach(item=> {
                if (item.id == id){
                    let found = list.indexOf(item);
                    list.splice(found, 1);
                    console.log("found at root");
                }
                else searchDelFolder(item, id);
            })
        }
    },
    actions: {
        addFolder(context, data){
            const list = context.state.list;
            const length = context.state.length;
            if (typeof data.active === 'undefined' || data.active === null || data.active == 0){
                list.push({
                    id: length+1,
                    type: 'folder',
                    name: data.name,
                    children: []
                })
            } else {
                list.forEach(item => {
                    searchFolder(item, data.name, data.active, length)
                })
            }
            context.commit('UPDATE_TREE', list);
            context.commit('UPDATE_LENGTH', length+1);
        },
        addFile(context, data){
            const list = context.state.list;
            const length = context.state.length;
            const files = data.newFile;
            const size = data.size;
            const active = data.active;
            if (typeof active === 'undefined' || active === null || active == 0){
                for (let i = 0; i< size;i++){
                    list.push(files[i])
                }
            } else {
                list.forEach(item => {
                    searchFile(item, files, active, length, size)
                })
            }
            context.commit('UPDATE_TREE', list);
            context.commit('UPDATE_LENGTH', length+size);
        },
        deleteFile(context, data){
            context.commit('DELETE_FILE_TREE', data);
        },
        deleteFolder(context, data){
            context.commit('DELETE_FOLDER_TREE', data);
        }
    }
}