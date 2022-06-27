<template>
  <div>
    <div class="text-right mt-3 mr-3" v-if="checkSelect">
      <!-- <p>{{selected}}</p> -->
      <v-btn
        small
        color="secondary"
        @click="openAddFileDialog">
        add
      </v-btn>
    </div>
    <div class="pl-3 pr-3">
      <v-text-field
        v-model="search"
        label="Search File"
        flat
        hide-details
        clearable
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
    </div>
    <v-treeview
      selectable
      selection-type="independent"
      v-model="selected"
      item-key="id"
      :items="items"
      :search="search"
      color="secondary"
      selected-color="secondary"
      dense
    ></v-treeview>
    <card-confirm
      v-if="addFileDialog"
      @confirmdialog="addFile"

      title="Add File"
      text="Do you want to add this file(s) to viewer?"
    ></card-confirm>
  </div>
</template>

<script>
import { ref, computed } from '@vue/composition-api';
import store from '../../store'
import CardConfirm from '../cards/CardConfirm.vue'

export default {
  components: {
    CardConfirm,
  },
  setup() {
    const items = computed(() => {return store.state.tree.list;})
    const selected = ref([]);
    const search = ref("");

    const addFileDialog = ref(false);
    const addFile = (bool) => {
      if(bool) addToList();
      addFileDialog.value = false;
    };
    const openAddFileDialog = () => {addFileDialog.value = true}
    
    const checkSelect = computed(() => {
      if (selected.value.length) return true;
      // console.log(selected.value)
      return false;
    });

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

    return {items, selected, search, checkSelect, 
            addFileDialog, addFile, openAddFileDialog}
  }
}

//treecontent2 vtkviewer 
</script>