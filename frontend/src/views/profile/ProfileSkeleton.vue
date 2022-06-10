<template>
    <v-container>
        <v-row no-gutters>
            <v-col
                cols="12"
                sm="4"
                md="4"
                class="text-center"
            >
                <v-skeleton-loader
                    type="image, list-item-two-line"
                ></v-skeleton-loader>
            </v-col>
            <v-col
                cols="12"
                sm="8"
                md="8"
            >
                    <v-form>
                        <v-skeleton-loader
                            type="article, list-item-two-line, list-item-two-line, list-item-two-line, list-item-two-line, list-item-two-line, actions"
                        ></v-skeleton-loader>
                    </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
    setup() {
        
    },
})
</script>
