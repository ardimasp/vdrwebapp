<template>
    <div class="text-center">
        <v-dialog
        v-model="dialog"
        width="500"
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
                        @click="dialog = false"
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
    setup() {
        const dialog = ref(true);

        return {
            dialog,
        }
    },
})
</script>
