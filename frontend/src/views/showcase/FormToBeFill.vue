<template>
<div>
  <v-form ref="form" v-model="valid" lazy-validation class="multi-col-validation">
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
          label="Area (km2)"
          outlined
          dense
          placeholder="Area (km2)"
          hide-details
          type="number"
          min="0"
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
          @change="selectFiles(index)"
          :rules="fileRules"
        >
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
              +{{ files.length - 2 }} File(s)
            </span>
          </template>
        </v-file-input>
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
        // imgFiles: undefined,

//         fileRules:[
//    v => !!v || 'File is required',
//    v => (v && v.size > 0) || 'File is required',
// ], 
        wellRules:[v => !!v || 'Well Name is required'],
        generalRules:[v => !!v || 'Field is required']
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

        console.log(this.childrens)
    },

    deleteWell(id) {

        this.childrens.splice(id, 1);

        console.log(this.childrens)
    },
    
    storeloc(choseLoc){
      console.log('loc', choseLoc)
      console.log(choseLoc)
      this.childrens[choseLoc.index].latitude = choseLoc.position.lat
      this.childrens[choseLoc.index].longitude = choseLoc.position.lng
    },
    submitData(){
    
      delete this.childrens.location;
      delete this.childrens.imgFiles;


      this.$refs.form.validate()
      if(this.$refs.form.validate() === true){
        const data = {
        fieldName: this.fieldName,
        wells: this.childrens
        }
        console.log(data)
        postDatatoDB(data);

        for (let i=0; i<this.imageDatas.length;i++){
          uploadImages(this.imageDatas[i])
      }
      }
        
    },

    selectFiles (index){
      let categoryChoosen = 'showcase'
      // console.log(this.imgFiles[0])
      let submitData = new FormData();
      for(let i = 0; i < this.imgFiles.length; i++){
        console.log(this.imgFiles[i])
          submitData.append('files', this.imgFiles[i]);
      }

      submitData.append('foldername', this.childrens[index].name);
      submitData.append('pointer', categoryChoosen);
      this.imageDatas.push(submitData)
      for (var pair of submitData.entries()) {
          console.log(pair[0]+ ', ' + pair[1]); 
      }
      },

    backPage(){
      this.$router.push('/map-showcase')
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
            console.log(this.existingFieldsWells)

      this.existingFields = this.existingFieldsWells.map(a => a.fieldName);
      this.existingWells = this.existingFieldsWells.map(a => a.wellName);
      
         this.exD = getDatafromDB()
         console.log(this.exD)
       this.ex = getDB()
         console.log(this.ex)

         if(this.existingWells){
        const rule =
        v => (this.existingWells.includes(v) === false) || 'Well name exist!'
        this.wellRules.push(rule)

      }

  },
  computed:{
    fileRules(){
      console.log(this.childrens)
      const fileRules = []
      if(this.childrens.length > 0){
        const rule =
        v => (this.existingWells.includes(v) === false) || 'Well name exist!'
        fileRules.push(rule)
      }
      return fileRules

    }
  },
  }
</script>
