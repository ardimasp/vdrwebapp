<template>
    <v-container class="text-center">
        <v-icon x-large color="primary">
            {{mdiAlertCircleOutline}}
        </v-icon>
        <div>
            <h6 class="display-1">
                Sorry, you do not have the permission to access this page.<br>
                <span style="color:#4DB6AC">Please</span> contact the administrator!
            </h6>
        </div>
    </v-container>
</template>

<script>
import { defineComponent, onMounted } from '@vue/composition-api'
import {mdiAlertCircleOutline} from '@mdi/js'
import store from '../../store'
import router from '../../router'

export default defineComponent({
    setup() {
        onMounted(() => {
            if(store.state.auth.permission == "Premium User") router.push('/production')
        })

        const warningSvg = "warning.svg"

        return {
            warningSvg, mdiAlertCircleOutline
        }
    },
})
</script>
