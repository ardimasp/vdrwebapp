import store from '../../store/index'

export const deleteFiles = (array) => {
    let arr = [], index;
    for (let i in array){
        index = store.state.files.list.indexOf(array[i]);
        arr.push(index);
    }
    arr.sort(function(a,b) {return b-a});

    for(let i in arr){
        store.dispatch("removeFromFiles", arr[i]);
    }
}

export const filelist = () => {
    const filelist = store.state.files.list
    return { filelist }
}

export const folderlist = () => {
    const folderlist = store.state.folder.list
    return { folderlist }
}

export const foldertab = () => {
    const foldertab = store.state.folder.tab
    return {foldertab}
}