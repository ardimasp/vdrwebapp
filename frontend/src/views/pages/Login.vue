<template>
  <div class="auth-wrapper auth-v1">
    <div class="auth-inner">
      <v-card class="auth-card">
        <!-- alert -->
        <v-snackbar
          v-model="setAlert"
          rounded="pill"
          color="secondary"
          timeout="5000"
        >Your session have expired, please login again.</v-snackbar>
        <!-- logo -->
        <v-card-title class="d-flex align-center justify-center py-7">
            <v-img
              :src="require('@/assets/images/logos/logo.svg')"
              max-height="30px"
              max-width="30px"
              alt="logo"
              contain
              class="me-3 "
            ></v-img>

            <h2 class="text-2xl font-weight-semibold">
              VDR
            </h2>
        </v-card-title>

        <!-- title -->
        <v-card-text>
          <p class="text-2xl font-weight-semibold text--primary mb-2">
            Welcome to VDR! 👋🏻
          </p>
          <p class="mb-2">
            Please sign-in to your account and start the adventure
          </p>
        </v-card-text>

        <!-- login form -->
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="username"
              outlined
              label="Username"
              placeholder="john"
              hide-details
              class="mb-3"
            ></v-text-field>

            <v-text-field
              v-model="password"
              outlined
              :type="isPasswordVisible ? 'text' : 'password'"
              label="Password"
              placeholder="············"
              :append-icon="isPasswordVisible ? icons.mdiEyeOffOutline : icons.mdiEyeOutline"
              hide-details
              @click:append="isPasswordVisible = !isPasswordVisible"
            ></v-text-field>

            <p  class="caption" style="color:red" v-if="errorMsg">
              You typed the wrong username or password!
            </p>

            <div class="d-flex align-center justify-space-between flex-wrap">
              <v-checkbox
                label="Remember Me"
                hide-details
                class="me-3 mt-1"
              >
              </v-checkbox>

              <!-- forgot link -->
              <a
                href="javascript:void(0)"
                class="mt-1"
              >
                Forgot Password?
              </a>
            </div>

            
            <v-progress-linear
              v-if="loading"
              indeterminate
              color="secondary"
            ></v-progress-linear>
            <v-snackbar 
              v-model="loading"
              rounded="pill"
              color="secondary"
            >
              Logging you in, preparing your data...
            </v-snackbar>
            <v-btn
              block
              color="primary"
              class="mt-6"
              @click="submitForm"
              :disabled="!checkValid"
            >
              Login
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </div>

    <!-- background triangle shape  -->
    <img
      class="auth-mask-bg"
      height="173"
      :src="require(`@/assets/images/misc/mask-${$vuetify.theme.dark ? 'dark':'light'}.png`)"
    >

    <!-- tree -->
    <v-img
      class="auth-tree"
      width="247"
      height="185"
      src="@/assets/images/misc/tree.png"
    ></v-img>

    <!-- tree  -->
    <v-img
      class="auth-tree-3"
      width="377"
      height="289"
      src="@/assets/images/misc/tree-3.png"
    ></v-img>
  </div>
</template>

<script>
// eslint-disable-next-line object-curly-newline
import { mdiFacebook, mdiTwitter, mdiGithub, mdiGoogle, mdiEyeOutline, mdiEyeOffOutline } from '@mdi/js'
import { computed, onMounted, ref } from '@vue/composition-api'
import store from '../../store'
import router from '../../router'
import adminService from './../../services/admin.service'
import {detectMimeType} from './../../function'

export default {
  setup() {
    const loading = ref(false)
    const isPasswordVisible = ref(false)
    const username = ref('')
    const password = ref('')
    const socialLink = [
      {
        icon: mdiFacebook,
        color: '#4267b2',
        colorInDark: '#4267b2',
      },
      {
        icon: mdiTwitter,
        color: '#1da1f2',
        colorInDark: '#1da1f2',
      },
      {
        icon: mdiGithub,
        color: '#272727',
        colorInDark: '#fff',
      },
      {
        icon: mdiGoogle,
        color: '#db4437',
        colorInDark: '#db4437',
      },
    ]

    const setAlert = computed(() => {return store.state.alert})

    const checkValid = computed(() => {
      if(username.value !== "" && password.value !== "" && loading.value ==false) return true;
      return false;
    })

    onMounted(() => {
      store.dispatch("logout");
    })

    const errorMsg = ref(false);
    const submitForm = async () => {
      loading.value = true;

      let submitData = new FormData();
      submitData.append("username", username.value);
      submitData.append("password", password.value);

      const result = await store.dispatch('login', submitData);

      if(result == 200) {
        errorMsg.value = false;
        await store.dispatch("setUsername", username.value)
        
        var res = await adminService.getUserDetail(username.value);
        if(res.status == 200) {
            let pic = res.data.data.profile_pict;
            let mime = detectMimeType(pic);
            let profile
            if(mime == "") profile = pic
            else profile = "data:" + mime + ";base64," + pic
            // profile.value = "data:" + mime + ";base64," + pic
            localStorage.setItem("profile", profile)
        }

        if(store.state.auth.permission == "Administrator") {
          await store.dispatch("fetchUserList")
          await router.push('/admin')
          await store.dispatch("setLoad", false)
        }
        else if(store.state.auth.permission == "Premium User") {
          await store.dispatch("fetchTreeList")
          await store.dispatch("fetchSreeyaList")
          await store.dispatch("fetchVtpList")
          await router.push('/');
          await store.dispatch("setLoad", false)
        }
        else {
          await store.dispatch("fetchTreeList");
          await store.dispatch("fetchVtpList");
          await router.push('/');
          await store.dispatch("setLoad", false)
        }
      }
      else errorMsg.value = true;
      loading.value = false;
    }

    return {
      isPasswordVisible,
      username,
      password,
      socialLink,
      submitForm,
      checkValid,
      errorMsg,
      loading, setAlert,

      icons: {
        mdiEyeOutline,
        mdiEyeOffOutline,
      },
    }
  },
}
</script>

<style lang="scss">
@import '~@/plugins/vuetify/default-preset/preset/pages/auth.scss';
</style>
