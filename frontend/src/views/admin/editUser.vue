<template>
    <div>
        <edit-user-skeleton v-if="loading"></edit-user-skeleton>
        <div v-else>
            <!-- <v-alert
                border="left"
                color="secondary"
                dark
                v-if="alertMsgShow"
            >
                Data is updated successfully!
            </v-alert> -->
            <v-snackbar
                v-model="alertMsgShow"
                timeout=3000
                rounded="pill"
                color="secondary"
            >
                Data is updated successfully!
            </v-snackbar>
            <v-breadcrumbs
                :items="breadcrumb"
            ></v-breadcrumbs>
            <div class="text-center">
            <v-avatar size="200">
                <v-img :src="profile"></v-img>
            </v-avatar>
            </div>
            <v-form>
                <v-container>
                    <v-text-field
                        v-model="username"
                        label="username"
                        required
                        :prepend-icon="mdiAccount"
                        readonly
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
                    <v-text-field
                        v-model="password"
                        label="new password"
                        required
                        :prepend-icon="mdiKey"
                        :append-icon="showPass ? mdiEye: mdiEyeOff"
                        :type="showPass ? 'text':'password'"
                        @click:append="showPass = !showPass"
                        v-if="editPassword"
                    ></v-text-field>
                    <div class="d-flex">
                        <v-btn color="error" class="mr-3" @click="clearForm">
                            Cancel
                        </v-btn>
                        <v-btn color="warning" class="mr-3" @click="changeEditStat" v-if="!editPassword">
                            Change Password
                        </v-btn>
                        <v-btn v-else class="mr-3" color="warning" @click="changeEditStat">
                            Cancel New Password
                        </v-btn>
                        <v-btn color="secondary" @click="submitForm">
                            Submit
                        </v-btn>
                    </div>
                </v-container>
            </v-form>
        </div>
    </div>
</template>

<script>
import { computed, defineComponent, onMounted, ref } from '@vue/composition-api'
import {mdiAccount, mdiKey, mdiEye, mdiEyeOff, mdiAccountOutline, 
        mdiCalendarRange, mdiDomain, mdiCardAccountDetails} from '@mdi/js'
import router from './../../router'
import store from '../../store';
import adminService from '../../services/admin.service';
import {detectMimeType} from '../../function'
import editUserSkeleton from './editUserSkeleton.vue'

export default defineComponent({
    components: {
        editUserSkeleton,
    },
    setup() {
        const userid = router.app["_route"].params.userid;
        const detail = computed(() => {
            var users = store.state.admin.userList;
            return users.find(x => x.userid == userid);
        })
        const username = ref(userid);
        const showPass = ref(false);
        const userTypes = ["Premium User", "Regular User"];
        const type = ref("Regular User");
        const name = ref("");
        const expiryDate = ref("");
        const affiliation = ref("");
        const profile = ref("");
        const profile64 = ref(""); //for submit update

        const menu = ref(false);
        const breadcrumb = [
            {
                text: '< Back',
                href: '/admin',
                disable: false,
            }
        ]

        const loading = ref(false)

        onMounted(async() => {
            loading.value = true;
            var res = await adminService.getUserDetail(userid);
            if(res.status == 200) {
                name.value = res.data.data.name;
                type.value = res.data.data.type;
                expiryDate.value = res.data.data.expiry_date;
                affiliation.value = res.data.data.affiliation;
                
                profile64.value = res.data.data.profile_pict;
                let mime = detectMimeType(profile64.value);
                if(mime == "") profile.value = profile64.value
                else profile.value = "data:" + mime + ";base64," + profile64.value
                // profile.value = "data:" + mime + ";base64," + profile64.value
            }
            loading.value = false;
        })

        const clearForm = () => {
            username.value = "";
            password.value = "";
            name.value = "";
            type.value = "";
            expiryDate.value = "";
            affiliation.value = "";
            alertMsgShow.value = false;
            router.push('/admin');
        }
        
        const alertMsgShow = ref(false);
        const submitForm = async () => {
            var submitData
            if(editPassword.value == true){
                submitData = {
                    "userid": username.value,
                    "password": password.value,
                    "type": type.value,
                    "name": name.value,
                    "expiry_date": expiryDate.value,
                    "affiliation": affiliation.value
                }
            } else {
                submitData = {
                    "userid": username.value,
                    "type": type.value,
                    "name": name.value,
                    "expiry_date": expiryDate.value,
                    "affiliation": affiliation.value
                }
            }
            

            let check = await adminService.editUser(submitData);
            if(check == 200) {
                alertMsgShow.value = true;
                password.value = "";
            }
        }

        // password
        const editPassword = ref(false);
        const password = ref("");
        const changeEditStat = () => {
            editPassword.value = !editPassword.value;
            password.value = "";
        }

        return {
            username, password, mdiAccount, mdiKey, mdiEye, mdiEyeOff,
            showPass, clearForm, submitForm, userid, detail,
            alertMsgShow, mdiAccountOutline, mdiCalendarRange, mdiDomain,
            mdiCardAccountDetails, userTypes, type, name, expiryDate, affiliation,
            menu, profile, changeEditStat, editPassword, breadcrumb, loading
        }
    },
})
</script>
