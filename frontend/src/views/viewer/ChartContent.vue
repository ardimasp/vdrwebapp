<template>
    <div class="chart-container">
        <canvas :id="chartId"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js/auto'
// import store from '../../store';

export default({
    props: {
        id: Number,
    },
    data() {
        this.chart = null;
        return {
            chartId: "chart"+this.id,
            x_data: [],
            y_data: [],
        }
    },
    mounted() {
        // const list_id = store.state.viewer.list.findIndex(x => x.id == this.id);
        this.x_data = [1,3,5,7,0,3,4,6,8,1];
        this.y_data = [0,6,5,3,1,9,7,4,2,3];

        const ctx = document.getElementById(this.chartId).getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.x_data,
                datasets: [{
                    label: 'idk what this',
                    backgroundColor: 'primary',
                    borderColor: '#9155FD',
                    data: this.y_data
                }]
            }
        })
    }
})
</script>

<style scoped>
.chart-container {
    /* margin-left: 20px; */
    width: 900px;
    height:600px;
    background-color: white;
}
</style>
