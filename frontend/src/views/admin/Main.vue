<template>
    <div>
        <div class="d-flex flex-row-reverse">
            <div>
                <v-btn color="primary" class="mb-3" link :to="{name:'admin_adduser'}">
                    <!-- <v-icon left>
                    {{iconFolderPlus}}
                    </v-icon>  -->
                    Add Client
                </v-btn>
            </div>
        </div>
        <v-data-table
            :headers="headers"
            :items="list"
            item-key="userid"
            :items-per-page="10"
            class="elevation-1"
        >
            <template v-slot:item.actions="{ item }">
                <v-icon
                    small
                    @click.prevent="editUser(item)"
                    class="mr-3"
                >
                    {{mdiPencil}}
                </v-icon>
                <v-icon
                    small
                    @click.prevent="deleteUserOpenDialog(item)"
                >
                    {{mdiDelete}}
                </v-icon>
            </template>
        </v-data-table>
        <card-confirm
            v-if="delUserDialog"
            title="Delete User"
            text="Do you want to delete this user?"

            @confirmdialog="deleteUser"
        ></card-confirm>
    </div>
</template>

<script>
import { defineComponent, computed, ref } from '@vue/composition-api'
import router from '../../router';
import store from '../../store';
import {mdiAccount, mdiKey, mdiEye, mdiEyeOff, mdiDelete, mdiPencil} from '@mdi/js'
import adminService from '../../services/admin.service';
import CardConfirm from './../cards/CardConfirm.vue'

export default defineComponent({
    components: {
        CardConfirm
    },
    async mounted() {
        if(store.state.admin.userList.length == 0) {
            await store.dispatch("fetchUserList")
        }
    },
    setup() {
        const headers= [
          { text: 'User ID', value: 'userid' },
          { text: 'Actions', value: 'actions', sortable: false },
        ];
        const list = computed(() => {return store.state.admin.userList});

        const editUser = (item) => {
            router.push({
                name: 'admin_edituser',
                params: {
                    userid: item.userid
                },
            });
        }

        const choosenItem = ref();
        const delUserDialog = ref(false);
        const deleteUserOpenDialog = (item) => {
            choosenItem.value = item;
            delUserDialog.value = true;
        }

        const deleteUser = async (bool) => {
            if(bool){
                await adminService.deleteUser(choosenItem.value.userid);
                await store.dispatch("fetchUserList")
            }
            delUserDialog.value = false;
        }

        return {
            headers, list, editUser, mdiAccount, mdiKey, mdiEye, mdiEyeOff,
            mdiDelete, deleteUser, mdiPencil, deleteUserOpenDialog, delUserDialog
        }
    },
})
</script>
