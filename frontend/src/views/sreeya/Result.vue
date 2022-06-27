<template>
    <div>
        <v-skeleton-loader
            v-if="loading"
            type="card"
            width="100%"
        ></v-skeleton-loader>
        <v-card
            v-show="!loading"
            class="mb-12"
            color="grey lighten-1"
        >
            <div v-if="showErr">
                <p class="headline font-weight-bold" v-for="err in errMsg" :key="err">{{err}}!</p>
                <p class="overline">Press the 'New Prediction' button below to reselect the file and make a new prediction</p>
            </div>
            <div v-else>
                <v-row>
                    <v-col cols="12" md="6">
                        <div id="plot3d"></div>
                    </v-col>
                    <v-col cols="12" md="6">
                        <div id="plot3d2"></div>
                    </v-col>
                </v-row>
                <v-row>
                    <v-col cols="12" md="6">
                        <div id="plot3d1"></div>
                    </v-col>
                    <v-col cols="12" md="6">
                        <sreeya-prediction :feature="feature"></sreeya-prediction>
                    </v-col>
                </v-row>
            </div>
        </v-card>
    </div>
</template>

<script>
import { defineComponent, onMounted, ref, } from '@vue/composition-api'
import sreeyaService from './../../services/sreeya.service'
import Plotly from 'plotly.js-dist-min'
import SreeyaPrediction from './SreeyaPrediction.vue'

export default defineComponent({
    props:{
        active: {type: String},
        feature: {type: String}
    },
    components: {
        SreeyaPrediction,
    },
    setup(props) {
        const loading = ref(false);
        const errMsg = ref([]);
        const showErr = ref(false);
        onMounted(async () => {
            loading.value = true;
            errMsg.value = [];
            showErr.value = false;
            if(props.active !== null || props.active !== "" || props.feature !== null || props.feature !== ""){
                var result;
                if(props.feature == "oil") result = await sreeyaService.oilPredictionExcel(props.active);
                else result = await sreeyaService.gasPredictionExcel(props.active);

                if(result.response && result.response.status == 422) {
                    if(Array.isArray(result.response.data.detail)) {
                        errMsg.value = null;
                        errMsg.value = result.response.data.detail
                    }
                    else errMsg.value.push(result.response.data.detail)
                    showErr.value = true
                }
                else if(result.response && result.response.status == 400) {
                    errMsg.value.push(result.response.data.detail)
                    showErr.value = true
                } 
                else {
                    var hoursOnline = result.data[0];
                    var downholeTemp = result.data[1];
                    var downholePress = result.data[2];
                    var pressDiff = result.data[3];
                    var tempDiff = result.data[4];
                    var prediction = result.data[5];

                    const trace1 = {
                        opacity: 0.5,
                        color: "pink",
                        type: 'mesh3d',
                        x: prediction.data,
                        y: downholeTemp.data,
                        z: downholePress.data,
                    }
                    const trace2 = {
                        opacity: 0.5,
                        color: 'rgb(200,100,200)',
                        type: 'mesh3d',
                        x: prediction.data,
                        y: pressDiff.data,
                        z: tempDiff.data,
                    }
                    const trace3 = {
                        x: hoursOnline.data,
                        y: prediction.data,
                        mode: 'markers',
                        name: "",
                    }

                    const layout = {
                        scene: {
                            xaxis: {title: "x-"+prediction.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            },
                            yaxis: {title: "y-"+downholeTemp.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            },
                            zaxis: {title: "z-"+prediction.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            },
                        },
                        width:500,
                    }
                    const layout1 = {
                        width:500,
                        scene: {
                            xaxis: {title: "x-"+prediction.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            },
                            yaxis: {title: "y-"+pressDiff.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            },
                            zaxis: {title: "z-"+prediction.label,
                                titlefont: {
                                    family: 'Roboto',
                                    size: 12,
                                    color: '#7f7f7f'
                                }
                            }
                        }
                    }
                    const layout2 = {
                        width:500,
                        xaxis: {
                            title: {
                            text: "x-"+hoursOnline.label,
                            font: {
                                family: 'Roboto',
                                size: 12,
                                color: '#7f7f7f'
                            }
                            },
                        },
                        yaxis: {
                            title: {
                            text: "y-"+prediction.label,
                            font: {
                                family: 'Roboto',
                                size: 12,
                                color: '#7f7f7f'
                            }
                            }
                        }
                    };

                    Plotly.newPlot('plot3d', [trace1], layout)
                    Plotly.newPlot('plot3d1', [trace2], layout1)
                    Plotly.newPlot('plot3d2', [trace3], layout2)
                    loading.value = false;
                }
            }
            loading.value = false;
        })

        return {
            loading, errMsg, showErr
        }
    },
})
</script>
