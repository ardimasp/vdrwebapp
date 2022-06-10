<template>
    <div>
        <v-card
            class="mb-12"
            color="grey lighten-1"
            height="200px"
        >
            3d surface plot T_T <a href="https://plotly.com/javascript/3d-subplots/" target="_blank">link here</a>
        </v-card>
    </div>
</template>

<script>
import { defineComponent, onMounted, ref, } from '@vue/composition-api'
// import sreeyaService from './../../services/sreeya.service'

export default defineComponent({
    props:{
        active: {type: String},
        feature: {type: String}
    },
    setup(props) {
        const data = ref();

        onMounted(async () => {
            if(props.active !== null || props.active !== "" || props.feature !== null || props.feature !== ""){
                data.value = "AAAAAAA"
            }
        })

        return {
            
        }
    },
})
</script>
