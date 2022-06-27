<template>
    <div class="text-center">
        <v-dialog
            v-model="dialog"
            max-width="300"
        >
            <v-card>
                <v-card-title class="text-h5 grey lighten-2 mb-3" style="background-color: #4DB6AC">
                    {{title}}
                </v-card-title>

                <v-card-text>
                    <p v-html="text"></p>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="secondary"
                        text
                        @click="closeDialog"
                    >
                        Close
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
import { defineComponent, ref } from '@vue/composition-api'

export default defineComponent({
    props: {
        title: {type: String},
        text: {type: String}
    },
    setup(props,{emit}) {
        const dialog = ref(true);
        const closeDialog = () => {
            dialog.value = false;
            emit("closedialog")
        }

        return {
            dialog, closeDialog
        }
    },
})
</script>
