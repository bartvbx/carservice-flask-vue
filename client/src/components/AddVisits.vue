<template>
  <button
    type="button"
    class="btn btn-success btn-sm"
    @click="modalShow = !modalShow"
    id="visit-modal"
  >
    Add a new visit
  </button>
  <b-modal
    v-model="modalShow"
    ref="addVisitModal"
    id="visit-modal"
    title="Add a new visit"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group
        id="form-client-group"
        label="Client:"
        label-for="form-client-input"
      >
        <VueMultiselect
          v-model="addVisitForm.client"
          :options="clients"
          label="name"
          track-by="name"
          placeholder="Select client"
          selectLabel="Press enter to select"
          selectedLabel="Selected"
          deselectLabel="Press enter to deselect"
          required
        >
        </VueMultiselect>
        or
        <br />
        <add-clients @submit="afterAddingClient"></add-clients>
      </b-form-group>

      <b-form-group
        id="form-visit-services-group"
        label="Services:"
        label-for="form-visit-services-input"
      >
        <VueMultiselect
          v-model="addVisitForm.services"
          :options="services"
          :multiple="true"
          label="name"
          track-by="name"
          placeholder="Select services"
          selectLabel="Press enter to select"
          selectedLabel="Selected"
          deselectLabel="Press enter to deselect"
        >
        </VueMultiselect>
      </b-form-group>

      <b-form-group
        id="form-date-group"
        label="Date:"
        label-for="form-date-input"
      >
        <Datepicker
          v-model="addVisitForm.date"
          required
          placeholder="Enter the date"
        ></Datepicker>
      </b-form-group>

      <b-form-group
        id="form-description-group"
        label="Additional information:"
        label-for="form-description-input"
      >
        <b-form-input
          id="form-description-input"
          type="text"
          v-model="addVisitForm.description"
          placeholder="Enter additional information"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-discount-group"
        label="Discount:"
        label-for="form-discount-input"
      >
        <b-form-input
          id="form-discount-input"
          type="number"
          min="0"
          max="100"
          v-model="addVisitForm.discount"
          placeholder="Enter the discount value (%)"
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
import VueMultiselect from "vue-multiselect";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import AddClients from "./AddClients.vue";
export default {
  components: { VueMultiselect, Datepicker, AddClients },
  data() {
    return {
      services: [],
      clients: [],
      addVisitForm: {
        state: "",
        date: "",
        description: "",
        services: [],
        client: [],
        discount: 0,
      },
      message: "",
      modalShow: false,
    };
  },
  methods: {
    initForm() {
      this.addVisitForm.state = "";
      this.addVisitForm.date = "";
      this.addVisitForm.description = "";
      this.addVisitForm.services = [];
      this.addVisitForm.client = [];
      this.addVisitForm.discount = 0;
    },

    getServices() {
      const path = "http://localhost:5000/services";
      axios
        .get(path)
        .then((res) => {
          this.services = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    getClients() {
      const path = "http://localhost:5000/clients";
      axios
        .get(path)
        .then((res) => {
          this.clients = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    addVisit(payload) {
      const path = "http://localhost:5000/visits";
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

    getNewestClient() {
      const path = "http://localhost:5000/clients/new";
      axios
        .get(path)
        .then((res) => {
          this.addVisitForm.client = res.data.client;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    afterAddingClient() {
      this.getClients();
      this.getNewestClient()
    },

    onSubmit(e) {
      e.preventDefault();
      const payload = {
        name: this.addVisitForm.name,
        date: this.addVisitForm.date,
        description: this.addVisitForm.description,
        services: this.addVisitForm.services,
        client: this.addVisitForm.client,
        discount: this.addVisitForm.discount,
      };
      this.addVisit(payload);
      this.initForm();
      this.modalShow = !this.modalShow;
    },

    onReset(e) {
      e.preventDefault();
      this.initForm();
    },
  },
  created() {
    this.getServices();
    this.getClients();
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
