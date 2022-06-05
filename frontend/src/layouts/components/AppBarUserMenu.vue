<template>
  <v-menu
    offset-y
    left
    nudge-bottom="14"
    min-width="230"
    content-class="user-profile-menu-content"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-badge
        bottom
        color="success"
        overlap
        offset-x="12"
        offset-y="12"
        class="ms-4 mt-4"
        dot
      >
        <v-avatar
          size="40px"
          v-bind="attrs"
          v-on="on"
        >
          <img :src="profile">
        </v-avatar>
      </v-badge>
    </template>
    <v-list>
      <div class="pb-3 pt-2">
        <v-badge
          bottom
          color="success"
          overlap
          offset-x="12"
          offset-y="12"
          class="ms-4"
          dot
        >
          <v-avatar size="40px">
            <!-- <v-img :src="require('@/assets/images/avatars/apurwita-480x480.png')"></v-img> -->
            <img :src="profile">
          </v-avatar>
        </v-badge>
        <div
          class="d-inline-flex flex-column justify-center ms-3"
          style="vertical-align:middle"
        >
          <span class="text--primary font-weight-semibold mb-n1">
            {{username}}
          </span>
          <small class="text--disabled text-capitalize">{{type}}</small>
        </div>
      </div>

      <v-divider></v-divider>

      <!-- Profile -->
      <v-list-item link @click.prevent="goProfile">
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiAccountOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <!-- Email -->
      <v-list-item link>
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiEmailOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Inbox</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <!-- Chat -->
      <v-list-item link>
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiChatOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Chat</v-list-item-title>
        </v-list-item-content>

        <v-list-item-action>
          <v-badge
            inline
            color="error"
            content="2"
          >
          </v-badge>
        </v-list-item-action>
      </v-list-item>

      <v-divider class="my-2"></v-divider>

      <!-- Settings -->
      <v-list-item link>
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiCogOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <!-- Pricing -->
      <v-list-item link>
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiCurrencyUsd }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Pricing</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <!-- FAQ -->
      <v-list-item link>
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiHelpCircleOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>FAQ</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider class="my-2"></v-divider>

      <!-- Logout -->
      <v-list-item link @click.prevent="logout">
        <v-list-item-icon class="me-2">
          <v-icon size="22">
            {{ icons.mdiLogoutVariant }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
import {
  mdiAccountOutline,
  mdiEmailOutline,
  mdiCheckboxMarkedOutline,
  mdiChatOutline,
  mdiCogOutline,
  mdiCurrencyUsd,
  mdiHelpCircleOutline,
  mdiLogoutVariant,
} from '@mdi/js'
import store from '../../store'
import router from '../../router'
import { computed, onMounted, ref } from '@vue/composition-api'
import adminService from '../../services/admin.service';
import {detectMimeType} from './../../function'

export default {
  setup() {
    const profile = ref("");
    onMounted(async () => {
      if(!localStorage.getItem("profile")){
        const userid = store.state.auth.username;
        var res = await adminService.getUserDetail(userid);
        if(res.status == 200) {
            let pic = res.data.data.profile_pict;
            let mime = detectMimeType(pic);
            if(mime == "") profile.value = pic
            else profile.value = "data:" + mime + ";base64," + pic
            // profile.value = "data:" + mime + ";base64," + pic
            store.dispatch("setProfile", profile.value);
            localStorage.setItem("profile", profile.value)
        }
      }
      else {
        profile.value = localStorage.getItem("profile")
      }
    })

    const logout = async () => {
      await store.dispatch("resetFileList")
      store.dispatch('logout');
      router.push('/login');
    }
    
    const username = computed(()=> {return store.state.auth.username})
    const type = computed(()=> {return store.state.auth.permission});

    const goProfile = () => {
      router.push({
        name: "profile",
        params: {
          userid: store.state.auth.username
        }
      })
    }

    return {
      logout, username, type, goProfile, profile,
      icons: {
        mdiAccountOutline,
        mdiEmailOutline,
        mdiCheckboxMarkedOutline,
        mdiChatOutline,
        mdiCogOutline,
        mdiCurrencyUsd,
        mdiHelpCircleOutline,
        mdiLogoutVariant,
      },
    }
  },
}
</script>

<style lang="scss">
.user-profile-menu-content {
  .v-list-item {
    min-height: 2.5rem !important;
  }
}
</style>
