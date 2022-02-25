<template>
  <div>
    <div 
      id="container" 
      :style="{padding: 0, width: divWidth+'px', height: divHeight+'px'}" 
      />
  </div>
</template>

<script>
import { ref, unref, onMounted, onBeforeUnmount, watchEffect, watch } from '@vue/composition-api';

import '@kitware/vtk.js/Rendering/Profiles/Geometry';


import vtkRenderWindow from '@kitware/vtk.js/Rendering/Core/RenderWindow';
import vtkRenderer from '@kitware/vtk.js/Rendering/Core/Renderer';
import vtkOpenGLRenderWindow from '@kitware/vtk.js/Rendering/OpenGL/RenderWindow';
import vtkRenderWindowInteractor from '@kitware/vtk.js/Rendering/Core/RenderWindowInteractor';
import vtkInteractorStyleTrackballCamera from '@kitware/vtk.js/Interaction/Style/InteractorStyleTrackballCamera';

import vtkActor           from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper          from '@kitware/vtk.js/Rendering/Core/Mapper';
import vtkConeSource      from '@kitware/vtk.js/Filters/Sources/ConeSource';

export default {
  name: 'VtkContent',
  props:{
    divWidthProp: {
        type: Number,
        default: 600
    },
    divHeightProp: {
        type: Number,
        default: 400
        },
  },
  setup(props) {
    const context = ref(null);
    const coneResolution = ref(6);
    const representation = ref(2);

    const divWidth = ref(props.divWidthProp);
    const divHeight = ref(props.divHeightProp);

    function setConeResolution(res) {
      coneResolution.value = Number(res);
    }

    function setRepresentation(rep) {
      representation.value = Number(rep);
    }

    function onClick(){
      console.log('clicked')
      const { renderWindow } = context.value;
      console.log(renderWindow.getViews()[0])
      divWidth.value = 100
      divHeight.value = 100
      renderWindow.getViews()[0].setSize(100, 100)
    }

    watch(() => [props.divWidthProp,props.divHeightProp], (currentValue, _oldValue) => {
        const { renderWindow } = context.value;
        divWidth.value = currentValue[0]
        divHeight.value = currentValue[1]
        renderWindow.getViews()[0].setSize(currentValue[0], currentValue[1])
    });

    watchEffect(() => {
      const res = unref(coneResolution);
      const rep = unref(representation);
      if (context.value) {
        const { actor, coneSource, renderWindow } = context.value;
        coneSource.setResolution(res);
        actor.getProperty().setRepresentation(rep);
        renderWindow.render();
      }
    });

    onMounted(() => {
      
      if (!context.value) {

        const container = document.querySelector('#container');
        // VTK renderWindow/renderer
        const renderWindow = vtkRenderWindow.newInstance();
        const renderer     = vtkRenderer.newInstance();
        renderWindow.addRenderer(renderer);

        // WebGL/OpenGL impl
        const openGLRenderWindow =vtkOpenGLRenderWindow.newInstance();
        openGLRenderWindow.setContainer(container);
        openGLRenderWindow.setSize(divWidth.value, divHeight.value);
        renderWindow.addView(openGLRenderWindow);

        // Interactor
        const interactor = vtkRenderWindowInteractor.newInstance();
        interactor.setView(openGLRenderWindow);
        interactor.initialize();
        interactor.bindEvents(container);

        // Interactor style
        const trackball = vtkInteractorStyleTrackballCamera.newInstance();
        interactor.setInteractorStyle(trackball);


        const coneSource = vtkConeSource.newInstance({ height: 1.0 });

        const mapper = vtkMapper.newInstance();
        mapper.setInputConnection(coneSource.getOutputPort());

        const actor = vtkActor.newInstance();
        actor.setMapper(mapper);

        

        renderer.addActor(actor);
        renderer.resetCamera();
        renderWindow.render();

        context.value = {
          renderWindow,
          renderer,
          coneSource,
          actor,
          mapper,
        };
      }
    });

    onBeforeUnmount(() => {
      if (context.value) {
        const {coneSource, actor, mapper } = context.value;
        actor.delete();
        mapper.delete();
        coneSource.delete();
        context.value = null;
      }
    });

    return {
      setRepresentation,
      setConeResolution,
      coneResolution,
      representation,
      onClick,
      divWidth,
      divHeight
    };
  }
}
</script>

<style scoped>
.controls {
  position: relative;
}
</style>