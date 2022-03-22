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
            console.log("list", state.list)
        },
        UPDATE_LENGTH(state, payload){
            state.length = payload;
            console.log("tree size", state.length);
        },
        DELETE_FILE_TREE(state, data){
            const list = state.list;
            data.sort(function(a,b){return b-a});
            let item;
            const size = data.length;
            for(let i = 0; i < list.length; i++){
                item = list[i];
                if (data.includes(item.id)) {
                    let found = list.indexOf(item);
                    list.splice(found, 1);
                    i--;
                }
                else searchDelFile(item, data, size);
            }
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
            const id = data.id;
            if (typeof data.active === 'undefined' || data.active === null || data.active == 0){
                list.push({
                    id: id,
                    type: 'folder',
                    name: data.name,
                    children: []
                })
            } else {
                list.forEach(item => {
                    searchFolder(item, id, data.name, data.active)
                })
            }
            context.commit('UPDATE_TREE', list);
            context.commit('UPDATE_LENGTH', context.state.length+1);
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