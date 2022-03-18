export const searchFolder = (item, name, active, length) => {
    Object.keys(item).forEach(key => {
        // check every key (id, name, type) if its an object
        if(typeof item[key] === "object") {
          // console.log("is an object", item[key]);
          // check the item.id directly n if its a folder
          if (item.id == active && item.type == "folder"){
            item.children.push({
              id: length+1,
              type: 'folder',
              name: name,
              children: []
            });
            return false;
          }
          // if no match found and there is an object
          else searchFolder(item[key], name, active, length);
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