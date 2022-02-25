<template>
  <div id="viewer-container">

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
      title="Tree View"
      :w="400"
      :h="200"
    >
     <template>
       <test-content></test-content>
     </template>
    </regular-card>
    
  </div>
</template>

<script>
import RegularCard from './RegularCard.vue'
import TestContent from './TestContent.vue'
import VtkCard from './VtkCard.vue'

export default {
  data: function () {
    return {
    }
  },
  components: {
    RegularCard,
    TestContent,
    VtkCard,
  },
  mounted(){
  },
  methods: {
    
  },
  setup() {
    return {
      
    }
  }
}
</script>