<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <hr />
          <p>Service list</p>
          <hr />
          <br />

          <b-alert variant="success" v-if="showMessage" show dismissible>
            {{ message }}
          </b-alert>

          <add-services @submit="afterSubmit"></add-services>
          <br />
          <br />

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Description</th>
                <th scope="col">Parts</th>
                <th scope="col">Parts price</th>
                <th scope="col">Labour price</th>
                <th scope="col">Total price</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service, index) in services" :key="index">
                <td>{{ service.name }}</td>
                <td>{{ service.description }}</td>
                <td>
                  <text
                    v-for="(service_parts, index) in service.parts"
                    :key="index"
                    >{{ service_parts.name }}
                    <span
                      v-if="
                        index != Object.keys(service.parts).length - 1
                      "
                      >,
                    </span>
                  </text>
                </td>
                <td>{{ service.parts_price }}</td>
                <td>{{ service.labour_price }}</td>
                <td>{{ service.total_price }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      id="service-update-modal"
                      @click="
                        editService(service);
                        modalShow = !modalShow;
                      "
                    >
                      Update
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteService(service)"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <b-modal
        v-model="modalShow"
        ref="editServiceModal"
        id="service-update-modal"
        title="Update service"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-name-edit-group"
            label="Name:"
            label-for="form-name-edit-input"
          >
            <b-form-input
              id="form-name-edit-input"
              type="text"
              v-model="editForm.name"
              required
              placeholder="Enter the service name"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-description-edit-group"
            label="Description:"
            label-for="form-description-edit-input"
          >
            <b-form-input
              id="form-description-edit-input"
              type="text"
              v-model="editForm.description"
              placeholder="Enter a description of the service"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-service-parts-edit-group"
            label="Parts:"
            label-for="form-service-parts-edit-input"
          >
            <VueMultiselect
              v-model="editForm.parts"
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
            id="form-price-edit-group"
            label="Labour price:"
            label-for="form-price-edit-input"
          >
            <b-form-input
              id="form-price-edit-input"
              type="number"
              v-model="editForm.labour_price"
              min="0"
              required
              placeholder="Enter the price of the service"
            >
            </b-form-input>
          </b-form-group>

          <b-button type="submit" variant="outline-info">Update</b-button>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueMultiselect from "vue-multiselect";
import AddServices from "./AddServices.vue";
export default {
  components: { VueMultiselect, AddServices },
  data() {
    return {
      services: [],
      parts: [],
      editForm: {
        id: "",
        name: "",
        description: "",
        parts: [],
        labour_price: 0,
      },
      message: "",
      showMessage: false,
      modalShow: false,
    };
  },
  methods: {
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

    afterSubmit(message) {
      this.message = message;
      this.showMessage = true;
      this.getServices();
      setTimeout(() => {
        this.showMessage = false;
      }, 4000);
    },

    initForm() {
      this.editForm.id = "";
      this.editForm.name = "";
      this.editForm.description = "";
      this.editForm.parts = [];
      this.editForm.labour_price = 0;
    },

    updateService(payload, serviceID) {
      const path = `http://localhost:5000/services/${serviceID}`;
      axios
        .put(path, payload)
        .then((res) => {
          this.getServices();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getServices();
        });
    },

    editService(service) {
      this.editForm = service;
    },

    onSubmitUpdate(e) {
      e.preventDefault();
      const payload = {
        name: this.editForm.name,
        description: this.editForm.description,
        parts: this.editForm.parts,
        labour_price: this.editForm.labour_price,
      };
      this.updateService(payload, this.editForm.id);
      this.modalShow = !this.modalShow;
    },

    removeService(ServiceID) {
      const path = `http://localhost:5000/services/${ServiceID}`;
      axios
        .delete(path)
        .then((res) => {
          this.getServices();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getServices();
        });
    },

    deleteService(service) {
      this.removeService(service.id);
    },
  },
  created() {
    this.getServices();
    this.getParts();
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
