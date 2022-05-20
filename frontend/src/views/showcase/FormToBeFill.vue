<template>
<div>
  <v-form class="multi-col-validation">
    <v-row>
      <v-col cols="8"
       >
        <v-text-field
          v-model="fieldName"
          label="Field Name"
          outlined
          dense
          placeholder="Field Name"
          hide-details
        ></v-text-field>
        </v-col>

        <v-col cols="4"
        
      >
        <v-btn
        color="primary"
          outlined
          class="mx-2" @click="addNewSection"
        >
          Add Wells
        </v-btn>
      </v-col>

    </v-row>
  <div v-for="(children) in this.childrens" :key="children">
    <v-card-title class="mt-5">Well</v-card-title>

    <v-row class="mx-2">
      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="wellName"
          label="Well Name"
          outlined
          dense
          placeholder="Well Name"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="area"
          label="Area (km2)"
          outlined
          dense
          placeholder="Area (km2)"
          hide-details
        ></v-text-field>
      </v-col>

<v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="latitude"
          label="Latitude"
          outlined
          dense
          placeholder="Latitude (Ex: -0.847199)"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="longitude"
          label="Longitude"
          outlined
          dense
          placeholder="Longitude (Ex: 117.015818)"
          hide-details
        ></v-text-field>
      </v-col>


      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="oilVolume"
          label="Oil Volume"
          outlined
          dense
          placeholder="Oil Volume"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="gasVolume"
          label="Gas Volume"
          outlined
          dense
          placeholder="Gas Volume"
          hide-details
        ></v-text-field>
      </v-col>

       <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="waterDepth"
          label="Water Depth"
          outlined
          dense
          placeholder="Water Depth"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="reservoir"
          label="Reservoir"
          outlined
          dense
          placeholder="Reservoir"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="sourceRock"
          label="Source Rock"
          outlined
          dense
          placeholder="Source Rock"
          hide-details
        ></v-text-field>
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <v-text-field
          v-model="play"
          label="Play"
          outlined
          dense
          placeholder="Play"
          hide-details
        ></v-text-field>
      </v-col>

      <v-col  cols="12"
        md="6">
        <v-file-input
          accept="image/*"
          v-model="files"
          color="primary"
          counter
          label="File input"
          multiple
          placeholder="Select your files"
          outlined
          :show-size="1000"
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
    </v-row>
    </div>

      <v-col cols="12">
        <v-btn color="primary">
          Submit
        </v-btn>
        <v-btn
          type="reset"
          outlined
          class="mx-2" @click="addNewChildren"
        >
          Reset
        </v-btn>
      </v-col>
  </v-form>
</div>
</template>

<script>
// import { ref } from '@vue/composition-api'
// import { mdiPaperclip  } from '@mdi/js'

export default {
  // setup() {
  //   fieldName = ref('')
  //   wellName = ref('')
  //   const city = ref('')
  //   const country = ref('')
  //   const company = ref('')
  //   const email = ref('')

  //   return {
  //     firstName,
  //     lastName,
  //     city,
  //     country,
  //     company,
  //     email,
  //     checkbox,
  //     // mdiPaperclip
  //   }
  // },

  data: function(){
    return{
      fieldName: '',
   
childrens: [
            {
              wellName:'',
              area:'',
              latitude:'',
              longitude:'',
              oilVolume:'',
              gasVolume:'',
              waterDepth:'',
              reservoir:'',
              sourceRock:'',
              play:'',

              files: [],
            }
        ]
    }
  },
  methods: {
        addNewChildren() {
            this.children.push({
                wellName:'',
              area:'',
              latitude:'',
              longitude:'',
              oilVolume:'',
              gasVolume:'',
              waterDepth:'',
              reservoir:'',
              sourceRock:'',
              play:'',

              files: [],
            })
        },
        
    }
}
</script>
