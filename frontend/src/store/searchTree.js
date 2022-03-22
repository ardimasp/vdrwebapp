export const searchFolder = (item, id, name, active) => {
    Object.keys(item).forEach(key => {
        // check every key (id, name, type) if its an object
        if(typeof item[key] === "object") {
          // console.log("is an object", item[key]);
          // check the item.id directly n if its a folder
          if (item.id == active && item.type == "folder"){
            item.children.push({
              id: id,
              type: 'folder',
              name: name,
              children: []
            });
            return false;
          }
          // if no match found and there is an object
          else searchFolder(item[key], name, active);
        }
        return true;
    })
}

export const searchFile = (item, files, active, length, size) => {
  Object.keys(item).forEach(key => {
    // check every key (id, name, type) if its an object
    if(typeof item[key] === "object") {
      // console.log("is an object", item[key]);
      // check the item.id directly n if its a folder
      if (item.id == active && item.type == "folder"){
        for (let i = 0; i< size;i++){
          item.children.push(files[i])
        }
        console.log(active, size);
        return false;
      }
      // if no match found and there is an object
      else searchFile(item[key], files, active, length, size);
    }
    return true;
  })
}

export const searchDelFile = (item, arr) => {
  Object.keys(item).forEach(key => {
    if(typeof item[key] === "object") {
      console.log("item", item.id, item.type, item[key]);
      if (item[key].type === "file") {
        // console.log("child", item.length, item);
        // const length = item.length;
        for(let i = 0; i < item.length; i++){
          // console.log("loop", item[i].id);
          if (arr.includes(item[i].id)){
            item.splice(i, 1);
            // console.log("found", item.length);
            i--;
          }
        }
      }
      else searchDelFile(item[key], arr);
    }
  })
}

export const searchDelFolder = (item, id) => {
  Object.keys(item).forEach(key => {
    if(typeof item[key] === "object") {
      // console.log("item", item.id, item.type, item[key]);
      if(item.id >= 0 && item.type == "folder" && item[key].some(el => el.id == id)){
        console.log("found?");
        let found = item[key].findIndex(x => x.id == id);
        item[key].splice(found, 1);
      }
      else searchDelFolder(item[key], id);
    }
  })
}