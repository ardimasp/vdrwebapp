<template>
  <v-container fluid v-cloak @drop="addDropFile" @dragover.prevent @dragover="dragOver" @dragleave="dragLeave">
      <h2>Files</h2>
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
      <card-confirm
        v-if="uploadDialog"
        title="Upload File(s)"
        text="Do you want to upload the file(s)?"

        @confirmdialog="confirmUpload"
      ></card-confirm>
      <data-table></data-table>
  </v-container>
</template>

<script>
import { ref } from '@vue/composition-api'
import DataTable from './DataTable.vue'
import CardConfirm from '../cards/CardConfirm.vue'
import store from '../../store/index'

export default {
  name: 'FileManagement',
  components: { DataTable, CardConfirm },
  setup() {
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
        };
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
      console.log('emit confirm dialog upload', bool)
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

    return {
      files, uploadDialog,
      addDropFile, confirmUpload, openUploadConfirm,
      dragOver, dragLeave,
    }
  },
}
</script>

<style scoped>
.drag-file {
  background: rgba(77, 182, 172, .2);
}
</style>