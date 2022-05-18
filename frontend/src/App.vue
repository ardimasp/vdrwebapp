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

export default {
  components: {
    LayoutBlank,
    LayoutContent,
  },
  async mounted() {
    // fetchAPI
    const userId = store.state.user.id;
    const treeList = store.state.tree.list;

    if(!treeList || treeList.length == 0){
      await store.dispatch("fetchTreeList", userId)
    }
    // end fetchAPI
  },
  setup() {
    // routing
    const { route } = useRouter()
    
    const resolveLayout = computed(() => {
      // Handles initial route
      if (route.value.name === null) {
        return 'layout-blank'
      }

      return 'layout-content'
    })
    // end routing
    
    return {
      resolveLayout,
    }
  },
  // async beforeCreate() {
  //   console.log("before created...")
  //   const userId = store.state.user.id;
  //   const treeList = store.state.tree.list;
  //   if(!treeList || treeList.length == 0){
  //     await store.dispatch("fetchTreeList", userId)
  //   }
  //   console.log("end of before created")
  // }
}
</script>
