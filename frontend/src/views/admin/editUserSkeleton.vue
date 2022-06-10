<template>
    <v-container>
        <div class="text-center">
            <v-skeleton-loader
                type="image"
            ></v-skeleton-loader>
        </div>
        <v-skeleton-loader
            type="list-item-two-line, list-item-two-line, list-item-two-line, list-item-two-line, list-item-two-line, actions"
        ></v-skeleton-loader>
    </v-container>
</template>

<script>
import { defineComponent} from '@vue/composition-api'

export default defineComponent({
    setup() {

        return {
        }
    },
})
</script>
