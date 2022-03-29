<template>
    <v-dialog v-model="dialog" persistent max-width="500px">
        <v-card>
            <v-card-title>
                New document
            </v-card-title>
            <v-card-text>
                <v-file-input
                    v-model="selectedFile"
                    counter
                    label="New File"
                    multiple
                    @change="onFileSelected"
                    placeholder="Select your files"
                    :prepend-icon="iconPaperClip"
                    outlined
                    hint="Select file(s)"
                    persistent-hint
                >
                </v-file-input>
            </v-card-text>
            <v-card-actions>
                <v-btn color="primary" text @click="closeDialog" > Close </v-btn>
                <v-btn color="primary" text @click="save" :disabled="!checkFile"> Save </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { mdiPaperclip } from '@mdi/js';
import { ref, computed } from '@vue/composition-api';
import store from './../../store/index'

export default{
    props: {
        active: {type: Number, default: 0},
    },
    setup(props, {emit}){
        const iconPaperClip = mdiPaperclip;
        const dialog = ref(true);
        const selectedFile = ref([]);

        const checkFile = computed(() => {
            if(selectedFile.value.length) return true;
            return false;
        });

        const closeDialog = () => {
            dialog.value = false;
            emit("closedialog");
        }

        const files = ref([]);
        const id = store.state.tree.length;
        const onFileSelected = () => {
            files.value = [];
            var currentDate = new Date();
            let idx = id;
            for (let i in selectedFile.value) {
                files.value.push({
                    id: idx,
                    name: selectedFile.value[i].name,
                    file: selectedFile.value[i].type,
                    uploaddate: currentDate.toLocaleString(),
                    type: 'file',
                });
                idx++;
            }
        }

        const save = () => {
            store.dispatch('addFile', {
                active: props.active, 
                size: files.value.length,
                newFile: files.value,
            })
            files.value = [];
            closeDialog();
        }

        return {iconPaperClip, dialog, selectedFile, checkFile,
                closeDialog, onFileSelected, save}
    },
}
</script>