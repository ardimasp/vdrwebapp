<template>
  <v-app>
    <vertical-nav-menu :is-drawer-open.sync="isDrawerOpen"></vertical-nav-menu>

    <v-app-bar
      app
      flat
      color="#F4F5FA"
      style="z-index: 9999"

    >
      <div class="boxed-container w-full">
        <div class="d-flex align-center mx-6">
          <!-- Left Content -->
          <v-app-bar-nav-icon
            class="d-block me-2"
            @click="isDrawerOpen = !isDrawerOpen"
          >
            <v-icon>
              {{ isDrawerOpen ? icons.mdiChevronLeft: icons.mdiChevronRight }}
            </v-icon>
          </v-app-bar-nav-icon>

          <v-spacer></v-spacer>

          <!-- Right Content -->
          <!-- <v-btn
            icon
            small
            class="ms-3"
          >
            <v-icon>
              {{ icons.mdiBellOutline }}
            </v-icon>
          </v-btn> -->
          <app-bar-user-menu></app-bar-user-menu>
        </div>
      </div>
    </v-app-bar>

    <v-main>
      <div class="app-content-container boxed-container pa-6">
        <slot></slot>
      </div>
    </v-main>

    <v-footer
      app
      inset
      height="56"
      color="#F4F5FA"
      bottom
      class="px-0 footer-pos"
    >
      <div class="boxed-container w-full">
        <div class="mx-6">
          <span>
            &copy; {{ currentYear }} <a
              href="https://international.binus.ac.id/"
              class="text-decoration-none"
              target="_blank"
            >Binus International</a></span>
        </div>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { ref, watch } from '@vue/composition-api'
import { mdiMagnify, mdiBellOutline, mdiChevronLeft, mdiChevronRight  } from '@mdi/js'
import VerticalNavMenu from './components/vertical-nav-menu/VerticalNavMenu.vue'
import AppBarUserMenu from './components/AppBarUserMenu.vue'
import store from '../store'

export default {
  components: {
    VerticalNavMenu,
    AppBarUserMenu,
  },
  setup() {
    const isDrawerOpen = ref(null)
    const currentYear = ref((new Date()).getFullYear())
    
    watch(() => isDrawerOpen.value, () =>{
      if(isDrawerOpen.value == null){return}
      else{ store.dispatch("updateDrawer", isDrawerOpen.value)}
    })
    return {
      isDrawerOpen,
      currentYear,

      // Icons
      icons: {
        mdiMagnify,
        mdiBellOutline,
        mdiChevronLeft,
        mdiChevronRight,
      },
    }

  },
}
</script>

<style lang="scss" scoped>
.v-app-bar ::v-deep {
  .v-toolbar__content {
    padding: 0;
    background-color: #f4f5fa;
    .app-bar-search {
      .v-input__slot {
        padding-left: 18px;
      }
    }
  }
}

.boxed-container {
  // max-width: 1440px;
  // margin-left: auto;
  // margin-right: auto;
  background-color: #f4f5fa;

}

.footer-pos{
  position: absolute;
  z-index: 9999;
  background-color: #f4f5fa;

}

// .header-pos{
//   // position: fixed;
//   // left: 0;
//   // top: 0;
//   // z-index: 9999;
//   margin-top: 30px;


// }
// @media (max-height:855px){
// .header-margin{
//   // top: 10;
//   // margin-top: 20px;

//   margin-bottom: 35px;

// }
// }
</style>
