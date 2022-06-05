<template>
    <v-stepper v-model="e1">
        <v-stepper-header>
            <v-stepper-step
                :complete="e1 > 1"
                step="1"
            >
                Select File
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step
                :complete="e1 > 2"
                step="2"
            >
                Choose Features
            </v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="3">
                Result
            </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
            <!-- search n select file -->
            <v-stepper-content step="1">
                <div>
                     <div class="d-flex flex-row-reverse">
                        <v-btn color="primary" @click="downloadTemplate">
                            <v-icon left>
                                {{mdiDownload}}
                            </v-icon> 
                            Download Template
                        </v-btn>
                    </div>
                    <p class="caption">
                        Please note that this feature only accept .xls or .xlsx file extension.
                        If you do not have the file in a specific template, please download the template and upload the file
                        to the file management.
                    </p>
                    <v-text-field
                    v-model="search"
                    label="Search File | Folder"
                    flat
                    hide-details
                    clearable
                    :clear-icon="mdiCloseCircleOutline"
                    ></v-text-field>
                    <v-treeview
                        :open="open" 
                        :search="search"
                        :items="items" 
                        item-key="id"
                        activatable
                        :active.sync="active"
                        color="secondary"
                        selected-color="secondary"
                        rounded
                    ></v-treeview>
                </div>

                <v-btn
                    color="primary"
                    @click="nextStep"
                    :disabled="!checkFirst"
                >
                    Continue
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="2">
                <div>
                    <label>Choose what you want to predict:</label>
                    <v-checkbox
                        v-model="selectFeatures"
                        color="secondary"
                        label="Oil"
                        value="oil"
                    ></v-checkbox>
                    <v-checkbox
                        v-model="selectFeatures"
                        color="secondary"
                        label="Gas"
                        value="gas"
                    ></v-checkbox>
                    <v-checkbox
                        v-model="selectFeatures"
                        color="secondary"
                        label="Both"
                        value="both"
                    ></v-checkbox>
                </div>

                <v-btn
                    color="primary"
                    @click="nextStep"
                    :disabled="!checkSecond"
                >
                    Continue
                </v-btn>

                <v-btn text @click="cancelStep">
                    Cancel
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="3">
                <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                >
                    3d surface plot T_T <a href="https://plotly.com/javascript/3d-surface-plots/" target="_blank">link here</a>
                </v-card>
                <p>options???</p>
                <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                >
                    Summary will be here ltr
                </v-card>

                <v-btn
                    color="primary"
                    @click="e1 = 1"
                >
                    New Prediction
                </v-btn>
            </v-stepper-content>
        </v-stepper-items>
  </v-stepper>
</template>

<script>
import { defineComponent, computed, ref, onMounted } from '@vue/composition-api'
import {mdiCloseCircleOutline, mdiDownload} from "@mdi/js"
import store from '../../store'
import router from '../../router'

export default defineComponent({
    setup() {
        onMounted(() => {
            if(store.state.auth.permission !== "Premium User") router.push('/not-authorized')
        })

        // to move the timelines
        const e1 = ref(1)

        // treeview select file by activeable
        const open = ["public"]
        const items = computed(() => {return store.state.tree.list;});
        const active = ref([]);
        const search = ref("");
        
        // checkbox select feature
        const selectFeatures = ref("")

        // moving between the steps
        const nextStep = () => { e1.value++ }
        const cancelStep = () => { e1.value-- }
        const checkFirst = computed(() => {
            if(active.value.length > 0 && checkFile(active.value[0])) return true
            return false;
        })
        const checkSecond = computed(() => {
            if(selectFeatures.value == "") return false;
            return true;
        })

        // check whether the file is correct or not
        const checkFile = (url) => {
            return /\.(jpg|jpeg|png|xls|xlsx|gif|svg)$/.test(url);
        }

        const downloadTemplate = () => {
            window.open('http://localhost:8000/src/views/sreeya/warning.svg', 'Download');
        }

        return {
            open, items, active, search, mdiDownload,
            mdiCloseCircleOutline, e1, selectFeatures,
            nextStep, cancelStep, checkFirst, checkSecond,
            downloadTemplate,
        }
    },
})
</script>
