<template>
    <v-container>
        <profile-skeleton
            v-if="load"
        ></profile-skeleton>
        <v-alert
            border="left"
            color="secondary"
            dark
            v-if="passwordUpdated"
        >
            Password is updated successfully!
        </v-alert>
        <v-row no-gutters>
            <v-col
                cols="12"
                sm="4"
                md="4"
                class="text-center"
            >
                <v-avatar size=200>
                    <v-img aspect-ratio="1" 
                        :src="profPic">
                    </v-img>
                </v-avatar>
                <div>
                    <v-file-input
                        accept="image/*"
                        label="Choose new image"
                        v-model="imageProfile"
                        @change="setNewProfile"
                        messages="Image upload limit is 4MB"
                    >
                    </v-file-input>
                    <v-avatar size=100 v-if="newImage" class="mt-5 mb-5">
                        <v-img aspect-ratio="1" 
                            :src="newImage">
                        </v-img>
                    </v-avatar>
                    <div v-if="newImage">
                        <p  class="caption" style="color:red" v-if="!checkImg">
                            Your file input exceeds the 4MB limit!
                        </p>
                        <v-btn color="error" class="mr-3" @click="clearImage">
                            Cancel
                        </v-btn>
                        <v-btn color="secondary" @click="submitImage" :disabled="!checkImg">
                            Save
                        </v-btn>
                    </div>
                </div>
            </v-col>
            <v-col
                cols="12"
                sm="8"
                md="8"
            >
                <v-container>
                    <v-form>
                        <v-text-field
                            v-model="username"
                            label="Username"
                            required
                            :prepend-icon="mdiAccount"
                            readonly
                        ></v-text-field>
                        <v-text-field
                            v-model="type"
                            label="User Type"
                            required
                            :prepend-icon="mdiCardAccountDetails"
                            readonly
                        ></v-text-field>
                        <v-text-field
                            v-model="name"
                            label="Name"
                            required
                            :prepend-icon="mdiAccountOutline"
                            readonly
                        ></v-text-field>
                        <v-text-field
                            v-model="expiryDate"
                            label="Expiry Date"
                            required
                            :prepend-icon="mdiCalendarRange"
                            readonly
                        ></v-text-field>
                        <v-text-field
                            v-model="affiliation"
                            label="Affiliation"
                            required
                            :prepend-icon="mdiDomain"
                            readonly
                        ></v-text-field>
                        <v-btn color="secondary" v-if="!editPassword" @click="changeEditStat">
                            Edit Password
                        </v-btn>
                        <div v-else>
                            <v-text-field
                                v-model="password"
                                label="Password"
                                :prepend-icon="mdiKey"
                                type="password"
                            ></v-text-field>
                            <v-text-field
                                v-model="confirmPassword"
                                label="Confirm Password"
                                :prepend-icon="mdiKey"
                                type="password"
                            ></v-text-field>
                            <p  class="caption" style="color:red" v-if="!checkPassword">
                                Your confirm password is not the same!
                            </p>
                            <div class="d-flex">
                                <v-btn color="error" class="mr-3" @click="changeEditStat">
                                    Cancel
                                </v-btn>
                                <v-btn color="secondary" @click="submitPassword" :disabled="!checkPassword">
                                    Submit
                                </v-btn>
                            </div>
                        </div>
                    </v-form>
                </v-container>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { computed, defineComponent, onMounted, ref } from '@vue/composition-api'
import { mdiAccount, mdiAccountOutline, mdiCalendarRange,
        mdiDomain, mdiCardAccountDetails, mdiKey } from '@mdi/js'
import store from '../../store';
import router from '../../router';
import adminService from '../../services/admin.service';
import {detectMimeType} from './../../function'
import ProfileSkeleton from './ProfileSkeleton.vue'

export default defineComponent({
    components: {
        ProfileSkeleton
    },
    setup() {
        const username = store.state.auth.username;
        const type = ref("");
        const name = ref("");
        const expiryDate = ref("");
        const affiliation = ref("");
        const profPic = ref("");
        const imageProfile = ref() //change profile pic file choose
        const newImage = ref("");

        // IMAGE
        const checkImg = computed(() => {
            if(imageProfile.value == null || imageProfile.value == "") return false;
            else {
                if(imageProfile.value.size > 4194304) return false
                return true;
            }
        })
        const clearImage = () => {
            imageProfile.value = null;
            newImage.value = "";
        }

        const setNewProfile = () => {
            passwordUpdated.value = false;
            let file = imageProfile.value;
            console.log("check size", file);
            let reader = new FileReader();
            reader.onloadend = function() {
                // console.log('RESULT: ', reader.result);
                newImage.value = reader.result;
            }
            reader.readAsDataURL(file);
            // console.log(b64);
        }

        const submitImage = async () => {
            var submitData = {
                "userid": username,
                "profile_pict": newImage.value
            }
            let check = await adminService.editUser(submitData);
            if(check == 200){
                profPic.value = newImage.value;
                clearImage();
                localStorage.setItem("profile", profPic.value)
            }
        }
        // END IMAGEEE

        const load = ref(false)
        onMounted(async () => {
            load.value = true;
            if(router.app["_route"].params.userid !== username){
                router.push({
                    name: 'profile',
                    params: {
                        userid: username
                    }
                })
            }
            else {
                var res = await adminService.getUserDetail(username);
                if(res.status == 200) {
                    name.value = res.data.data.name;
                    type.value = res.data.data.type;
                    expiryDate.value = res.data.data.expiry_date;
                    affiliation.value = res.data.data.affiliation;

                    let pic = res.data.data.profile_pict;
                    let mime = detectMimeType(pic);
                    if(mime == "") profPic.value = pic
                    else profPic.value = "data:" + mime + ";base64," + pic
                }
            }
            load.value = false;
        })

        // password
        const editPassword = ref(false);
        const password = ref("");
        const confirmPassword = ref("");
        const passwordUpdated = ref(false);
        const changeEditStat = () => {
            editPassword.value = !editPassword.value;
            password.value = "";
            confirmPassword.value = "";
            if(passwordUpdated.value==true && editPassword.value==true) passwordUpdated.value=false;
        }
        const checkPassword = computed(() => {
            if(password.value !== "" &&  password.value == confirmPassword.value) return true;
            return false;
        })
        const submitPassword = async () => {
            var submitData = {
                "userid": username,
                "password": password.value,
            }
            let check = await adminService.editUser(submitData);
            if(check == 200){
                passwordUpdated.value = true
                changeEditStat()
            }
        }
        // END PASSWORD

        return {
            username, type, name, expiryDate, affiliation, profPic,
            mdiAccount, mdiAccountOutline, mdiCalendarRange, mdiDomain,
            mdiCardAccountDetails, imageProfile, checkImg, clearImage,
            setNewProfile, submitImage, newImage, editPassword,
            changeEditStat, password, confirmPassword, submitPassword,
            checkPassword, mdiKey, passwordUpdated, load
        }
    },
})
</script>
