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
                    <v-text-field
                    v-model="search"
                    label="Search File | Folder"
                    flat
                    hide-details
                    clearable
                    :clear-icon="mdiclosecircleoutline"
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
                    @click="e1 = 2"
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
                    @click="e1 = 3"
                >
                    Continue
                </v-btn>

                <v-btn text @click="e1 = 1">
                    Cancel
                </v-btn>
            </v-stepper-content>

            <v-stepper-content step="3">
                <v-card
                    class="mb-12"
                    color="grey lighten-1"
                    height="200px"
                ></v-card>

                <v-btn
                    color="primary"
                    @click="e1 = 1"
                >
                    Continue
                </v-btn>
                <v-btn text @click="e1 = 2">
                    Cancel
                </v-btn>
            </v-stepper-content>
        </v-stepper-items>
  </v-stepper>
</template>

<script>
import { defineComponent, computed, ref } from '@vue/composition-api'
import {mdiCloseCircleOutline} from "@mdi/js"
import store from '../../store'

export default defineComponent({
    setup() {
        // to move the timelines
        const e1 = ref(1)

        // treeview select file by activeable
        const open = ["public"]
        const items = computed(() => {return store.state.tree.list;});
        const active = ref([]);
        const search = ref("");
        
        // checkbox select feature
        const selectFeatures = ref("")

        return {
            open, items, active, search,
            mdiCloseCircleOutline, e1, selectFeatures
        }
    },
})
</script>
