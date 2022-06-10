<template>
    <v-card class="pa-5">
        <v-card-title class="h4">Prediction</v-card-title>
        <v-container>
            <label>Predict:</label>
            <v-row>
                <v-col sm="3">
                    <v-checkbox
                        v-model="selectFeatures"
                        color="secondary"
                        label="Oil"
                        value="oil"
                    ></v-checkbox>
                </v-col>
                <v-col sm="3">
                    <v-checkbox
                        v-model="selectFeatures"
                        color="secondary"
                        label="Gas"
                        value="gas"
                    ></v-checkbox>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Hours Online</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Hours"
                        v-model="hoursOnline"
                        type="number"
                        dense
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Downhole Temperature</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Temperature"
                        v-model="downholeTemp"
                        type="number"
                        dense
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Downhole Pressure</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Pressure"
                        v-model="downlholePress"
                        type="number"
                        dense
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Pressure Difference</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Difference"
                        v-model="pressDiff"
                        type="number"
                        dense
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Temperature Difference</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Difference"
                        v-model="tempDiff"
                        type="number"
                        dense
                    ></v-text-field>
                </v-col>
            </v-row>
            
            
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader class="font-weight-bold">Prediction Result</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        label="Result"
                        v-model="result"
                        type="number"
                        dense
                        readonly
                    >
                        <template v-slot:progress>
                            <v-progress-linear
                            v-if="custom"
                            :value="progress"
                            color="secondary"
                            absolute
                            height="7"
                            ></v-progress-linear>
                        </template>
                    </v-text-field>
                </v-col>
            </v-row>
            <div class="d-flex flex-row-reverse">
                <v-btn color="secondary" @click="predict" :disabled="!checkPredict">
                    Predict
                </v-btn>
            </div>
        </v-container>
    </v-card>
</template>

<script>
import { computed, defineComponent, ref } from '@vue/composition-api'
import sreeyaService from './../../services/sreeya.service'

export default defineComponent({
    setup() {
        const hoursOnline = ref(0);
        const downholeTemp = ref(0);
        const downlholePress = ref(0);
        const pressDiff = ref(0);
        const tempDiff = ref(0);
        const result = ref();

        // loading
        const custom = ref(false);
        const progress = computed(() => {
            return Math.min(100, this.value.length * 10)
        })

        const selectFeatures = ref("");
        const checkPredict = computed(() => {
            if(selectFeatures.value == "" || selectFeatures.value == null) return false
            return true
        })
        
        const predict = async () => {
            custom.value = true
            var submitData = {
                "hours_online": hoursOnline.value,
                "downhole_temp": downholeTemp.value,
                "downhole_press": downlholePress.value,
                "press_diff": pressDiff.value,
                "temp_diff": tempDiff.value,
            }

            var data;
            if (selectFeatures.value == "oil") data = await sreeyaService.oilPrediction(submitData);
            else data = await sreeyaService.gasPrediction(submitData);
            
            result.value = data.prediction;
            custom.value = false
        }

        return {
            hoursOnline, downholeTemp, downlholePress, pressDiff, tempDiff,
            result, predict, custom, progress, selectFeatures, checkPredict,
        }
    },
})
</script>
