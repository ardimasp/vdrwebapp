<template>
  <v-container fluid v-cloak @drop="addDropFile" @dragover.prevent @dragover="dragOver" @dragleave="dragLeave">
      <div class="d-flex justify-space-between">
        <h2>{{folderName}}</h2>
        <v-btn
          v-if="tab_id != 1"
          outlined
          color="error"
          @click="openDeleteConfirm"
        >Delete</v-btn>
      </div>
      <span class="subtitle-2 text-no-wrap">Drag and drop to upload file</span>
      <div class="upload-file-resize d-flex justify-end">
        <v-file-input
          label="Upload File"
          outlined
          multiple
          filled
          densed
          v-model="files"
          @change="openUploadConfirm"
        ></v-file-input>
      </div>
      <data-table></data-table>
      <card-confirm
        v-if="uploadDialog"
        title="Upload File(s)"
        text="Do you want to upload the file(s)?"

        @confirmdialog="confirmUpload"
      ></card-confirm>
      <card-confirm
        v-if="removeDialog"
        title="Delete File(s)"
        text="Do you want to delete this folder including the file(s)?"

        @confirmdialog="confirmDelete"
    ></card-confirm>
  </v-container>
</template>

<script>
import { ref } from '@vue/composition-api'
import DataTable from './DataTable.vue'
import CardConfirm from '../cards/CardConfirm.vue'
import store from '../../store/index'
import {deleteFiles} from './folderfile'

export default {
  name: 'FileManagement',
  components: { DataTable, CardConfirm },
  setup(props, {emit}) {
    //function for drag and drop file
    const files = ref([])
    const addDropFile = (e) => {
      e.preventDefault();
      files.value = Array.from(e.dataTransfer.files)
      // clear out
      e.currentTarget.classList.remove('drag-file');
      openUploadConfirm()
    }

    //function at upload on change
    const uploadDialog = ref(false)
    const openUploadConfirm = () => {
      uploadDialog.value = true
      console.log(uploadDialog.value)
    }

    const uploadFile = () => {
      var currentDate = new Date();
      let new_data;
      for (let i in files.value) {
        console.log(files.value[i])
        new_data = {
          name: files.value[i].name,
          filetype: files.value[i].type,
          uploadedat: currentDate.toLocaleString(),
          folder_id: store.state.folder.tab,
        };
        console.log(new_data)
        store.dispatch('addToFiles', new_data);
      }
      files.value = []
    }
    
    const confirmUpload = (bool) => {
      if (bool) uploadFile();
      else {
        files.value = []
      }

      uploadDialog.value = false;
      // console.log('emit confirm dialog upload', bool)
    }

    // add remove colour at drag
    const dragOver = (e) => {
      e.preventDefault();
      if (!e.currentTarget.classList.contains('drag-file')) {
            e.currentTarget.classList.add('drag-file');
        }
    }
    const dragLeave = (e) => {
      e.currentTarget.classList.remove('drag-file');
    }

    const tab_id = store.state.folder.tab;
    const folderName = store.state.folder.list.find(x => x.id === store.state.folder.tab).name;

    const removeDialog = ref(false);
    const openDeleteConfirm = () => {
      removeDialog.value = true;
    }
    const confirmDelete = (bool) => {
      if(bool){
        removeDialog.value = false;
        // delete the files first
        var files = store.state.files.list;
        files = files.filter((file)=>{
          return file.folder_id == store.state.folder.tab;
        })
        deleteFiles(files);

        // delete the folder
        const index = store.state.folder.list.findIndex(x => x.id === store.state.folder.tab);
        store.dispatch("removeFromFolders", index);

        store.dispatch("updateTab", 1)
        emit("updateactivetab", 0);
      }
    }

    return {
      files, uploadDialog, folderName, tab_id, removeDialog,
      addDropFile, confirmUpload, openUploadConfirm,
      dragOver, dragLeave, openDeleteConfirm, confirmDelete
    }
  },
}
</script>

<style scoped>
.drag-file {
  background: rgba(77, 182, 172, .2);
}
</style>