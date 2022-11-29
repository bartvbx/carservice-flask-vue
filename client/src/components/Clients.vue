<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <hr />
          <p>Client list</p>
          <hr />
          <br />

          <b-alert variant="success" v-if="showMessage" show dismissible>
            {{ message }}
          </b-alert>

          <add-clients @submit="afterSubmit"></add-clients>
          <br />
          <br />

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Client</th>
                <th scope="col">Brand</th>
                <th scope="col">Model</th>
                <th scope="col">Contact</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(client, index) in clients" :key="index">
                <td>{{ client.name }}</td>
                <td>{{ client.car_brand }}</td>
                <td>{{ client.car_model }}</td>
                <td>{{ client.contact }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      id="client-update-modal"
                      @click="
                        editClient(client);
                        modalShow = !modalShow;
                      "
                    >
                      Update
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteClient(client)"
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
        ref="editClientModal"
        id="client-update-modal"
        title="Update client"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-name-edit-group"
            label="Client:"
            label-for="form-name-edit-input"
          >
            <b-form-input
              id="form-name-edit-input"
              type="text"
              v-model="editForm.name"
              required
              placeholder="Enter the customer name"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-car-brand-edit-group"
            label="Brand:"
            label-for="form-car-brand-edit-input"
          >
            <b-form-input
              id="form-car-brand-edit-input"
              type="text"
              v-model="editForm.car_brand"
              required
              placeholder="Enter the brand of the car"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-car-model-edit-group"
            label="Model:"
            label-for="form-car-model-edit-input"
          >
            <b-form-input
              id="form-car-model-edit-input"
              type="text"
              v-model="editForm.car_model"
              required
              placeholder="Enter the car model"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-contact-edit-group"
            label="Contact:"
            label-for="form-contact-edit-input"
          >
            <b-form-input
              id="form-contact-edit-input"
              type="text"
              v-model="editForm.contact"
              required
              placeholder="Enter contact details"
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
import AddClients from "./AddClients.vue";
export default {
  components: { AddClients },
  data() {
    return {
      clients: [],
      editForm: {
        id: "",
        name: "",
        car_brand: "",
        car_model: "",
        contact: "",
      },
      message: "",
      showMessage: false,
      modalShow: false,
    };
  },
  methods: {
    initForm() {
      this.editForm.id = "";
      this.editForm.name = "";
      this.editForm.car_brand = "";
      this.editForm.car_model = "";
      this.editForm.contact = "";
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

    afterSubmit(message) {
      this.message = message;
      this.showMessage = true;
      this.getClients();
      setTimeout(() => {
        this.showMessage = false;
      }, 4000);
    },

    updateClient(payload, clientID) {
      const path = `http://localhost:5000/clients/${clientID}`;
      axios
        .put(path, payload)
        .then((res) => {
          this.getClients();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getClients();
        });
    },

    editClient(client) {
      this.editForm = client;
    },

    onSubmitUpdate(e) {
      e.preventDefault();
      const payload = {
        name: this.editForm.name,
        car_brand: this.editForm.car_brand,
        car_model: this.editForm.car_model,
        contact: this.editForm.contact,
      };
      this.updateClient(payload, this.editForm.id);
      this.modalShow = !this.modalShow;
    },

    removeClient(ClientID) {
      const path = `http://localhost:5000/clients/${ClientID}`;
      axios
        .delete(path)
        .then((res) => {
          this.getClients();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getClients();
        });
    },

    deleteClient(client) {
      this.removeClient(client.id);
    },
  },
  created() {
    this.getClients();
  },
};
</script>
