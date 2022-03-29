<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="text-h5">
          {{ title }}
        </v-card-title>
        <v-card-text> {{ text }} </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            text
            @click="confirmDialog(false)"
          >
            Discard
          </v-btn>
          <v-btn
            color="success"
            text
            @click="confirmDialog(true)"
            data-testid="dialog-confirm"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
    name: 'card-confirm',
    data() {
        return {
            dialog: true,
        }
    },
    props: {
        title: String,
        text: String
    },
    emits: ['confirmdialog'],
    methods: {
        confirmDialog(bool) {
            this.$emit('confirmdialog', bool)
            this.dialog = false
        }
    }
}
</script>