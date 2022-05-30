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
    store.dispatch("setUserToken", localStorage.getItem("user"));
    const state = store.state.auth.logged;
    console.log("at mounted", state, localStorage.getItem("user"));

    if(state) {
      store.dispatch("fetchTreeList")
      store.dispatch("setUsername", localStorage.getItem("username"))
      store.dispatch("setPermission", localStorage.getItem("type"))
      console.log("login data check user", store.state.auth.username, store.state.auth.permission, store.state.auth.logged)
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
