<template>
<div id="formContainer">
  <template>
        <v-progress-linear
          v-if="load"
          indeterminate
          color="secondary"
        ></v-progress-linear>
      </template>
  <v-form ref="form" v-model="formValid" lazy-validation>
    <v-row>
      <v-col class="mt-2" cols="12"
       >
        
        <v-combobox
        v-model="wellName"
          label="Select Well"
          :items="existingWells"
          outlined
          dense
          placeholder="Well Name"
          required
          :menu-props="{ maxHeight: '150' }"
          :rules="[v => !!v || 'Choose the well for VTP']"
          @change="enableFileInput"
        ></v-combobox>
        </v-col>

    </v-row>

    <v-row >
      <v-col
        cols="12"
        md="6"
      >

        <v-select
        v-model="vtptypeChosen"
          label="Select VTP Type"
          :items="vtpType"
          outlined
          dense
          placeholder="VTP Type"
          required
          :menu-props="{ maxHeight: '100' }"
          :rules="[v => !!v || 'Choose the VTP type']"
          style="z-index: 8;"
          @change="latlngRequired"

        ></v-select>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field v-if="vtptypeChosen==vtpType[0]"
        required
          v-model="radius"
          label="Radius"
          outlined
          dense
          placeholder="Radius"
          hide-details
          type="number"
          min="0"
          suffix="m"
          :rules="generalRules"
        ></v-text-field>
         <v-text-field v-if="vtptypeChosen==vtpType[1] ||vtptypeChosen==vtpType[2] "
        required
          v-model="tilt"
          label="Tilt Angle"
          outlined
          dense
          placeholder="Tilt Angle"
          hide-details
          type="number"
          min="0"
          suffix="°"
          :rules="generalRules"
        ></v-text-field>
      </v-col>
    </v-row>

      <div v-if="location.position">
      <v-row class="mt-2">
            <v-col
              cols="6"
            >
                  <v-text-field
                  required
                    v-model="location.position.lat"
                    label="Latitude"
                    outlined
                    dense
                    placeholder="Latitude (Ex: -0.847199)"
                    hide-details
                    :rules="generalRules"
                  ></v-text-field>
              
            </v-col>

            <v-col
              cols="6"
            >

                  <v-text-field
                  required
                    v-model="location.position.lng"
                    label="Longitude"
                    outlined
                    dense
                    placeholder="Longitude (Ex: 117.015818)"
                    hide-details
                    :rules="generalRules"

                  ></v-text-field>
            </v-col>
      </v-row>
      </div>
      <div v-else>
        <br>
        <h4 class="ml-3">Please choose the location of the Well by double tapping on a location on the map, drag and place the marker or use the search tool on the top left</h4>
      </div>

      <v-col
              cols="12"
              md="12"
            >
        <div style="width:100%;height: 500px">
          <SearchLocation v-model="location" :key="1" :ind="1" v-on:input="storeloc" />
        </div>
      </v-col>
      <v-row>
      <v-col class="mt-2" cols="12"
        md="6">
       <v-text-field v-if="vtptypeChosen==vtpType[2]"
        required
          v-model="surfaceLength"
          label="Length"
          outlined
          dense
          placeholder="Length"
          hide-details
          type="number"
          min="0"
          suffix="m"
          :rules="generalRules"
        ></v-text-field>
      </v-col>
      <v-col class="mt-2" cols="12"
        md="6">
       <v-text-field v-if="vtptypeChosen==vtpType[2]"
        required
          v-model="surfaceWidth"
          label="Width"
          outlined
          dense
          placeholder="Width"
          hide-details
          type="number"
          suffix="m"
          min="0"
          :rules="generalRules"
        ></v-text-field>
      </v-col>
      <v-col  cols="12"
        md="6">
       <v-text-field v-if="vtptypeChosen==vtpType[1]"
        required
          v-model="long"
          label="Long"
          outlined
          dense
          placeholder="Long"
          hide-details
          type="number"
          min="0"
          suffix="m"
          :rules="generalRules"
        ></v-text-field>
      </v-col>
    </v-row>
     <v-row>
      <v-col  cols="12"
        md="6">
        <v-file-input
        :disabled="fileDisabled"
        required
        dense
          accept="vtp/*"
          v-model="vtpFiles"
          color="primary"
          counter
          label="File input"
          placeholder="Select your files"
          outlined  
          :show-size="1000"
          type="file"
          @change="findFileName"
        >
         
        </v-file-input>
      </v-col>

    </v-row>

      <v-col cols="12">
        <v-btn
          type="reset"
          outlined
          class="mx-2" 
          @click="backPage"
        >
          BACK
        </v-btn>
        <v-btn color="primary" :disabled="!valid" @click="submitData">
          Submit
        </v-btn>
      </v-col>
      <!-- <v-alert type="success" :value="successAlert">
        Successfully save data
      </v-alert> -->
     
      <v-dialog
      v-model="successDialog"
      max-width="350"
    >
      <v-card>
          <v-card-title>  Do you want to add more data?</v-card-title>
          
          <v-card-text>
          No to go back to data showcase page.
          <br/> Yes to continue adding more data.          
          </v-card-text>
          
          <v-card-actions class="dense">
            <v-spacer></v-spacer>

            <v-btn
              text
              color="primary"
              large
              @click="backPage"

            >
              No
            </v-btn>
            <v-btn
              text
              color="primary"
              large
              @click="closeDialog"

            >
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
  </v-form>
  <div style="position: absolute; right:0; bottom:0">
      <v-snackbar
        v-model="snackbar"
        right
        :timeout="timeout"
        :color="status"
        elevation="24"
        style="position: absolute;"
      >
        {{resultPost}}
      </v-snackbar>
      </div>
</div>        

</template>

<script>
import {getDatafromDB, getDB, getVTPdata, vtpUpload,vtpInfo} from '../showcase/MapEndPoint.js';
import SearchLocation from "../showcase/SearchLocation.vue";
// import {rectangleLatlng} from './RotateBoundary.js';
import store from "../../store";

export default {
  components:{
    SearchLocation
  },
  data: function(){
    return{
      valid: true,
      formValid:false,
      wellName: '',
      dialog: false,
      key: 1,
      path:'',
      vtptypeChosen:'',
      center:[],
      tilt:'',
      long:'',
      surfaceWidth:'',
      surfaceLength:'',
      radius: '',
      vtpFiles: undefined,
      vtpfilename: '',
     
        successAlert: false,
        imageDatas: [],
        existingFieldsWells: null,
        existingFields: null,
        existingWells: null,
        exD: null,
        fileDisabled: true,
        snackbar:false,
        timeout:5000,
        status:"info",
        resultPost:"",
        successDialog:false,
        vtpType: ['well-vtp','line-vtp','surface-vtp'],
        
        location: {},
        returnedStatus: undefined,
        returnedStatusUpload:undefined,

        wellRules:[v => !!v || 'Well Name is required'],
        generalRules:[v => !!v || 'Field is required'],
        load: false,

    }
  },
  methods: {
    
    // storeloc(choseLoc){
    //   console.log('loc', choseLoc)
    //   console.log(choseLoc)
    // },
    angleToRadians(angle)
    {
      return (Math.PI / 180) * angle;
    },
    async submitData(){
       
      if(this.$refs.form.validate() === true){
      this.load = true;

      var fileVTP = this.selectFiles(this.vtpFiles, this.vtptypeChosen, this.wellName)
      this.returnedStatusUpload = await vtpUpload(fileVTP)

      if(this.vtptypeChosen == this.vtpType[1]){
        let rx = this.location.position.lat + ((this.long/2)/110.574) * Math.cos(this.angleToRadians(this.tilt));
        let ry = this.location.position.lng + ((this.long/2)/110.574) * Math.sin(this.angleToRadians(this.tilt));
        let lx = this.location.position.lat - ((this.long/2)/110.574) * Math.cos(this.angleToRadians(this.tilt));
        let ly = this.location.position.lng - ((this.long/2)/110.574) * Math.sin(this.angleToRadians(this.tilt));
        const data = {
        path: '/'+this.wellName+'/'+this.vtpfilename,
        type: this.vtptypeChosen,
        center: [this.location.position.lat, this.location.position.lng],
        geodata: [[rx, ry], [lx,ly]],
        tilt: this.tilt
        }
        this.returnedStatus = await vtpInfo(data);
        await store.dispatch("fetchVtpList")

      }else if(this.vtptypeChosen == this.vtpType[2]){
      
        let ne_lat = this.location.position.lat + ((this.surfaceWidth/2)/110.574)
        let ne_lon =  this.location.position.lng - ((this.surfaceLength/2)/(111.320 * Math.cos(this.angleToRadians((this.surfaceWidth/2)/110574))))
        let sw_lat = this.location.position.lat - ((this.surfaceWidth/2)/110.574)
        let sw_lon = this.location.position.lng + ((this.surfaceLength/2)/(111.320 *  Math.cos(this.angleToRadians((this.surfaceWidth/2)/110574))))

        var pointlist = [];   
        var p1 = [sw_lat, ne_lon];
        pointlist.push(p1);
        var p2 = [ne_lat, ne_lon];
        pointlist.push(p2);
        var p3 = [ne_lat, sw_lon];
        pointlist.push(p3);
        var p4 = [sw_lat, sw_lon];
        pointlist.push(p4);    
        const res = []
        const angle = this.tilt * (Math.PI / 180)

        for (let i = 0; i < pointlist.length; i++) {
            const p = pointlist[i]
            // translate to center
            const p2 = [p[0] - this.location.position.lat, p[1] - this.location.position.lng]
            // rotate using matrix rotation
            const p3 =  [Math.cos(angle) * p2[0] - Math.sin(angle) * p2[1], Math.sin(angle) * p2[0] + Math.cos(angle) * p2[1]]
            // translate back to center
            let p4 = [p3[0] + this.location.position.lat, p3[1] + this.location.position.lng]
            // done with that point
            // p4 = map.layerPointToLatLng(p4)
            res.push(p4)
        }
          const data = {
          path: '/'+this.wellName+'/'+this.vtpfilename,
          type: this.vtptypeChosen,
          center: [this.location.position.lat, this.location.position.lng],
          geodata: res,
          tilt: this.tilt
        }
        this.returnedStatus = await vtpInfo(data);
        await store.dispatch("fetchVtpList")
      }
      else if(this.vtptypeChosen == this.vtpType[0]){
        const data = {
          path: '/'+this.wellName+'/'+this.vtpfilename,
          type: this.vtptypeChosen,
          center: [this.location.position.lat, this.location.position.lng],
          radius:this.radius
        }
        this.returnedStatus = await vtpInfo(data);
        await store.dispatch("fetchVtpList")
      }
     
        if(Number.isInteger(this.returnedStatus)){
          var successstatusStr = String(this.returnedStatus)[0]
          if(successstatusStr === '2'){
            this.$refs.form.reset()
            this.status = "success"
            this.resultPost = "Successfully save data"
            this.snackbar = true
            this.successDialog = true
            this.load = false;

          }
        }else if(Array.isArray(this.returnedStatus)){
          var failstatusStr = String(this.returnedStatus[0])[0]
          if(failstatusStr === '4'){
            this.$refs.form.reset()
            this.status = "error"
            this.resultPost = this.returnedStatus[1]
            this.snackbar = true
            this.load = false;

            // this.successDialog = true
          }
          else{
            this.$refs.form.reset()
            this.status = "error"
            this.resultPost = "Please reload & try again"
            this.snackbar = true
            this.load = false;

            // this.successDialog = true
          }
        }
        
      }else{
        this.value = false
      }
        
    },
    findFileName(){
      this.vtpfilename=this.vtpFiles.name;
    },

    selectFiles (vtpFiles, vtpType, wellName){
      let submitData = new FormData();
      submitData.append('file', vtpFiles);
      submitData.append('foldername', wellName);
      submitData.append('pointer', vtpType);
      return(submitData)
      },


    backPage(){
      this.$router.push('/maps')
    },

    closeDialog(){
      this.$router.go(this.$router.currentRoute)
      this.successDialog = false
    },

    enableFileInput(){
      const isEmpty = str => !str.trim().length;

      if(isEmpty(this.wellName)){
        this.fileDisabled = true

      }else{
        this.fileDisabled = false      
      }

    },
    latlngRequired(){
      const isEmpty = str => !str.trim().length;
    if(!isEmpty(this.wellName)){
            
    if(this.category == this.vtpType[0]){
            this.latlngTotal = 1
          }else if(this.category == this.vtpType[1]){
            this.latlngTotal = 2
          }else if(this.category == this.vtpType[2]){
            this.latlngTotal = 4
          }}
    }    
  },
  async mounted(){
 
      this.existingFieldsWells = await getVTPdata()

      this.existingFields = this.existingFieldsWells.map(a => a.fieldName);
      this.existingWells = this.existingFieldsWells.map(a => a.name);

         this.exD = getDatafromDB()
       this.ex = getDB()

         if(this.existingWells){
        const rule =
        v => (this.existingWells.includes(v) === false) || "Well name exist!"
        this.wellRules.push(rule)

      }

  },
  computed:{
    // wellRule(){
    //   if(Object.keys(this.childrens).length > 0){
    //     var usedWells = this.childrens.map(a => a.wellName);

    //   const wellRule = 
    //    v => (usedWells.includes(v) === false) || 'Well name exist!'
    //     this.wellRules.push(wellRule)
    //   }
    // },
    // fileRules(){
    //   // console.log(this.childrens)
    //   const imguploadRules = []
    //   const Grule = v => !!v || 'Upload image required'
    //   imguploadRules.push(Grule)
    //   if(Object.keys(this.childrens).length > 0){
    //     const rule =
    //     v => this.existingWells.includes(v) === false || 'Input well name first!'
    //     imguploadRules.push(rule)
    //   }
    //   return imguploadRules

    // }
  },
  }
</script>

<style lang="css" scoped>
.formContainer {
  position: fixed;
  left: 0px;
  top: 0px;
  z-index: 1;
}

.match-height[data-v-4722cb3d] {
    margin-top: 0px;
}

h4 {
  color: green;
}
</style>