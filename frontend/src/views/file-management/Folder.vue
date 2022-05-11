<template>
    <div>
      <div class="d-flex flex-row-reverse">
        <div>
          <v-btn class="mr-3" color="primary" @click="openFileDialog">
            <v-icon left>
              {{iconFilePlus}}
            </v-icon> 
            Add file
          </v-btn>
          <v-btn color="primary" @click="openFolderDialog">
            <v-icon left>
              {{iconFolderPlus}}
            </v-icon> 
            Add folder
          </v-btn>
        </div>
      </div>
      <div v-if="checkSelect">
        <v-btn
          color="secondary"
          small
          class="mr-3"
        >Download</v-btn>
        <v-btn
          color="secondary"
          small
          @click="openDelFileDialog"
        >Delete</v-btn>
        <div class="caption">Selecting file(s)</div>
      </div>
        <v-text-field
          v-model="search"
          label="Search File | Folder"
          flat
          hide-details
          clearable
          clear-icon="mdi-close-circle-outline"
        ></v-text-field>
        <v-treeview 
            v-model="tree" 
            :open="open" 
            :search="search"
            :items="items" 
            item-key="id"
            selectable
            selection-type="leaf"
            rounded
            hoverable
            activatable
            :active.sync="active"
            color="secondary"
            selected-color="secondary"
        >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="!item.file">
                {{ open ? iconFolderOpen : iconFolder }}          
              </v-icon>
              <v-icon v-else>
                {{ fileTypes[item.file] }}
              </v-icon>
            </template>
            <template slot="append" slot-scope="props">
                <div>
                  <span class="mr-6">
                    {{props.item.file}}
                  </span>
                  <span>
                    {{props.item.uploaddate}}
                  </span>
                  <span v-if="props.item.type == 'folder'">
                    <v-icon small @click.prevent="saveSelectedFolder(props.item.id)">
                      {{iconDelete}}
                    </v-icon>
                  </span>
                </div>
            </template>
        </v-treeview>
        <dialog-folder
          v-if="folderDialog"
          :active="active[0]"
          @closedialog="closeFolderDialog"
        ></dialog-folder>
        <dialog-file
          v-if="fileDialog"
          :active="active[0]"
          @closedialog="closeFileDialog"
        ></dialog-file>
        <card-confirm
          v-if="delFileDialog"
          title="Delete File(s)"
          text="Do you want to delete this file(s)?"

          @confirmdialog="deleteFile"
        ></card-confirm>
        <card-confirm
          v-if="delFolderDialog"
          title="Delete Folder"
          text="Do you want to delete this folder?"

          @confirmdialog="deleteFolder"
        ></card-confirm>
    </div>
</template>

<script>
import {mdiFolderPlus, mdiFilePlus, mdiFolderOpen, mdiFolder,
mdiLanguageHtml5, mdiNodejs, mdiCodeJson, mdiLanguageMarkdown, mdiFilePdf,
mdiFileImage, mdiFileDocumentOutline,mdiFileExcel, mdiDelete} from '@mdi/js'
import { computed, ref } from '@vue/composition-api'

import DialogFile from './DialogFile.vue'
import DialogFolder from './DialogFolder.vue'
import CardConfirm from './../cards/CardConfirm.vue'
import store from '../../store'

export default{
  components: {
      DialogFile,
      DialogFolder,
      CardConfirm,
  },
  setup(){
    const iconFolderPlus = mdiFolderPlus;
    const iconFilePlus = mdiFilePlus;
    const iconFolderOpen = mdiFolderOpen;
    const iconFolder = mdiFolder;
    const iconDelete = mdiDelete;
    const active = ref([]);
    const fileTypes= {
                    html: mdiLanguageHtml5,
                    js: mdiNodejs,
                    json: mdiCodeJson,
                    md: mdiLanguageMarkdown,
                    "application/pdf": mdiFilePdf,
                    "image/png": mdiFileImage,
                    txt: mdiFileDocumentOutline,
                    xls: mdiFileExcel,
                  };

    const open= ["public"];
    const tree = ref([]); //selected
    const items = store.state.tree.list;
    const search = ref("");

    // computed
    const checkSelect = computed(() => {
      if (tree.value.length) return true;
      return false;
    });

    // add file(s)
    const fileDialog = ref(false);
    const openFileDialog = () => { fileDialog.value = true; }
    const closeFileDialog = () => {fileDialog.value = false; }

    // add folder
    const folderDialog = ref(false);
    const openFolderDialog = () => {folderDialog.value = true; }
    const closeFolderDialog = () => {folderDialog.value = false;}

    // delete file(s)
    const delFileDialog = ref(false);
    const deleteFile = (bool) => {
      if(bool) store.dispatch('deleteFile', tree.value);
      delFileDialog.value = false;
    }
    const openDelFileDialog = () => {delFileDialog.value = true}

    // delete folder
    const selectedFolder = ref(0);
    const delFolderDialog = ref(false);
    const deleteFolder = (bool) => {
      if(bool) store.dispatch('deleteFolder', selectedFolder.value);
      delFolderDialog.value = false;
    }
    const saveSelectedFolder = (id) => {
      selectedFolder.value = id
      delFolderDialog.value = true;
    }

    return {
      iconFolderPlus, open, tree, items, search, iconDelete,
      active, iconFilePlus, checkSelect, deleteFile, deleteFolder,
      iconFolderOpen, iconFolder, fileTypes, fileDialog, openFileDialog,
      openFolderDialog, folderDialog, closeFolderDialog, closeFileDialog,
      delFileDialog, delFolderDialog, openDelFileDialog, saveSelectedFolder
    }
  },
}
</script>