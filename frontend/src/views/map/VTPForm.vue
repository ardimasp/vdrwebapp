<template>
<div id="formContainer">
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
          label="Radius (m)"
          outlined
          dense
          placeholder="Radius (m)"
          hide-details
          type="number"
          min="0"
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
          :rules="generalRules"
        ></v-text-field>
      </v-col>
              <!-- <v-row> -->
    </v-row>
        <!-- <v-row v-for="n in latlngTotal" :key="n">
     <v-col cols="6"
        > <v-text-field
                  required
                    v-model="latArray[n]"
                    label="Latitude"
                    outlined
                    dense
                    placeholder="Latitude (Ex: -0.847199)"
                    hide-details
                    :rules="generalRules"
                  ></v-text-field>
        </v-col>
        <v-col  cols="6"
        > <v-text-field
                  required
                    v-model="lngArray[n]"
                    label="Longitude"
                    outlined
                    dense
                    placeholder="Longitude (Ex: 117.015818)"
                    hide-details
                    :rules="generalRules"
                  ></v-text-field>
        </v-col>
            </v-row> -->

      <!-- </div> -->
              <!-- </v-row> -->

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
          <!-- @change="selectFiles(index)" -->

      </v-col>

      <!-- <v-col  cols="12"
        md="6">
         <v-btn
          type="reset"
          outlined
          color="error"
          class="mx-2" @click="deleteWell(index)"
        >
          Delete
        </v-btn>
      </v-col> -->
    </v-row>

      <v-col cols="12">
        <v-btn color="primary" :disabled="!valid" @click="submitData">
          Submit
        </v-btn>
        <v-btn
          type="reset"
          outlined
          class="mx-2" 
          @click="backPage"
        >
          BACK
        </v-btn>
      </v-col>
      <!-- <v-alert type="success" :value="successAlert">
        Successfully save data
      </v-alert> -->
      <v-snackbar
        v-model="snackbar"
        :timeout="timeout"
        right
        :color="status"
        elevation="24"
      >
        {{resultPost}}
      </v-snackbar>
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
</div>        

</template>

<script>
import {getDatafromDB, getDB, getListFieldWell, vtpUpload,vtpInfo} from '../showcase/MapEndPoint.js';
import SearchLocation from "../showcase/SearchLocation.vue";
// import {rectangleLatlng} from './RotateBoundary.js';

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
        tempImg: [],
        existingFieldsWells: null,
        existingFields: null,
        existingWells: null,
        exD: null,
        selectedFiles: undefined,
        selectedImages: undefined,
        fileDisabled: true,
        snackbar:false,
        timeout:5000,
        status:"info",
        resultPost:"",
        successDialog:false,
        vtpType: ['well-vtp','line-vtp','surface-vtp'],
        latlngTotal: 1,
        latArray: [],
        lngArray: [],
        // category:[],
        location: {},
        returnedStatus: undefined,
        returnedStatusUpload:undefined,
        // imgFiles: undefined,

        // Rules:[v => !!v || 'Image is required'], 
        wellRules:[v => !!v || 'Well Name is required'],
        generalRules:[v => !!v || 'Field is required']
    }
  },
  methods: {
    
    storeloc(choseLoc){
      console.log('loc', choseLoc)
      console.log(choseLoc)
      // this.childrens[choseLoc.index].latitude = choseLoc.position.lat
      // this.childrens[choseLoc.index].longitude = choseLoc.position.lng
    },
    angleToRadians(angle)
    {
      return (Math.PI / 180) * angle;
    },
    async submitData(){
      // for (let i = 0; i < Object.keys(this.childrens).length; i++){
      //   this.selectFiles(this.childrens[i])
      // }

      // delete this.childrens.location;
      // delete this.childrens.imgFiles;

      console.log('chosen well', this.wellName),
      console.log('chosen vtp type',  this.vtptypeChosen)
      console.log('chosen tilt angle',  this.tilt)
            console.log('chosen long',  this.long)
      console.log('location', this.location.position.lat, this.location.position.lng)
      console.log('vtp file chosen', this.vtpfilename)
      var fileVTP = this.selectFiles(this.vtpFiles, this.vtptypeChosen, this.wellName)
      this.returnedStatusUpload = await vtpUpload(fileVTP)
      console.log('returnedStatusUpload', this.returnedStatusUpload)
       
      console.log(this.$refs.form.validate())
      if(this.$refs.form.validate() === true){

      if(this.vtptypeChosen == this.vtpType[1]){
        let x = this.location.position.lat + (this.long/1000) * Math.cos(this.angleToRadians(this.tilt));
        let y = this.location.position.lng + (this.long/1000) * Math.sin(this.angleToRadians(this.tilt));
        console.log([x,y])
        const data = {
        path: '/'+this.wellName+'/'+this.vtpfilename,
        type: this.vtptypeChosen,
        center: [this.location.position.lat, this.location.position.lng],
        geodata: [[this.location.position.lat, this.location.position.lng], [x,y]],
        tilt: this.tilt
        }
        this.returnedStatus = await vtpInfo(data);

      }else if(this.vtptypeChosen == this.vtpType[2]){
        let x = (this.location.position.lat - (0.5*this.surfaceWidth))
        let y = (this.location.position.lng - (0.5*this.surfaceLength))
        console.log([x,y])
        const data = {
          path: '/'+this.wellName+'/'+this.vtpfilename,
          type: this.vtptypeChosen,
          center: [this.location.position.lat, this.location.position.lng],
          geodata: [[this.location.position.lat, this.location.position.lng], [x,y]],
          tilt: this.tilt
        }
        this.returnedStatus = await vtpInfo(data);

        //  let z = (this.location.position.lat + (0.5*this.surfaceWidth))
        // let a = (this.location.position.lng + (0.5*this.surfaceLength))

        // var pointlist = [];   

        // var p1 = [z, y];
        // pointlist.push(p1);
        // var p2 = [z, a];
        // pointlist.push(p2);
        // var p3 = [z, y];
        // pointlist.push(p3);
        // var p4 = [x,a];
        // pointlist.push(p4);    
        // let recLatlng = rectangleLatlng(x, y, this.surfaceWidth, this.tilt)

      //   const res = []
			// const angle = this.tilt * (Math.PI / 180)
			// 		for (let i = 0; i < pointlist.length; i++) {
			// 				const p = pointlist[i]
			// 				// translate to center
			// 				const p2 = [p[0] - this.location.position.lat, p[1] - this.location.position.lng]
			// 				// rotate using matrix rotation
			// 				const p3 =  [Math.cos(angle) * p2[0] - Math.sin(angle) * p2[1], Math.sin(angle) * p2[0] + Math.cos(angle) * p2[1]]
			// 				// translate back to center
			// 				let p4 = [p3[0] + this.location.position.lat, p3[1] + this.location.position.lng]
			// 				// done with that point
			// 				// p4 = map.layerPointToLatLng(p4)
			// 				res.push(p4)
			// 		}

        // console.log(res)
      }
      else if(this.vtptypeChosen == this.vtpType[0]){
        const data = {
          path: '/'+this.wellName+'/'+this.vtpfilename,
          type: this.vtptypeChosen,
          center: [this.location.position.lat, this.location.position.lng],
          radius:this.radius
        }
        this.returnedStatus = await vtpInfo(data);

      }
      // if(this.$refs.form.validate() === true){
      //   const data = {
      //   fieldName: this.fieldName,
      //   wells: this.childrens
      //   }
      //   console.log(data)
      //   var returnedStatus = await postDatatoDB(data);
        
      //   for (let i=0; i<this.imageDatas.length;i++){
      //     uploadImages(this.imageDatas[i])
      // }
        if(Number.isInteger(this.returnedStatus)){
          var successstatusStr = String(this.returnedStatus)[0]
          if(successstatusStr === '2'){
            this.$refs.form.reset()
            this.status = "success"
            this.resultPost = "Successfully save data"
            this.snackbar = true
            this.successDialog = true
          }
        }else if(Array.isArray(this.returnedStatus)){
          var failstatusStr = String(this.returnedStatus[0])[0]
          if(failstatusStr === '4'){
            this.$refs.form.reset()
            this.status = "error"
            this.resultPost = this.returnedStatus[1]
            this.snackbar = true
            // this.successDialog = true
          }
          else{
            this.$refs.form.reset()
            this.status = "error"
            this.resultPost = "Please reload & try again"
            this.snackbar = true
            // this.successDialog = true
          }
        }
        
      }
        
    },
    findFileName(){
      //  var fileData =   e.target.files;
      this.vtpfilename=this.vtpFiles.name;
      console.log(this.vtpfilename)
    },

    selectFiles (vtpFiles, vtpType, wellName){
      // let categoryChoosen = 'showcase'
      let submitData = new FormData();
      // for(let i = 0; i < imgArr.imgFiles.length; i++){
        // console.log(imgArr.imgFiles[i])
          submitData.append('file', vtpFiles);
      // }
      submitData.append('foldername', wellName);
      submitData.append('pointer', vtpType);
      console.log(submitData)
      return(submitData)
      // this.finalVTPfile = submitData
      // this.imageDatas.push(submitData)
      
      },


    backPage(){
      this.$router.push('/maps')
    },

    closeDialog(){
      this.successDialog = false
    },

    enableFileInput(){
      const isEmpty = str => !str.trim().length;

      if(isEmpty(this.wellName)){
        this.fileDisabled = true

      }else{
        this.fileDisabled = false
        console.log(this.wellName)
      
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
 
      this.existingFieldsWells = await getListFieldWell()
            console.log(this.existingFieldsWells)

      this.existingFields = this.existingFieldsWells.map(a => a.fieldName);
      this.existingWells = this.existingFieldsWells.map(a => a.wellName);
      
         this.exD = getDatafromDB()
         console.log(this.exD)
       this.ex = getDB()
         console.log(this.ex)

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