<template>
<div id="formContainer">
  <v-form ref="form" v-model="formValid" lazy-validation style="position:relative">
    <v-row>
      <v-col cols="8"
       >
        
        <v-combobox
        v-model="fieldName"
          label="Field Name"
          :items="existingFields"
          outlined
          dense
          placeholder="Field Name"
          required
          :menu-props="{ maxHeight: '150' }"
          :rules="[v => !!v || 'Choose the field of the well']"
        ></v-combobox>
        </v-col>

        <v-col cols="4"
      >
        <v-btn
        color="primary"
          outlined
          class="mx-2" @click="addNewChildren"
        >
          Add Wells
        </v-btn>
      </v-col>
    </v-row>
  <div v-for="(children, index) in this.childrens" :key="index">
    <v-card-title class="mt-5">Well</v-card-title>
    <v-row class="mx-2">
      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.name"
          label="Well Name"
          outlined
          dense
          placeholder="Well Name"
          hide-details
          :rules="wellRules"
          @input="enableFileInput(index)"
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.area"
          label="Area"
          outlined
          dense
          placeholder="Area"
          hide-details
          type="number"
          min="0"
          suffix="km²"
          :rules="generalRules"
        ></v-text-field>
      </v-col>
     
      <div v-if="children.location.position">
      <v-row class="mt-2 ml-3">
            <v-col
              cols="6"
            >
                  <v-text-field
                  required
                    v-model="children.location.position.lat"
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
                    v-model="children.location.position.lng"
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
          <SearchLocation v-model="children.location" :key="key" :ind="index" v-on:input="storeloc" />
        </div>
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.oilVolume"
          label="Oil Volume"
          outlined
          dense
          placeholder="Oil Volume"
          hide-details
          type="number"
          min="0"
          suffix="bar"

          :rules="[v => !!v || 'Input the oil volume']"

        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.gasVolume"
          label="Gas Volume"
          outlined
          dense
          placeholder="Gas Volume"
          hide-details
          type="number"
          min="0"
          suffix="x10 ^ 6 ft ^3 (MMCF)"

          :rules="[v => !!v || 'Input the gas volume']"
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.sourceRock"
          label="Source Rock"
          outlined
          dense
          placeholder="Source Rock"
          hide-details
          :rules="generalRules"

        ></v-text-field>
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
        required
          v-model="children.play"
          label="Play"
          outlined
          dense
          placeholder="Play"
          hide-details
          :rules="generalRules"
  
        ></v-text-field>
      </v-col>

<v-col
        cols="12"
        md="6"
      >
      
        <v-autocomplete
        required
        dense
        outlined
            v-model="children.waterDepth"
            :items="waterDepthchoose"
            label="Water Depth"
            :rules="[v => !!v || 'Choose the water depth']"

            >
         
          </v-autocomplete>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
       
        <v-autocomplete
        required
        dense
        outlined
            v-model="children.reservoir"
            :items="reserviorchoose"
            label="Reservoir"
            :rules="[v => !!v || 'Choose the reservior']"
            >
         
          </v-autocomplete>
      </v-col>

      <v-col  cols="12"
        md="6">
        <v-file-input
          :disabled="fileDisabled"
          required
          dense
          accept="image/*"
          v-model="children.imgFiles"
          color="primary"
          counter
          label="File input"
          multiple
          placeholder="Select your files"
          outlined  
          :show-size="1000"
          type="file"
          :rules="fileRules"
          @change="inputChanged(index)"
        >
          <!-- <template v-slot:selection="{ text,i }">
              <v-chip small text-color="white" color="#295671" close @click:close="remove(i, index)">
                  {{ text }}
              </v-chip>
          </template> -->
          <template v-slot:selection="{ index, text }">
            <v-chip
              v-if="index < 2"
              color="primary"
              label
              small
            >
              {{ text }}
            </v-chip>

            <span
              v-else-if="index === 2"
              class="text-overline grey--text text--darken-3 mx-2"
            >
              +{{ children.imgFiles.length - 2 }} File(s)
            </span>
          </template>
        </v-file-input>
        <!-- <div v-if="files.length">
            <h5>All files</h5>
                <v-chip :key="index" v-for="(f,index) in files" class="mr-1">
                    {{ f.name }}
                </v-chip>
            </div> -->
          <!-- @change="selectFiles(index)" -->

      </v-col>

      <v-col  cols="12"
        md="6">
         <v-btn
          type="reset"
          outlined
          color="error"
          class="mx-2" @click="deleteWell(index)"
        >
          Delete
        </v-btn>
      </v-col>
    </v-row>
    </div>
  <template>
        <v-progress-linear
          v-if="load"
          indeterminate
          color="secondary"
        ></v-progress-linear>
      </template>
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
     <div style="position: absolute; right:0; bottom:0">
      <v-snackbar
        v-model="snackbar"
        right
        :color="status"
        elevation="24"
        style="position: absolute;"
      >
        {{resultPost}}
      </v-snackbar>
      </div>
  </v-form>
</div>        

</template>

<script>
import {postDatatoDB, getDatafromDB, getDB, getListFieldWell, uploadImages} from './MapEndPoint.js';
import SearchLocation from "./SearchLocation.vue";

export default {
  components:{
    SearchLocation
  },
  data: function(){
    return{
      valid: true,
      formValid:false,
      fieldName: '',
      dialog: false,
      key: 1,
      childrens: [
          {
            name:'',
            area:0,
            latitude:'',
            longitude:'',
            oilVolume:0,
            gasVolume:0,
            waterDepth:'',
            reservoir:'',
            sourceRock:'',
            play:'',
            location: {},
        imgFiles: undefined,

            // files: undefined,
          }
        ],
        successAlert: false,
        imageDatas: [],
        tempImg: [],
        waterDepthchoose: ['Onshore (darat)', 'Offshore shallow (laut <= 200 m)', 'Offshore deep (laut > 200m)'],
        reserviorchoose: ['Sandstone', 'Carbonate'],
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
        // imgFiles: undefined,

        // Rules:[v => !!v || 'Image is required'], 
        wellRules:[v => !!v || 'Well Name is required'],
        generalRules:[v => !!v || 'Field is required'],
        load: false,

        currFiles: [],
        files: [],
        childFiles: []
    }
  },
  methods: {

    addNewChildren() {
        this.childrens.push({
          name:'',
          area:'',
          latitude:'',
          longitude:'',
          oilVolume:'',
          gasVolume:'',
          waterDepth:'',
          reservoir:'',
          sourceRock:'',
          play:'',
          location: {},
        imgFiles: undefined,

        })

        if(Object.keys(this.childrens).length > 0){
        var usedWells = this.childrens.map(a => a.name);

      const wellRule = 
       v => (usedWells.includes(v) === false) || 'Well name exist!'
        this.wellRules.push(wellRule)
      }
    },

    deleteWell(id) {
      this.wellRules.splice(id)
        this.childrens.splice(id, 1);
    },
    
    storeloc(choseLoc){
      this.childrens[choseLoc.index].latitude = choseLoc.position.lat
      this.childrens[choseLoc.index].longitude = choseLoc.position.lng
    },

    // remove (i, index) {
    //   console.log('children index', index)

    //   this.files.splice(i, 1)
    //   // this.childrens[index].imgFiles = this.files

    // },

    // inputChanged (index) {
    //   console.log('children index', index)
    //   this.files = [
    //       ...this.currFiles,
    //       ...this.files
    //   ]
    //   console.log(this.files)

    //   console.log('imgfil', this.childrens[index].imgFiles.length)
    //   var data = {id: index, imgFil: this.files}
    //   this.childFiles.append(data)
    //   console.log(this.childFiles)
    // },
    
    async submitData(){
      for (let i = 0; i < Object.keys(this.childrens).length; i++){
        this.selectFiles(this.childrens[i])
      }

      delete this.childrens.location;
      delete this.childrens.imgFiles;

      if(this.$refs.form.validate() === true){
        this.load = true;

        const data = {
        fieldName: this.fieldName,
        wells: this.childrens
        }
        var returnedStatus = await postDatatoDB(data);
        
        for (let i=0; i<this.imageDatas.length;i++){
          uploadImages(this.imageDatas[i])
      }
        if(Number.isInteger(returnedStatus)){
          var successstatusStr = String(returnedStatus)[0]
          if(successstatusStr === '2'){
            this.$refs.form.reset()
            this.status = "success"
            this.resultPost = "Successfully save data"
            this.snackbar = true
            this.successDialog = true
            this.load = false;

          }
        }else if(Array.isArray(returnedStatus)){
          var failstatusStr = String(returnedStatus[0])[0]
          if(failstatusStr === '4'){
            this.status = "error"
            this.resultPost = returnedStatus[1]
            this.snackbar = true
            this.load = false;
          }
          else{
            this.status = "error"
            this.resultPost = "Please reload & try again"
            this.snackbar = true
            this.load = false;
          }
        }
        
      }
        
    },

    selectFiles (imgArr){
      let categoryChoosen = 'showcase'
      let submitData = new FormData();
      for(let i = 0; i < imgArr.imgFiles.length; i++){
          submitData.append('files', imgArr.imgFiles[i]);
      }
      submitData.append('foldername', imgArr.name);
      submitData.append('pointer', categoryChoosen);
      this.imageDatas.push(submitData)
      
      },

    backPage(){
      this.$router.push('/map-showcase')
    },

    closeDialog(){
      this.successDialog = false
    },

    enableFileInput(index){
      const isEmpty = str => !str.trim().length;

      if(isEmpty(this.childrens[index].name)){
        this.fileDisabled = true

      }else{
        this.fileDisabled = false
      }
    }
    
  },
  async mounted(){
 
      this.existingFieldsWells = await getListFieldWell()
      this.existingFields = this.existingFieldsWells.map(a => a.fieldName);
      this.existingWells = this.existingFieldsWells.map(a => a.wellName);
      
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
    fileRules(){
      // console.log(this.childrens)
      const imguploadRules = []
      const Grule = v => !!v || 'Upload image required'
      imguploadRules.push(Grule)
      if(Object.keys(this.childrens).length > 0){
        const rule =
        v => this.existingWells.includes(v) === false || 'Input well name first!'
        imguploadRules.push(rule)
      }
      return imguploadRules

    }
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