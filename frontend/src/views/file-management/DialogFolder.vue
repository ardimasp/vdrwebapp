<template>
    <v-row justify="center">
        <v-dialog
            v-model="dialog"
            persistent
            max-width="500px"
        >
            <v-card>
                <v-card-title>
                    <span class="text-h5">New Folder</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-col cols="12">
                            <v-text-field
                            label="Folder Name"
                            v-model="folderName"
                            counter="20"
                            ></v-text-field>
                        </v-col>
                    </v-container>
                    <v-card-actions>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="closeDialog"
                        >
                            Close
                        </v-btn>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="save"
                            :disabled="!checkValid"
                        >
                            Save
                        </v-btn>
                    </v-card-actions>
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
import { computed, defineComponent, ref } from '@vue/composition-api'
import fileService from '../../services/file.service';
import store from './../../store/index'

export default defineComponent({
    props: {
        active: {type: String},
    },
    setup(props, {emit}) {
        const dialog = ref(true);
        const folderName = ref("");

        const checkValid = computed(() => {
            if(folderName.value.length == 0 || folderName.value.length > 20) return false;
            return true;
        })

        const closeDialog = () => {
            dialog.value = false;
            emit("closedialog");
        }

        const save = async () => {
            var submitData;
            if(!props.active || props.active.length == 0) submitData = {"paths": ["./" + folderName.value]};
            else submitData = {"paths": [props.active + "/" + folderName.value]};

            // call APi
            await fileService.addFolder(submitData);
            await store.dispatch("fetchTreeList");
            closeDialog();
        }

        return {dialog, folderName, checkValid, closeDialog, save}
    },
})
</script>
