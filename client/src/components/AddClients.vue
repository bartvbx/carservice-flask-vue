<template>
  <button
    type="button"
    class="btn btn-success btn-sm"
    @click="modalShow = !modalShow"
    id="client-modal"
  >
    Add a new client
  </button>
  <b-modal
    v-model="modalShow"
    ref="addClientModal"
    id="client-modal"
    title="Add a new client"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group
        id="form-name-group"
        label="Client:"
        label-for="form-name-input"
      >
        <b-form-input
          id="form-name-input"
          type="text"
          v-model="addClientForm.name"
          required
          placeholder="Enter the customer name"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-car-brand-group"
        label="Brand:"
        label-for="form-car-brand-input"
      >
        <b-form-input
          id="form-car-brand-input"
          type="text"
          v-model="addClientForm.car_brand"
          required
          placeholder="Enter the brand of the car"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-car-model-group"
        label="Model:"
        label-for="form-car-model-input"
      >
        <b-form-input
          id="form-car-model-input"
          type="text"
          v-model="addClientForm.car_model"
          required
          placeholder="Enter the car model"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-contact-group"
        label="Contact:"
        label-for="form-contact-input"
      >
        <b-form-input
          id="form-contact-input"
          type="text"
          v-model="addClientForm.contact"
          required
          placeholder="Enter contact details"
        >
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="outline-info">Add</b-button>
      <b-button type="reset" variant="outline-danger">Clear</b-button>
    </b-form>
  </b-modal>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      addClientForm: {
        name: "",
        car_brand: "",
        car_model: "",
        contact: "",
      },
      message: "",
      modalShow: false,
    };
  },
  methods: {
    initForm() {
      this.addClientForm.name = "";
      this.addClientForm.car_brand = "";
      this.addClientForm.car_model = "";
      this.addClientForm.contact = "";
    },

    addClient(payload) {
      const path = "http://localhost:5000/clients";
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
        name: this.addClientForm.name,
        car_brand: this.addClientForm.car_brand,
        car_model: this.addClientForm.car_model,
        contact: this.addClientForm.contact,
      };
      this.addClient(payload);
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
