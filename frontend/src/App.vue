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
import store from './store'
import route from './router'
// import {checkToken} from './check.js'

export default {
  components: {
    LayoutBlank,
    LayoutContent,
  },
  async mounted() {
    store.dispatch("resetFileList")
    // fetchAPI
    store.dispatch("setUserToken", localStorage.getItem("user"));
    const state = store.state.auth.logged;
    console.log("at mounted", state, localStorage.getItem("user"));

    // const userId = store.state.user.id;
    // const treeList = store.state.tree.list;
    // let check = await checkToken();
    // console.log("check token at initial", check, userId)

    if(state) store.dispatch("fetchTreeList")
    else route.push('/login');

    // if(userId !== "" && check){  //if user token is not null and token is correct
    //   if(!treeList || treeList.length == 0){
    //     await store.dispatch("fetchTreeList", userId)
    //   }
    // } 
    // else {
    //   route.push('/login');
    // }
    
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

      return 'layout-content'
    })
    // end routing
    
    return {
      resolveLayout, route,
    }
  },
}
</script>
