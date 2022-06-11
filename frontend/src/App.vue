<template>
  <component :is="resolveLayout">
    <router-view></router-view>
  </component>
</template>

<script>
import { computed, } from '@vue/composition-api'
import { useRouter } from '@/utils'
import LayoutBlank from '@/layouts/Blank.vue'
import LayoutContent from '@/layouts/Content.vue'
import LayoutAdmin from '@/layouts/TopContent.vue'
import store from './store'
import route from './router'
import {decode, decryptToken, encryptToken } from './function'
// import CryptoJS from "crypto-js";
// import {checkToken} from './check.js'

export default {
  components: {
    LayoutBlank,
    LayoutContent,
    LayoutAdmin,
  },
  async mounted() {
    store.dispatch("resetFileList")
    // fetchAPI
    const state = store.state.auth.logged;
    // console.log("check at main",localStorage.getItem("user"))

    if(state) {
      store.dispatch("setToken", decryptToken(localStorage.getItem("user")))
      store.dispatch("fetchTreeList")

      // const decrypt = await decryptToken(store.state.auth.user)
      // const data = await decode(decrypt);
      const data = decode(store.state.auth.user)
      store.dispatch("setUsername", data.userid)
      store.dispatch("setPermission", data.type)
      store.dispatch("setString", data.exp);

      if(store.state.auth.permission == "Premium User") store.dispatch("fetchSreeyaList")

      // test
      var encrypt = encryptToken(localStorage.getItem("user"))
      console.log("at main encrypt", encrypt)
      console.log("decrypt", decryptToken(encrypt))
      console.log("localstorage", localStorage.getItem("user"))
      console.log("jwt", decode(decryptToken(encrypt)))
    }
    else route.push('/login');
    // end fetchAPI
  },
  setup() {
    // routing
    const { route } = useRouter()
    
    const resolveLayout = computed(() => {
      // Handles initial route
      if (route.value.meta.layout == "blank") {
        return 'layout-blank'
      }
      else if (route.value.meta.layout == "top") {
        return 'layout-admin'
      }

      return 'layout-content'
    })
    // end routing
    
    return {
      resolveLayout, route,
    }
  },
}
</script>
