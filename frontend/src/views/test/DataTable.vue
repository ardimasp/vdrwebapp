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
      :items="fileFolderData"
      :search="search"
      show-select
      :single-select="singleSelect"
      item-key="name"
    >
      <template v-slot:top>
        <div v-if="selectedCount" class="text-right mr-3 mb-3">
          <v-btn
            color="primary"
            small
            class="mr-3"
          >Download ({{selected.length}})</v-btn>
          <v-btn
            color="primary"
            small
            @click="openDeleteConfirm('null')"
          >Delete ({{selected.length}})</v-btn>
        </div>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-spacer></v-spacer>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              small
              v-bind="attrs"
              v-on="on"
              class="mr-3"
            >
              {{ iconDownload }}
            </v-icon>
          </template>
          <span>Download {{item.name}}</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              small
              @click="openDeleteConfirm(item)"
              v-bind="attrs"
              v-on="on"
            >
              {{ iconDelete }}
            </v-icon>
          </template>
          <span>Delete {{item.name}}</span>
        </v-tooltip>
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
import {deleteFiles} from './folderfile'

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
    fileFolderData(){
      var files = this.filedata;
      files = files.filter((file)=>{
        return file.folder_id == store.state.folder.tab;
      })
      return files;
    },
  },
  methods: {
    deleteItem(item) {
      const index = store.state.files.list.indexOf(item)
      store.dispatch("removeFromFiles", index);
    },
    deleteAll(){
      deleteFiles(this.selected);
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
