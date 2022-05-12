<template>
  <!-- class viewer container act as a constraint -->
  <div id="viewer-container" class="viewer-container">

    <vtk-card 
      :x="600"
      :y="0"
      title="3D View"
      :w="400"
      :h="500"
    >
    </vtk-card>

    <regular-card 
      :x="0"
      :y="0"
      title="Files"
      :w="400"
      :h="350"
    >
     <template>
       <tree-content></tree-content>
     </template>
    </regular-card>

    <!-- <regular-card
      :x="0"
      :y="350"
      title="text chart"
      :w="400"
      :h="200"
    >
      <template>
        <chart-content></chart-content>
      </template>
    </regular-card> -->
    
    <!-- newly added need to check -->
    <regular-card
      v-for="item in items"
      :key="item.id"
      :x="item.x_dimension"
      :y="item.y_dimension"
      :title="item.name"
      :w="item.width"
      :h="item.height"
    >
      <template>
        <chart-content
          :id="item.id"
        ></chart-content>
      </template>
    </regular-card>

  </div>
</template>

<script>
import store from '../../store'

import RegularCard from './RegularCard.vue'
import TreeContent from './TreeContent.vue'
import VtkCard from './VtkCard.vue'
import ChartContent from './ChartContent.vue'

export default{
  components: {
    RegularCard,
    TreeContent,
    VtkCard,
    ChartContent,
  },
  setup(){
    const items = store.state.viewer.list;

    return {
      items,
    }
  }
}
</script>

<style>
  .viewer-container {
    width: 100%;
    min-height: 600px;
  }
</style>