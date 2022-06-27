<template>
    <div>
        <v-form lazy-validation v-model="validForm">
        <v-container>
            <div class="d-flex align-center justify-space-between">
                <label>Predict:</label>
                <v-col cols="4">
                    <v-select
                        dense
                        outlined
                        v-model="tempMeasurement"
                        :items="tempOptions"
                        label="temperature"
                    ></v-select>
                </v-col>
            </div>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Hours Online</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        v-model="hoursOnline"
                        type="number"
                        hint="value ≥ 0"
                        persistent-hint
                        suffix="hours"
                        dense
                        required
                        :rules="[v=>(v && v>=0) || 'value ≥ 0']"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Downhole Temperature</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        v-model="downholeTemp"
                        type="number"
                        hint="0 ≤ value ≤ 172"
                        persistent-hint
                        :suffix="tempMeasurement == 'celcius' ? '°C':'°F'"
                        dense
                        required
                        :rules="[v=>(v && v>=0 && v<=172) || '0 ≤ value ≤ 172']"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Downhole Pressure</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        v-model="downholePress"
                        type="number"
                        hint="0 ≤ value ≤ 308"
                        persistent-hint
                        suffix="bar"
                        dense
                        required
                        :rules="[v=>(v && v>=0 && v<=308) || '0 ≤ value ≤ 308']"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Pressure Difference</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        v-model="pressDiff"
                        type="number"
                        hint="0 ≤ value ≤ 325"
                        persistent-hint
                        suffix="bar"
                        dense
                        required
                        :rules="[v=>(v && v>=0 && v<=325) || '0 ≤ value ≤ 325']"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" sm="3">
                    <v-subheader>Temperature Difference</v-subheader>
                </v-col>
                <v-col cols="12" sm="9">
                    <v-text-field
                        v-model="tempDiff"
                        type="number"
                        hint="0 ≤ value ≤ 190"
                        persistent-hint
                        :suffix="tempMeasurement == 'celcius' ? '°C':'°F'"
                        dense
                        required
                        :rules="[v=>(v && v>=0 && v<=190) || '0 ≤ value ≤ 190']"
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
                        dense
                        readonly
                        :suffix="feature=='oil'?'m³':'x10⁶ ft³'"
                    >
                    </v-text-field>
                </v-col>
            </v-row>
            <div class="d-flex flex-row-reverse">
                <v-btn color="secondary" @click="predict" :disabled="!checkPredict || !validForm">
                    Predict
                </v-btn>
            </div>
        </v-container>
        </v-form>
    </div>
</template>

<script>
import { defineComponent, ref, computed } from '@vue/composition-api'
import sreeyaService from './../../services/sreeya.service'

export default defineComponent({
    props: {
        feature: {type:String},
    },
    setup(props) {
        const validForm = ref(true)

        const hoursOnline = ref(0);
        const downholeTemp = ref(0);
        const downholePress = ref(0);
        const pressDiff = ref(0);
        const tempDiff = ref(0);
        const result = ref();

        const tempOptions = ["celcius", "fahrenheit"];
        const tempMeasurement = ref("celcius");

        const checkPredict = computed(() => {
            if (hoursOnline.value < 0) return false
            if (downholePress.value < 0 || downholePress.value > 308) return false
            if (downholeTemp.value < 0 || downholeTemp.value > 172) return false
            if (pressDiff.value < 0 || pressDiff.value > 325) return false
            if (tempDiff.value < 0 || tempDiff.value > 190) return false

            return true
        })
        
        const predict = async () => {
            var submitData = {
                "hours_online": hoursOnline.value,
                "downhole_temp": downholeTemp.value,
                "downhole_press": downholePress.value,
                "press_diff": pressDiff.value,
                "temp_diff": tempDiff.value,
                "deg": tempMeasurement.value
            }

            var data;
            if (props.feature == "oil") data = await sreeyaService.oilPrediction(submitData);
            else data = await sreeyaService.gasPrediction(submitData);
            
            result.value = data.prediction;
        }

        return {
            hoursOnline, downholeTemp, downholePress, pressDiff, tempDiff,
            result, predict, checkPredict, validForm, tempMeasurement, tempOptions
        }
    },
})
</script>
