import treedata from "./../dummy/treedata"
import { searchFile, searchFolder } from "./searchTree";

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
        }
    },
    actions: {
        addFolder(context, data){
            // console.log("add folder", data.active, data.name)
            const list = context.state.list;
            const length = context.state.length;
            // let status = true;
            if (typeof data.active === 'undefined' || data.active === null || data.active == 0){
                list.push({
                    id: length+1,
                    type: 'folder',
                    name: data.name,
                    children: []
                })
                // console.log(list);
            } else {
                list.forEach(item => {
                    searchFolder(item, data.name, data.active, length)
                    // if(status){
                    //     status = searchFolder(item, data.name, data.active, length)
                    // } 
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
            const active = data.active
            // let status = true;
            // console.log("size", data.size)
            if (typeof active === 'undefined' || active === null || active == 0){
                for (let i = 0; i< size;i++){
                    list.push(files[i])
                }
            } else {
                list.forEach(item => {
                    // if(status){
                    //     status = searchFile(item, data.active, length, data.size)
                    // } 
                    searchFile(item, files, active, length, size)
                })
            }
            context.commit('UPDATE_TREE', list);
            context.commit('UPDATE_LENGTH', length+size);
        }
    }
}