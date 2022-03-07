<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      v-model="selected"
      :headers="headers"
      :items="filedata"
      :search="search"
      show-select
      :single-select="singleSelect"
      item-key="name"
    >
      <template v-slot:top>
        <div v-if="selectedCount" class="text-right mr-3 mb-3">
          <v-btn
            color="primary"
            x-small
            @click="openDeleteConfirm('null')"
          >Delete ({{selected.length}})</v-btn>
        </div>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-spacer></v-spacer>
        <v-icon
          small
          class="mr-3"
        >
          {{ iconDownload }}
        </v-icon>
        <v-icon
          small
          @click="openDeleteConfirm(item)"
        >
          {{ iconDelete }}
        </v-icon>
      </template>
    </v-data-table>
    <card-confirm
      v-if="deleteDialog"
      title="Delete File(s)"
      text="Do you want to delete this file(s)?"

      @confirmdialog="confirmDelete"
    ></card-confirm>
  </v-card>
</template>

<script>
import { mdiDelete, mdiDownload } from '@mdi/js'
import CardConfirm from '../cards/CardConfirm.vue'

import store from '../../store/index'

export default {
  components: {CardConfirm,},
  data() {
    return {
      search: '',
      selected: [], 
      singleSelect: false,
      headers: [
        {
          text: 'File Name',
          align: 'start',
          value: 'name',
        },
        { text: 'File Type', value: 'filetype' },
        { text: 'Uploaded at', value: 'uploadedat' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      iconDelete: mdiDelete,
      iconDownload: mdiDownload,
      filedata: store.state.files.list,

      deleteDialog: false,
      selectedDelItem: null,
    }
  },
  computed: {
    selectedCount(){
      if(this.selected.length) return true;
      return false;
    },
  },
  methods: {
    deleteItem(item) {
      const index = store.state.files.list.indexOf(item)
      store.dispatch("removeFromFiles", index);
    },
    deleteAll(){
      let arr = [], index;
      for (let i in this.selected){
        index = store.state.files.list.indexOf(this.selected[i]);
        arr.push(index);
      }
      arr.sort(function(a,b) {return b-a});

      for(let i in arr){
        store.dispatch("removeFromFiles", arr[i]);
      }
      // clean out
      this.selected = [];
    },
    confirmDelete(bool) {
      if(this.selected.length && bool){   //if the list is from selected
        this.deleteAll()
      }
      else if (bool) {                    //if its from the selecteddelitem
        this.deleteItem(this.selectedDelItem);
      }
      this.selectedDelItem = null;
      this.deleteDialog = false;
    },
    openDeleteConfirm(item){
      if(item != "null"){
        this.selectedDelItem = item;
      }
      this.deleteDialog = true;
    },

  },
}
</script>
