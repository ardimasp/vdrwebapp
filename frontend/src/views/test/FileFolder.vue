<template>
  <v-card>
    <!-- <v-toolbar
      flat
      color="primary"
      dark
    >
      <v-toolbar-title>User Profile</v-toolbar-title>
    </v-toolbar> -->
    <v-toolbar
        flat
        color="primary"
        dark
    ></v-toolbar>
    <v-tabs vertical v-model="activeTab">
      <v-tab v-for="folder in folders" :key="folder.name+folder.id" class="justify-start" @change="changeTab(folder.id)">
          <v-icon
            small
            left
          >
            {{ iconFolder }}
          </v-icon>
          {{ folder.name }} {{folder.id -1}}
      </v-tab>
      <v-tab>
          <v-icon
            small
            left
            color="secondary_button"
          >
            {{ iconPlus }}
          </v-icon> 
          <span class="color:secondary_button;">Add Folder</span>
      </v-tab>

      <v-tab-item v-for="i in folders" :key="i.name+i.id">
          <file-management
            @updateactivetab="updateActiveTab"
          ></file-management>
      </v-tab-item>
      <!-- add new folder tab -->
      <v-tab-item>
        <v-row class="d-flex justify-center">
          <v-col
          cols="12"
          md="6">
            <v-card class="pa-6 ma-10" elevation="0">
              Folder Name:
              <v-text-field
                v-model="folderName"
                :counter="10"
                label="Name"
                required
              ></v-text-field>
              <div align="center">
                <v-btn color="primary" small class="ma-4" @click="addFolder" :disabled="!checkValid">
                  <v-icon left>
                    {{ iconFolderPlus }}
                  </v-icon>
                  Add Folder
                </v-btn>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>

<script>
import { computed, defineComponent, ref, } from '@vue/composition-api'
import store from '../../store/index'
import { mdiFolder, mdiPlus, mdiFolderPlus } from '@mdi/js'

// import DataTable from './DataTable.vue'
import FileManagement from './FileManagement.vue'

export default defineComponent({
    components: {
        // DataTable,
        FileManagement
    },
    setup() {
        const folders = store.state.folder.list;
        const iconFolder = mdiFolder;
        const iconPlus = mdiPlus;
        const iconFolderPlus = mdiFolderPlus;
        const folderName = ref('');
        const activeTab = ref(0);


        const changeTab = (tab_id) => {
          store.dispatch("updateTab", tab_id);
        }

        const checkValid = computed(() => {
          if(folderName.value.length > 10 || folderName.value.length == 0) return false
          return true;
        })

        const addFolder = () => {
          const new_folder = {
            id: folders.length+1,
            name: folderName.value.toUpperCase()
          };
          store.dispatch("addToFolders", new_folder);
          folderName.value = '';

          store.dispatch("updateTab", new_folder.id);
          activeTab.value = folders.length;
        }

        const updateActiveTab = (value) => {
          activeTab.value = value;
        }

        return {folders, iconFolder, iconPlus, iconFolderPlus, folderName, activeTab,
                changeTab, addFolder, checkValid, updateActiveTab}
    },
})
</script>
