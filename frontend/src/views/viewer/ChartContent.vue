<template>
    <div>
        <canvas :id="chartId"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js/auto'
import store from '../../store';

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
        const list_id = store.state.viewer.list.findIndex(x => x.id == this.id);
        this.x_data = store.state.viewer.list[list_id].x_data;
        this.y_data = store.state.viewer.list[list_id].y_data;

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
