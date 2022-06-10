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
                <v-menu
                    v-model="menu"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                            v-model="expiryDate"
                            label="Expiry Date"
                            :prepend-icon="mdiCalendarRange"
                            readonly
                            v-bind="attrs"
                            v-on="on"
                            required
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="expiryDate"
                        @input="menu = false"
                    ></v-date-picker>
                </v-menu>
                <v-text-field
                    v-model="affiliation"
                    label="Affiliation"
                    required
                    :prepend-icon="mdiDomain"
                ></v-text-field>
            </v-container>
            <div class="d-flex">
                <v-btn color="error" class="mr-3" @click="clearForm">
                    Cancel
                </v-btn>
                <v-btn color="secondary" @click="submitForm" :disabled="!checkForm">
                    Submit
                </v-btn>
            </div>
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
        const expiryDate = ref("");
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
            name.value == "";
            expiryDate.value == "";
            affiliation.value == ""
        }

        const checkForm = computed(() => {
            if(username.value == "" || password.value == "" || name.value == "" || expiryDate.value == "" || affiliation.value == ""){
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
                "expiry_date": expiryDate.value,
                "affiliation": affiliation.value,
                "profile_pict": profile
            }
            console.log("submit add profile",submitData)

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
            showPass, clearForm, submitForm, alertMsg, alertMsgShow, alertColour,
            checkForm, userTypes, type, name, expiryDate, affiliation,
            menu, mdiAccountOutline, mdiCalendarRange, mdiDomain,
            mdiCardAccountDetails, breadcrumb
        }
    },
})
</script>
