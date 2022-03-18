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
        <div>
          {{tree}}
        </div>
        <v-text-field
          v-model="search"
          label="Search File | Folder"
          flat
          hide-details
          clearable
          clear-icon="mdi-close-circle-outline"
        ></v-text-field>
        <!-- <v-subheader>
          file folder
        </v-subheader> -->
        <v-treeview 
            v-model="tree" 
            :open="open" 
            :search="search"
            :items="items" 
            item-key="id"
            selectable
            selection-type="independent"
            rounded
            hoverable
            activatable
            :active.sync="active"
            color="secondary_button"
            selected-color="secondary_button"
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
    </div>
</template>

<script>
import {mdiFolderPlus, mdiFilePlus, mdiFolderOpen, mdiFolder,
mdiLanguageHtml5, mdiNodejs, mdiCodeJson, mdiLanguageMarkdown, mdiFilePdf,
mdiFileImage, mdiFileDocumentOutline,mdiFileExcel} from '@mdi/js'
import { ref } from '@vue/composition-api'

import DialogFile from './DialogFile.vue'
import DialogFolder from './DialogFolder.vue'
import store from '../../store'

export default{
  components: {
      DialogFile,
      DialogFolder,
  },
  setup(){
    const iconFolderPlus = mdiFolderPlus;
    const iconFilePlus = mdiFilePlus;
    const iconFolderOpen = mdiFolderOpen;
    const iconFolder = mdiFolder;
    const active = ref([]);
    const fileTypes= {
                    html: mdiLanguageHtml5,
                    js: mdiNodejs,
                    json: mdiCodeJson,
                    md: mdiLanguageMarkdown,
                    "application/pdf": mdiFilePdf,
                    png: mdiFileImage,
                    txt: mdiFileDocumentOutline,
                    xls: mdiFileExcel,
                  };

    const open= ["public"];
    const tree = ref([]);
    const items = store.state.tree.list;
    const search = ref("");

    const fileDialog = ref(false);
    const openFileDialog = () => {
      fileDialog.value = true;
      console.log("open", fileDialog.value)
    }
    const closeFileDialog = () => {
      fileDialog.value = false;
      console.log("close", fileDialog.value)
    }

    const folderDialog = ref(false);
    const openFolderDialog = () => {
      folderDialog.value = true;
    }
    const closeFolderDialog = () => {
      folderDialog.value = false;
    }

    return {
      iconFolderPlus, open, tree, items, search,
      active, iconFilePlus,
      iconFolderOpen, iconFolder, fileTypes, fileDialog, openFileDialog,
      openFolderDialog, folderDialog, closeFolderDialog, closeFileDialog
    }
  },
}
</script>