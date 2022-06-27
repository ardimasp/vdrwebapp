<template>
  <v-app>
    <v-app-bar
      app
      flat
      color="#F4F5FA"
    >
      <div class="boxed-container w-full">
        <div class="d-flex align-center mx-6">
          <!-- Left Content -->
          <v-app-bar-nav-icon
            class="d-block me-2"
            @click.prevent="goHome"
          >
            <v-img
                :src="require('@/assets/images/logos/V_logo.png')"
                max-height="30px"
                max-width="30px"
                alt="logo"
                contain
                eager
                class="app-logo"
            ></v-img>
            <!-- <v-slide-x-transition>
            <h2 class="app-title text--primary">
                VDR
            </h2>
            </v-slide-x-transition> -->
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
      class="px-0"
      color="#F4F5FA"
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
import { ref } from '@vue/composition-api'
import { mdiMagnify, mdiBellOutline, mdiChevronLeft, mdiChevronRight  } from '@mdi/js'
import AppBarUserMenu from './components/AppBarUserMenu.vue'
import router from '../router'
import store from '../store'

export default {
  components: {
    AppBarUserMenu,
  },
  setup() {
    const currentYear = ref((new Date()).getFullYear())

    const goHome = () => {
      if(store.state.auth.permission == "Administrator") router.push('/admin')
      else router.push('/')
    }

    return {
      currentYear,
      goHome,

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
}

.app-content-container {
  // margin-top: -30px;
}
</style>
