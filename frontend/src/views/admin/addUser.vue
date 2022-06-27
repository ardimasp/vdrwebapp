<template>
    <div>
        <v-snackbar
            :color="alertColour"
            v-model="alertMsgShow"
            rounded="pill"
            timeout=3000
            right
        >
            {{alertMsg}}
        </v-snackbar>
        <v-breadcrumbs
            :items="breadcrumb"
        ></v-breadcrumbs>
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
                <v-autocomplete
                    v-model="type"
                    label="User Type"
                    required
                    :prepend-icon="mdiCardAccountDetails"
                    :items="userTypes"
                ></v-autocomplete>
                <v-text-field
                    v-model="name"
                    label="Name"
                    required
                    :prepend-icon="mdiAccountOutline"
                ></v-text-field>
                <v-text-field
                    v-model="affiliation"
                    label="Affiliation"
                    required
                    :prepend-icon="mdiDomain"
                ></v-text-field>
                <div class="d-flex">
                    <v-btn color="error" outlined class="mr-3" @click="clearForm">
                        Cancel
                    </v-btn>
                    <v-btn color="primary" @click="submitForm" :disabled="!checkForm">
                        Submit
                    </v-btn>
                </div>
            </v-container>
        </v-form>
    </div>
</template>

<script>
import { computed, defineComponent, ref } from '@vue/composition-api'
import {mdiAccount, mdiKey, mdiEye, mdiEyeOff, mdiAccountOutline, 
        mdiCalendarRange, mdiDomain, mdiCardAccountDetails} from '@mdi/js'
import store from '../../store';
import adminService from '../../services/admin.service';
import {profile} from './profile'

export default defineComponent({
    setup() {
        const username = ref("");
        const password = ref("");
        const showPass = ref(false);
        const userTypes = ["Premium User", "Regular User"];
        const type = ref("Regular User");
        const name = ref("");
        const affiliation = ref("");

        const menu = ref(false);
        const breadcrumb = [
            {
                text: '< Back',
                href: '/admin',
                disable: false,
            }
        ]

        const clearForm = () => {
            username.value = "";
            password.value = "";
            name.value = "";
            affiliation.value = ""
        }

        const checkForm = computed(() => {
            if(username.value == "" || password.value == "" || name.value == "" || affiliation.value == ""){
                return false
            }
            return true;
        })

        const alertMsgShow = ref(false);
        const alertMsg = ref("");
        const alertColour = ref("")
        const submitForm = async () => {
            var submitData = {
                "userid": username.value,
                "password": password.value,
                "type": type.value,
                "name": name.value,
                "affiliation": affiliation.value,
                "profile_pict": profile
            }

            let status = await adminService.addUser(submitData);
            if (status == 200) {
                console.log(submitData);
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
            showPass, clearForm, submitForm, alertMsg, alertMsgShow, alertColour,
            checkForm, userTypes, type, name, affiliation,
            menu, mdiAccountOutline, mdiCalendarRange, mdiDomain,
            mdiCardAccountDetails, breadcrumb
        }
    },
})
</script>
