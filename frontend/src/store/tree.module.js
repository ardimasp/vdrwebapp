import treedata from "./../dummy/treedata"
import { searchStatus, countStatus, countIncrement, searchFile, 
        searchFolder, searchDelFolder, searchDelFile, countReset } from "./treeFunction";

export default {
    state: {
        list: treedata,
        length: 20,
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
            data.sort(function(a,b){return b-a});
            let item;
            for(let i = 0; i < list.length; i++){
                item = list[i];
                if (data.includes(item.id)) {
                    let found = list.indexOf(item);
                    list.splice(found, 1);
                    i--;
                    countIncrement()
                }
                else searchDelFile(item, data);

                console.log("counter at root", countStatus())
                if(countStatus() == data.length) break;
                continue;
            }
            countReset();
        },
        DELETE_FOLDER_TREE(state, id){
            const list = state.list;
            for(let i = 0; i < list.length; i++){
                if (list[i].id == id){
                    list.splice(i, 1);
                    break
                }
                else searchDelFolder(list[i], id);

                if(searchStatus()) break;
                continue;
            }
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
                for (let i = 0; i < list.length; i++){
                    console.log("looping", i, "...");
                    searchFolder(list[i], id, data.name, data.active)
    
                    if(searchStatus()) break;
                    continue;
                }
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
                for (let i = 0; i < list.length; i++){
                    console.log("looping", i, "...");
                    searchFile(list[i], files, active, size)
    
                    if(searchStatus()) break;
                    continue;
                }
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