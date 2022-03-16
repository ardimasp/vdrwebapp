<template>
  <v-app>
    <vertical-nav-menu :is-drawer-open.sync="isDrawerOpen"></vertical-nav-menu>

    <v-app-bar class="header-pos"
      app
      flat
      style="z-index: 9999"

    >
      <div class="header-margin boxed-container w-full h-5">
        <div class="d-flex align-center mx-6 my-6">
          <!-- Left Content -->
          <v-app-bar-nav-icon
            class="d-block me-2 mt-5"
            @click="isDrawerOpen = !isDrawerOpen"
          >
            <v-icon>
              {{ isDrawerOpen ? icons.mdiChevronLeft: icons.mdiChevronRight }}
            </v-icon>
          </v-app-bar-nav-icon>

          <v-spacer></v-spacer>

          <!-- Right Content -->
          <v-btn
            icon
            small
            class="ms-3 mt-4"
          >
            <v-icon>
              {{ icons.mdiBellOutline }}
            </v-icon>
          </v-btn>
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
      bottom
      style="background-color: #f4f5fa;"
      class="px-0 footer-pos"
    >
      <div class="boxed-container w-full">
        <div class="mx-6 d-flex justify-space-between">
          <span>
            &copy; {{ currentYear }} <a
              href="https://international.binus.ac.id/"
              class="text-decoration-none"
              target="_blank"
            >Binus International</a></span>
          <span class="d-sm-inline d-none">
            <a
              href="https://international.binus.ac.id/computer-science/category/article/"
              target="_blank"
              class="me-6 text--secondary text-decoration-none"
            >Blog</a>
          </span>
        </div>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
import { ref } from '@vue/composition-api'
import { mdiMagnify, mdiBellOutline, mdiChevronLeft, mdiChevronRight  } from '@mdi/js'
import VerticalNavMenu from './components/vertical-nav-menu/VerticalNavMenu.vue'
import AppBarUserMenu from './components/AppBarUserMenu.vue'

export default {
  components: {
    VerticalNavMenu,
    AppBarUserMenu,
  },
  setup() {
    const isDrawerOpen = ref(null)
    const currentYear = ref((new Date()).getFullYear())

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

.app-content-container {
  margin-top: -50px;
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
