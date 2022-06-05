<template>
    <!-- <v-card
        class="mb-12"
        color="grey lighten-1"
        flat
    > -->
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
    <!-- </v-card> -->
</template>

<script>
import { defineComponent, computed, ref } from '@vue/composition-api'
import {mdiCloseCircleOutline} from "@mdi/js"
import store from '../../store'

export default defineComponent({
    setup() {
        const open = ["public"]
        const items = computed(() => {return store.state.tree.list;});
        const active = ref([]);
        const search = ref("");

        return {
            open, items, active, search,
            mdiCloseCircleOutline,
        }
    },
})
</script>
