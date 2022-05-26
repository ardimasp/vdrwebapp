<template>
    <div>
        <v-alert
            border="left"
            color="secondary"
            dark
            v-if="alertMsgShow"
        >
            Data is updated successfully!
        </v-alert>
        <v-form>
            <v-container>
                <v-text-field
                    v-model="username"
                    label="username"
                    required
                    :prepend-icon="mdiAccount"
                    readonly
                ></v-text-field>
                <v-text-field
                    v-model="password"
                    label="new password"
                    required
                    :prepend-icon="mdiKey"
                    :append-icon="showPass ? mdiEye: mdiEyeOff"
                    :type="showPass ? 'text':'password'"
                    @click:append="showPass = !showPass"
                ></v-text-field>
            </v-container>
            <div class="d-flex">
                <v-btn color="error" class="mr-3" @click="clearForm">
                    Cancel
                </v-btn>
                <v-btn color="secondary" @click="submitForm">
                    Submit
                </v-btn>
            </div>
        </v-form>
    </div>
</template>

<script>
import { computed, defineComponent, ref } from '@vue/composition-api'
import {mdiAccount, mdiKey, mdiEye, mdiEyeOff} from '@mdi/js'
import router from './../../router'
import store from '../../store';
import adminService from '../../services/admin.service';

export default defineComponent({
    setup() {
        const userid = router.app["_route"].params.userid;
        const detail = computed(() => {
            var users = store.state.admin.userList;
            return users.find(x => x.userid == userid);
        })

        const username = ref(userid);
        const password = ref("");
        const showPass = ref(false);

        const clearForm = () => {
            username.value = "";
            password.value = "";
            alertMsgShow.value = false;
            router.push('/admin');
        }
        
        const alertMsgShow = ref(false);
        const submitForm = async () => {
            var submitData = {
                "userid": username.value,
                "password": password.value,
            }

            let check = await adminService.editUser(submitData);
            if(check == 200) {
                alertMsgShow.value = true;
                password.value = "";
            }
        }

        return {
            username, password, mdiAccount, mdiKey, mdiEye, mdiEyeOff,
            showPass, clearForm, submitForm, userid, detail,
            alertMsgShow,
        }
    },
})
</script>
