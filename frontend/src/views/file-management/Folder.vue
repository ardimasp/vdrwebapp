<template>
    <div>
      <!-- {{load}}
      <folder-skeleton v-if="load"></folder-skeleton> -->
      <div>
        <div class="d-flex flex-row-reverse">
          <div>
            <v-icon @click="toggleInfo" class="mr-3">
              {{mdiInformationOutline}}
            </v-icon>
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
            @click="downloadFiles"
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
          :clear-icon="mdiCloseCircleOutline"
        ></v-text-field>
        <v-progress-linear
          v-if="load"
          color="secondary"
          indeterminate
        ></v-progress-linear>
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
              <v-icon v-if="!item.filetype">
                {{ open ? iconFolderOpen : iconFolder }}          
              </v-icon>
              <v-icon v-else>
                {{ fileTypes[item.filetype] }}
              </v-icon>
            </template>
            <template slot="append" slot-scope="props">
                <div>
                  <!-- <span class="mr-6">
                    {{props.item.filetype}}
                  </span> -->
                  <span class="mr-6">
                    {{props.item.uploaddate}}
                  </span>
                  <span v-if="props.item.type == 'folder'">
                    <v-icon small @click.prevent="saveSelectedFolder(props.item.id)">
                      {{iconDelete}}
                    </v-icon>
                  </span>
                  <span v-else>
                    <v-icon small @click.prevent="downloadFile(props.item.id)">
                      {{iconDownload}}
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

        <!-- dialogues -->
        <card-dialog
          v-if="information"
          title="Guide"
          :text="text"
        ></card-dialog>
      </div>
    </div>
</template>

<script>
import {mdiFolderPlus, mdiFilePlus, mdiFolderOpen, mdiFolder,
      mdiLanguageHtml5, mdiNodejs, mdiCodeJson, mdiLanguageMarkdown, mdiFilePdf,
      mdiFileImage, mdiFileDocumentOutline,mdiFileExcel, mdiDelete, mdiDownload,
      mdiCloseCircleOutline, mdiInformationOutline} from '@mdi/js'
import { computed, ref } from '@vue/composition-api'

import DialogFile from './DialogFile.vue'
import DialogFolder from './DialogFolder.vue'
import CardConfirm from './../cards/CardConfirm.vue'
import CardDialog from './../cards/CardDialog.vue'
import store from '../../store'
import fileService from './../../services/file.service'

export default{
  components: {
      DialogFile,
      DialogFolder,
      CardConfirm,
      CardDialog,
  },
  setup(){
    // const items = store.state.tree.list;
    const load = computed(() => {return store.state.initialLoad})
    // const load = ref(store.state.initialLoad);
    const items = computed(() => {return store.state.tree.list;})

    const iconFolderPlus = mdiFolderPlus;
    const iconFilePlus = mdiFilePlus;
    const iconFolderOpen = mdiFolderOpen;
    const iconFolder = mdiFolder;
    const iconDownload = mdiDownload;
    const iconDelete = mdiDelete;
    const active = ref([]);
    const fileTypes= {
                    html: mdiLanguageHtml5,
                    js: mdiNodejs,
                    json: mdiCodeJson,
                    md: mdiLanguageMarkdown,
                    "application/pdf": mdiFilePdf,
                    "image/png": mdiFileImage,
                    "image/jpeg": mdiFileImage,
                    txt: mdiFileDocumentOutline,
                    xls: mdiFileExcel,
                  };

    const open= ["public"];
    const tree = ref([]); //selected
    const search = ref("");

    // information
    const information = ref(false);
    const text = `
          <ul>
            <b>Adding new file or folder:</b>
            <li>To add new file(s) or folder into the root folder, don't press on any text and activate them</li>
            <li>Respectively, press and activate on the text in which it is a folder to add new file or folder into existing folder</li>
            <li>There are categories when adding new file(s):</li>
            <ul>
              <li>Choose '*' for general use</li>
              <li>Choose 'Chart' to use on Viewer's page</li>
              <li>Choose 'Showchase' to use on Map's and Showcase's page</li> 
              <li>Choose 'Sreeya' to use on Production's page (for Premium user)</li>
            </ul>
          </ul>
          <br>
          <ul>
            <b>Deleting file or folder:</b>
            <li>To delete file(s), select the checkbox(es) and press delete</li>
            <li>Whilst deleting a folder, the file(s) inside the folder would be deleted</li>
          </ul>
          <br>
          <ul>
            <b>Downloading file or folder:</b>
            <li>To download a file, press the download button on the right side of the file name</li>
            <li>To download multiple files, select the chechboxes and press download</li>
          </ul>`;
    const toggleInfo = () => {
      information.value = !information.value
    }

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
    const deleteFile = async (bool) => {
      if(bool) {
        if(store.state.auth.permission == "Premium User" && tree.value.includes("/template.xlsx")){
          let idx = tree.value.indexOf("/template.xlsx")
          tree.value.splice(idx, 1)
          console.log("template exist")
        }
        await fileService.deleteFile(tree.value);
        await store.dispatch("fetchTreeList");
      }
      delFileDialog.value = false;
    }
    const openDelFileDialog = () => {delFileDialog.value = true}

    // delete folder
    const selectedFolder = ref(0);
    const delFolderDialog = ref(false);
    const deleteFolder = async (bool) => {
      if(bool) {
        await fileService.deleteFolder(selectedFolder.value);
        await store.dispatch("fetchTreeList");
      }
      delFolderDialog.value = false;
    }
    const saveSelectedFolder = (id) => {
      selectedFolder.value = id
      delFolderDialog.value = true;
    }

    // download file
    const downloadFile = async (path) => {
      await fileService.downloadFile(path);
    }

    const downloadFiles = async () => {
      var submitData = {
        "paths": tree.value
      }
      await fileService.downloadFiles(submitData);
    }

    return {
      iconFolderPlus, open, tree, items, search, iconDelete,
      active, iconFilePlus, checkSelect, deleteFile, deleteFolder,
      iconFolderOpen, iconFolder, fileTypes, fileDialog, openFileDialog,
      openFolderDialog, folderDialog, closeFolderDialog, closeFileDialog,
      delFileDialog, delFolderDialog, openDelFileDialog, saveSelectedFolder,
      iconDownload, downloadFile, downloadFiles, mdiCloseCircleOutline, information,
      mdiInformationOutline, toggleInfo, text, load
    }
  },
}
</script>