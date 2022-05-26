<template>
    <div>
        <v-alert
            border="left"
            :color="alertColour"
            dark
            v-if="alertMsgShow"
        >
            {{alertMsg}}
        </v-alert>
        <v-form style="color:white">
            <v-container>
                <v-text-field
                    v-model="username"
                    label="username"
                    required
                    :prepend-icon="mdiAccount"
                ></v-text-field>
                <v-text-field
                    v-model="password"
                    label="password"
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
import { defineComponent, ref } from '@vue/composition-api'
import {mdiAccount, mdiKey, mdiEye, mdiEyeOff} from '@mdi/js'
import store from '../../store';
import adminService from '../../services/admin.service';

export default defineComponent({
    setup() {
        const username = ref("");
        const password = ref("");
        const showPass = ref(false);

        const clearForm = () => {
            username.value = "";
            password.value = "";
        }

        const alertMsgShow = ref(false);
        const alertMsg = ref("");
        const alertColour = ref("")
        const submitForm = async () => {
            var submitData = {
                "userid": username.value,
                "password": password.value
            }

            let status = await adminService.addUser(submitData);
            if (status == 200) {
                await store.dispatch("fetchUserList");
                alertMsgShow.value = true;
                alertColour.value = "#4DB6AC";
                alertMsg.value = "User successfully added!"
                clearForm();
            }
            else if (status == 409) {
                alertMsgShow.value = true;
                alertColour.value = "#FFB400";
                alertMsg.value = "A User with this Username already Exist!"
            }

        }

        // const colorSecondary = "#4DB6AC";

        return {
            username, password, mdiAccount, mdiKey, mdiEye, mdiEyeOff,
            showPass, clearForm, submitForm, alertMsg, alertMsgShow, alertColour
        }
    },
})
</script>
