<template>
  <div>
    <div 
      id="container" 
      :style="{padding: 0, width: divWidth+'px', height: divHeight+'px'}" 
      />
  </div>
</template>

<script>
import { ref, onMounted, watch } from '@vue/composition-api';

import '@kitware/vtk.js/Rendering/Profiles/Geometry';

import vtkRenderWindow from '@kitware/vtk.js/Rendering/Core/RenderWindow';
import vtkRenderer from '@kitware/vtk.js/Rendering/Core/Renderer';
// import vtkCamera  from '@kitware/vtk.js/Rendering/Core/Camera';
import vtkOpenGLRenderWindow from '@kitware/vtk.js/Rendering/OpenGL/RenderWindow';
import vtkRenderWindowInteractor from '@kitware/vtk.js/Rendering/Core/RenderWindowInteractor';
import vtkInteractorStyleTrackballCamera from '@kitware/vtk.js/Interaction/Style/InteractorStyleTrackballCamera';

import vtkActor           from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper          from '@kitware/vtk.js/Rendering/Core/Mapper';
import vtkConeSource      from '@kitware/vtk.js/Filters/Sources/ConeSource';

import vtkColorTransferFunction from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction';
import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';

import vtkAxesActor from '@kitware/vtk.js/Rendering/Core/AxesActor';
import vtkOrientationMarkerWidget from '@kitware/vtk.js/Interaction/Widgets/OrientationMarkerWidget';

import { ColorMode, ScalarMode, } from '@kitware/vtk.js/Rendering/Core/Mapper/Constants';

export default {
  name: 'VtpContent',
  props:{
    divWidthProp: {
        type: Number,
        default: 500
    },
    divHeightProp: {
        type: Number,
        default: 400
        },
    dataVtp: {
        type: Object,
        default: null
        },
  },
  data(){
      return {
          mapper: null,
          actor: null,
          colorMap: null,
          lookupTable: null,
          dataRange: null,
      }
  },
  watch: { 
    dataVtp: function(newVal) { // watch it
      this.onUpdateVtp(newVal);
    }
  },
  methods: {
    changeColorMapName(colormapname,gain){
      this.lookupTable.applyColorMap(vtkColorMaps.getPresetByName(colormapname));

      this.lookupTable.setMappingRange(...[this.dataRange[0]*gain,this.dataRange[1]*gain]);
      this.lookupTable.updateRange();
      this.renderWindow.render();
    },
    setGain(gain){
      let newGain = parseFloat(gain);

      if(newGain < 0.0001) newGain = 0.0001;
      this.lookupTable.setMappingRange(...[this.dataRange[0]*newGain,this.dataRange[1]*newGain]);
      this.lookupTable.updateRange();
      this.renderWindow.render();

    },
    removeActor() {
      this.actor.delete();
      this.mapper.delete();
      this.renderer.resetCamera();
      this.renderWindow.render();
    },
    onUpdateVtp(dataVtp) {
      
      this.lookupTable = vtkColorTransferFunction.newInstance();
      this.lookupTable.applyColorMap(vtkColorMaps.getPresetByName(vtkColorMaps.rgbPresetNames[0]));
      this.dataRange = [Number.MAX_SAFE_INTEGER, Number.MIN_SAFE_INTEGER];
    
      this.mapper = vtkMapper.newInstance(
        {
        interpolateScalarsBeforeMapping: true,
        useLookupTableScalarRange: true,
        lookupTable: this.lookupTable,
        scalarVisibility: true,
      }
      );
      this.actor = vtkActor.newInstance();

      this.actor.setMapper(this.mapper);
      this.renderer.addActor(this.actor);

      vtkConeSource.newInstance({ height: 1.0 });
      // const coneSource = vtkConeSource.newInstance({ height: 1.0 });
      // this.mapper.setInputConnection(coneSource.getOutputPort());

      this.mapper.setInputData(dataVtp);
      // this.actor.rotateX(90);
      // this.actor.rotateZ(55);

      //get new data range
      const range = dataVtp.getPointData().getArrayByName("amplitude").getRange();
      let newDataRange = this.dataRange;
      newDataRange[0] = Math.min(range[0], this.dataRange[0]);
      newDataRange[1] = Math.max(range[1], this.dataRange[1]);
      this.lookupTable.setMappingRange(...[newDataRange[0],newDataRange[1]]);
      this.lookupTable.updateRange();

      const colorByArrayName = "amplitude";
      const colorMode = ColorMode.MAP_SCALARS;
      const scalarMode = ScalarMode.USE_POINT_FIELD_DATA;
      this.mapper.set({
        colorByArrayName,
        colorMode,
        scalarMode,
      })


      this.renderer.resetCamera();
      
      this.renderWindow.render();
    },
  },
  setup(props) {
    const context = ref(null);
    const coneResolution = ref(6);
    const representation = ref(2);

    const divWidth = ref(props.divWidthProp);
    const divHeight = ref(props.divHeightProp);
    

    const renderWindow = vtkRenderWindow.newInstance();
    const renderer     = vtkRenderer.newInstance();
    renderer.setBackground([255,255,255])

    
    function setConeResolution(res) {
      coneResolution.value = Number(res);
    }

    function setRepresentation(rep) {
      representation.value = Number(rep);
    }

    function onClick(){
      const { renderWindow } = context.value;
      divWidth.value = 100
      divHeight.value = 100
      renderWindow.getViews()[0].setSize(100, 100)
    }

    watch(() => [props.divWidthProp,props.divHeightProp], (currentValue) => {
        const { renderWindow } = context.value;
        divWidth.value = currentValue[0]
        divHeight.value = currentValue[1]
        renderWindow.getViews()[0].setSize(currentValue[0], currentValue[1])
    });

    onMounted(() => {
      
      if (!context.value) {

        const container = document.querySelector('#container');
        // VTK renderWindow/renderer
        
        renderWindow.addRenderer(renderer);

        // WebGL/OpenGL impl
        const openGLRenderWindow = vtkOpenGLRenderWindow.newInstance();
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

        
        
        
        //create orientation widget
        const axes = vtkAxesActor.newInstance();
        const orientationWidget = vtkOrientationMarkerWidget.newInstance({
          actor: axes,
          interactor: renderWindow.getInteractor(),
        });   
        orientationWidget.setEnabled(true);
        orientationWidget.setViewportCorner(
          vtkOrientationMarkerWidget.Corners.BOTTOM_RIGHT
        );
        orientationWidget.setViewportSize(0.15);
        orientationWidget.setMinPixelSize(100);
        orientationWidget.setMaxPixelSize(300); 

        context.value = {
          renderWindow
        };
      }
    });



    return {
      setRepresentation,
      setConeResolution,
      coneResolution,
      representation,
      onClick,
      divWidth,
      divHeight,
      renderWindow,
      renderer,
    };
  }
}
</script>

<style scoped>
.controls {
  position: relative;
}
</style>