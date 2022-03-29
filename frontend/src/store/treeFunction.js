let search = false;

export const searchStatus = () => {return search};

export const searchFile = (item, files, active, size) => {
    search = false;
    if(item.type == "folder") {
        if(item.id == active){
            for (let i = 0; i< size;i++){
                item.children.push(files[i])
            }
            search = true;
        }
        else searchFile(item.children, files, active, size);
    }
    else if (item.length){
        for(let i = 0; i < item.length; i++){
            searchFile(item[i], files, active, size)
    
            if(search) break;
            continue;
        }
    }
    return
}

export const searchFolder = (item, id, name, active) => {
    search = false;
    if(item.type == "folder") {
        if(item.id == active){
            item.children.push({
                id: id,
                type: 'folder',
                name: name,
                children: []
              });
            search = true;
        }
        else searchFolder(item.children, id, name, active);
    }
    else if (item.length){
        for(let i = 0; i < item.length; i++){
            searchFolder(item[i], id, name, active)
    
            if(search) break;
            continue;
        }
    }
    return
}

export const searchDelFolder = (item, id) => {
    search = false;
    if(item.type == "folder") {
        // item.id >= 0 prevent undefined
        // some almost the same as include -> check if exist
        if(item.id >= 0 && item.children.some(el => el.id == id)){
            let index = item.children.findIndex(x => x.id == id);
            item.children.splice(index, 1);
            search = true;
        }
        else searchDelFolder(item.children, id);
    }
    else if (item.length){
        for(let i = 0; i < item.length; i++){
            searchDelFolder(item[i], id)
    
            if(search) break;
            continue;
        }
    }
    return
}

let count = 0;
export const countStatus = () => {return count}
export const countIncrement = () => {count++}
export const countReset = () => {count = 0}

export const searchDelFile = (item, arr) => {
    if(item.type == "folder") {
        for(let i = 0; i < item.children.length; i++){
            if (arr.includes(item.children[i].id)){
                if (item.children[i].type == "file") {
                    item.children.splice(i, 1);
                    i--;
                    count++;
                }
            }
            if(count == arr.length) break;
            continue;
        }
        if (item.children.length) searchDelFile(item.children, arr);
    }
    else if (item.length){
        for(let i = 0; i < item.length; i++){
            searchDelFile(item[i], arr)
    
            if(count == arr.length) break;
            continue;
        }
    }
    return
}