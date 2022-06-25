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
import {decode, decryptToken } from './function'
// import CryptoJS from "crypto-js";
// import {checkToken} from './check.js'

export default {
  components: {
    LayoutBlank,
    LayoutContent,
    LayoutAdmin,
  },
  async mounted() {
    // store.dispatch("resetFileList")
    // fetchAPI
    const state = store.state.auth.logged;
    // const aaa = require('process.env')
    // console.log(process.env.VUE_APP_ENDPOINT)

    if(state) {
      await store.dispatch("setLoad", true)
      await store.dispatch("setToken", decryptToken(localStorage.getItem("user")))
      const data = decode(store.state.auth.user)
      await store.dispatch("setUsername", data.userid)
      await store.dispatch("setPermission", data.type)
      await store.dispatch("setString", data.exp);

      await store.dispatch("fetchTreeList")
      await store.dispatch("fetchVtpList")

      if(store.state.auth.permission == "Premium User") await store.dispatch("fetchSreeyaList")

      await store.dispatch("setLoad", false)
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
