<template>
  <div>
    <div class="pl-3 pr-3">
      <v-text-field
        v-model="search"
        label="Search File"
        flat
        hide-details
        clearable
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
      <!-- for progress bar -->
      <slot></slot>
    </div>
    <v-treeview
      :selectable="!selectable"
      selection-type="independent"
      v-model="selected"
      item-key="id"
      :items="items"
      :search="search"
      color="secondary"
      selected-color="secondary"
      dense
    ></v-treeview>
  </div>
</template>

<script>
import { ref, computed, watch } from '@vue/composition-api';
import store from '../../store'

export default {
  props: {
    selectable: {type: Boolean}
  },
  setup(props, {emit}) {
    const items = computed(() => {return store.state.tree.vtp;})
    const selected = ref([]);
    const search = ref("");

    watch(selected, (newSelected, prevSelected) => {
      // do the validation here ltr
      // just deliver the newly selected

      // check if prevselected hv more (sth is unselected)
      if(prevSelected.length > newSelected.length){
        for (let i = 0; i < prevSelected.length; i++){
          if(!newSelected.includes(prevSelected[i])) {
            if(checkFileChoosen(prevSelected[i])) emit("removedata", newSelected, i)
          }
        }
      }

      let newSelect;
      if(newSelected.length > prevSelected.length){
        newSelect = newSelected.slice(-1)
        if(checkFileChoosen(newSelect)) emit("changeselected", newSelected)
      }
    })

    const checkFileChoosen = (url) => {
      return /\.(vtp)$/.test(url);
    }

    const addToList = () => {
      checkFile();
      selected.value = []
    };

    let searchCounter = 0;
    const checkFile = () => {
      // check if the file is a folder or not
      // insert file detail into the list
      const list = store.state.tree.list;
      const data = selected.value;
      let item;
      for(let i = 0; i<list.length; i++){
        item = list[i];
        if(data.includes(item.id)){
          searchCounter++;
        }
        else searchFile(item, data);

        if(searchCounter == data.length) break;
        continue;
      }

      searchCounter = 0;
    };

    let list_size = store.state.viewer.list.length;
    let new_item;
    const searchFile = (item, arr) => {
      if(item.type == "folder") {
        for(let i = 0; i < item.children.length; i++){
            if (arr.includes(item.children[i].id)){
                if (item.children[i].type == "file") {
                  // add the x n y data here or in the store
                  new_item = {
                    id: list_size++,
                    file_id: item.children[i].id,
                    name: item.children[i].name,
                    x_dimension: 0,
                    y_dimension: 0,
                    width: 300,
                    height: 300
                  };
                  store.dispatch('addToViewerList', new_item)
                  searchCounter++;
                }
            }
            if(searchCounter == arr.length) break;
            continue;
        }
        if (arr.includes(item.id)) searchCounter++;
        if (item.children.length) searchFile(item.children, arr);
      }
      else if (item.length){
        for(let i = 0; i < item.length; i++){
            searchFile(item[i], arr)
    
            if(searchCounter == arr.length) break;
            continue;
        }
      }
    }

    return {
      items, selected, search, addToList, checkFileChoosen
    }
  }
}
</script>