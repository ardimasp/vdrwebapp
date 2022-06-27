<template>
    <div>
        <v-row>
            <v-col cols="12" sm="6">
                <v-card>
                    <v-container>
                        <v-card-title>
                            Regular User
                        </v-card-title>
                        <v-card-subtitle class="subtitle-2 font-weight-bold">
                            Price: <span style="color:#4DB6AC">Rp 10,000</span>
                        </v-card-subtitle>
                        <v-card-text>
                            Features:
                            <ul>
                                <li>3D Viewer</li>
                                <li>3D Viewer Map</li>
                                <li>Data Showcase</li>
                                <li>File Management</li>
                                <br>
                            </ul>
                        </v-card-text>
                    </v-container>
                </v-card>
            </v-col>
            <v-col cols="12" sm="6">
                <v-card>
                    <v-container>
                        <v-card-title>
                            Premium User
                        </v-card-title>
                        <v-card-subtitle class="subtitle-2 font-weight-bold">
                            Price: <span style="color:#4DB6AC">Rp 100,000</span>
                        </v-card-subtitle>
                        <v-card-text>
                            Features:
                            <ul>
                                <li>3D Viewer</li>
                                <li>3D Viewer Map</li>
                                <li>Data Showcase</li>
                                <li>File Management</li>
                                <li>Production AI</li>
                            </ul>
                        </v-card-text>
                    </v-container>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
    setup() {
        
    },
})
</script>
