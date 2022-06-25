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
                    placeholder="Select your files"
                    :prepend-icon="iconPaperClip"
                    outlined
                    hint="Select file(s)"
                    persistent-hint
                >
                </v-file-input>
                <v-select
                    :items="selectItems"
                    label="Category"
                    outlined
                    dense
                    v-model="categoryChoosen"
                ></v-select>
                <v-progress-linear
                    v-if="loading"
                    indeterminate
                    color="secondary"
                ></v-progress-linear>
                <p class="caption" v-if="!checkVTP">the file you are uploading contains .vtp file, we suggest that you upload it here!</p>
            </v-card-text>
            <!-- {{checkVTP}} -->
            <v-card-actions>
                <v-btn color="primary" text @click="closeDialog" :disabled="loading"> Close </v-btn>
                <v-btn color="primary" text @click="save" :disabled="!checkFile || !checkVTP"> Save </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { mdiPaperclip } from '@mdi/js';
import { ref, computed } from '@vue/composition-api';
import store from './../../store/index'
import fileService from '../../services/file.service';

export default{
    props: {
        active: {type: String},
    },
    setup(props, {emit}){
        const loading = ref(false);
        const iconPaperClip = mdiPaperclip;
        const dialog = ref(true);
        const selectedFile = ref([]);
        const selectItems = ["*","well-vtp","line-vtp","surface-vtp", "showcase", "production"];
        const categoryChoosen = ref("");

        const checkFile = computed(() => {
            if(selectedFile.value.length && !categoryChoosen.value == "" && !loading.value) return true;
            return false;
        });
        const checkVTP = computed(() => {
            for(let i = 0; i < selectedFile.value.length; i++) if( /\.(vtp)$/.test(selectedFile.value[i].name)) return false
            return true
        })

        const closeDialog = () => {
            dialog.value = false;
            emit("closedialog");
        }

        const save = async () => {
            loading.value = true;
            let submitData = new FormData();
            for(let i = 0; i < selectedFile.value.length; i++){
                submitData.append('files', selectedFile.value[i]);
            }
            // check if its root folder or not
            if(!props.active || props.active.length == 0) submitData.append('foldername', ".")
            else submitData.append('foldername', props.active);
            submitData.append('pointer', categoryChoosen.value);

            // call API
            await fileService.addFile(submitData);
            await store.dispatch("fetchTreeList");
            await store.dispatch("fetchVtpList")
            if(store.state.auth.permission == "Premium User") await store.dispatch("fetchSreeyaList");

            loading.value = false;
            closeDialog();
        }

        return {
            iconPaperClip, dialog, selectedFile, checkFile, selectItems, categoryChoosen,
            closeDialog, save, loading, checkVTP
        }
    },
}
</script>