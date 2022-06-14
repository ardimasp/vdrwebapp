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
            <!-- 3d subplot plot T_T <a href="https://plotly.com/javascript/3d-subplots/" target="_blank">link here</a> -->
            <div id="plot3d"></div>
            <div id="plot3d2" style="width:80vw"></div>
            <div v-if="showErr">
                <p class="headline font-weight-bold">{{errMsg}}!</p>
                <p class="overline">Press the 'New Prediction' button below to reselect the file and make a new prediction</p>
            </div>
        </v-card>
    </div>
</template>

<script>
import { defineComponent, onMounted, ref, } from '@vue/composition-api'
import sreeyaService from './../../services/sreeya.service'
import Plotly from 'plotly.js-dist-min'

export default defineComponent({
    props:{
        active: {type: String},
        feature: {type: String}
    },
    setup(props) {
        const loading = ref(false);
        const errMsg = ref("");
        const showErr = ref(false);
        onMounted(async () => {
            loading.value = true;
            if(props.active !== null || props.active !== "" || props.feature !== null || props.feature !== ""){
                var result;
                if(props.feature == "oil") result = await sreeyaService.oilPredictionExcel(props.active);
                else result = await sreeyaService.gasPredictionExcel(props.active);
                console.log(result)

                if(result.response && result.response.status == 422) {
                    errMsg.value = result.response.data.detail
                    showErr.value = true
                } else {
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
                        scene: "scene1"
                    }
                    const trace2 = {
                        opacity: 0.5,
                        color: 'rgb(200,100,200)',
                        type: 'mesh3d',
                        x: prediction.data,
                        y: pressDiff.data,
                        z: tempDiff.data,
                        scene: "scene2"
                    }
                    const trace3 = {
                        x: hoursOnline.data,
                        y: prediction.data,
                        mode: 'markers',
                        name: "",
                    }

                    const layout = {
                        title: {
                            text:'Prediction result',
                            font: {
                                family: 'Roboto',
                                size: 24
                            },
                            xref: 'paper',
                            x: 0.05,
                        },
                        height: 600,
                        width: 1000,
                        scene1: {
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
                            domain: {
                                x: [0.0,  0.5],
                            },
                        },
                        scene2: {
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
                            },
                            domain: {
                                x: [0.5, 1],
                            }
                        },
                    }
                    const layout2 = {
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

                    Plotly.newPlot('plot3d', [trace1, trace2], layout)
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
