<template>
  <button
    type="button"
    class="btn btn-success btn-sm"
    @click="modalShow = !modalShow"
    id="part-modal"
  >
    Dodaj nową część
  </button>
  <b-modal
    v-model="modalShow"
    ref="addPartModal"
    id="part-modal"
    title="Dodaj nową część"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group
        id="form-name-group"
        label="Nazwa:"
        label-for="form-name-input"
      >
        <b-form-input
          id="form-name-input"
          type="text"
          v-model="addPartForm.name"
          required
          placeholder="Wprowadź nazwę części"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-description-group"
        label="Opis:"
        label-for="form-description-input"
      >
        <b-form-input
          id="form-description-input"
          type="text"
          v-model="addPartForm.description"
          placeholder="Wprowadź opis części"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-price-group"
        label="Cena:"
        label-for="form-price-input"
      >
        <b-form-input
          id="form-price-input"
          type="number"
          v-model="addPartForm.price"
          min="0"
          required
          placeholder="Wprowadź cenę części"
        >
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="outline-info">Dodaj</b-button>
      <b-button type="reset" variant="outline-danger">Wyczyść</b-button>
    </b-form>
  </b-modal>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      addPartForm: {
        name: "",
        description: "",
        price: "",
      },
      message: "",
      modalShow: false,
    };
  },
  methods: {
    initForm() {
      this.addPartForm.name = "";
      this.addPartForm.description = "";
      this.addPartForm.price = "";
    },

    addPart(payload) {
      const path = "http://localhost:5000/parts";
      axios
        .post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.$emit("submit", this.message);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    onSubmit(e) {
      e.preventDefault();
      const payload = {
        name: this.addPartForm.name,
        description: this.addPartForm.description,
        price: this.addPartForm.price,
      };
      this.addPart(payload);
      this.initForm();
      this.modalShow = !this.modalShow;
    },

    onReset(e) {
      e.preventDefault();
      this.initForm();
    },
  },
};
</script>
