<template>
  <button
    type="button"
    class="btn btn-success btn-sm"
    @click="modalShow = !modalShow"
    id="service-modal"
  >
    Add a new service
  </button>
  <b-modal
    v-model="modalShow"
    ref="addServiceModal"
    id="service-modal"
    title="Add a new service"
    hide-footer
  >
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group
        id="form-name-group"
        label="Name:"
        label-for="form-name-input"
      >
        <b-form-input
          id="form-name-input"
          type="text"
          v-model="addServiceForm.name"
          required
          placeholder="Enter the service name"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-description-group"
        label="Description:"
        label-for="form-description-input"
      >
        <b-form-input
          id="form-description-input"
          type="text"
          v-model="addServiceForm.description"
          placeholder="Enter a description of the service"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
        id="form-service-parts-group"
        label="Parts:"
        label-for="form-service-parts-input"
      >
        <VueMultiselect
          v-model="addServiceForm.parts"
          :options="parts"
          :multiple="true"
          label="name"
          track-by="name"
          placeholder="Select parts"
          selectLabel="Press enter to select"
          selectedLabel="Selected"
          deselectLabel="Press enter to deselect"
        >
        </VueMultiselect>
      </b-form-group>

      <b-form-group
        id="form-price-group"
        label="Labour price:"
        label-for="form-price-input"
      >
        <b-form-input
          id="form-price-input"
          type="number"
          v-model="addServiceForm.labour_price"
          min="0"
          required
          placeholder="Enter the price of the service"
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
export default {
  components: { VueMultiselect },
  data() {
    return {
      parts: [],
      addServiceForm: {
        name: "",
        description: "",
        parts: [],
        labour_price: 0,
      },
      message: "",
      modalShow: false,
    };
  },
  methods: {
    initForm() {
      this.addServiceForm.name = "";
      this.addServiceForm.description = "";
      this.addServiceForm.parts = [];
      this.addServiceForm.price = 0;
    },

    getParts() {
      const path = "http://localhost:5000/parts";
      axios
        .get(path)
        .then((res) => {
          this.parts = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    addService(payload) {
      const path = "http://localhost:5000/services";
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
        name: this.addServiceForm.name,
        description: this.addServiceForm.description,
        parts: this.addServiceForm.parts,
        labour_price: this.addServiceForm.labour_price,
      };
      this.addService(payload);
      this.initForm();
      this.modalShow = !this.modalShow;
    },

    onReset(e) {
      e.preventDefault();
      this.initForm();
    },
  },
  created() {
    this.getParts();
  },
};
</script>
