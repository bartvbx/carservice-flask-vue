<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <hr />
          <p>Visit list</p>
          <hr />
          <br />

          <b-alert variant="success" v-if="showMessage" show>
            {{ message }}
          </b-alert>

          <add-visits @submit="afterSubmit"></add-visits>
          <br />
          <br />

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">State</th>
                <th scope="col">Date</th>
                <th scope="col">Services</th>
                <th scope="col">Client</th>
                <th scope="col">Car</th>
                <th scope="col">Contact</th>
                <th scope="col">Price</th>
                <th scope="col">Additional information</th>
                <th scope="col">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(visit, index) in visits" :key="index">
                <td>
                  <b-form-checkbox
                    id="state-checkbox"
                    v-model="visit.state"
                    name="state-checkbox"
                    @change="changeVisitState(visit)"
                  > 
                  </b-form-checkbox>
                </td>
                <td>{{ formatDate(visit.date) }}</td>
                <td>
                  <text
                    v-for="(visit_services, index) in visit.services"
                    :key="index"
                    >{{ visit_services.name }}
                    <span
                      v-if="
                        index != Object.keys(visit.services).length - 1
                      "
                      >,
                    </span>
                  </text>
                </td>
                <td>{{ visit.client[0].name }}</td>
                <td>
                  {{ visit.client[0].car_brand }} {{ visit.client[0].car_model }}
                </td>
                <td>{{ visit.client[0].contact }}</td>
                <td>{{ visit.final_price }}</td>
                <td>{{ visit.description }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      id="visit-update-modal"
                      @click="
                        editVisit(visit);
                        modalShow = !modalShow;
                      "
                    >
                      Update
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteVisit(visit)"
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
        ref="editVisitModal"
        id="visit-update-modal"
        title="Update visit"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-client-edit-group"
            label="Client:"
            label-for="form-client-edit-input"
          >
            <VueMultiselect
              v-model="editForm.client"
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
            id="form-visit-services-edit-group"
            label="Services:"
            label-for="form-visit-services-edit-input"
          >
            <VueMultiselect
              v-model="editForm.services"
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
            id="form-date-edit-group"
            label="Date:"
            label-for="form-date-edit-input"
          >
            <Datepicker
              v-model="editForm.date"
              format="yyyy-MM-dd HH:mm:ss"
              required
              placeholder="Enter the date"
            ></Datepicker>
          </b-form-group>

          <b-form-group
            id="form-description-edit-group"
            label="Additional information:"
            label-for="form-description-edit-input"
          >
            <b-form-input
              id="form-description-edit-input"
              type="text"
              v-model="editForm.description"
              placeholder="Enter additional information"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-discount-edit-group"
            label="Discount:"
            label-for="form-discount-edit-input"
          >
            <b-form-input
              id="form-discount-edit-input"
              type="number"
              min="0"
              max="100"
              v-model="editForm.discount"
              required
              placeholder="Enter the discount value (%)"
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
import { formatISO9075 } from 'date-fns';
import VueMultiselect from "vue-multiselect";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import AddVisits from "./AddVisits.vue";
import AddClients from "./AddClients.vue";
export default {
  components: { VueMultiselect, Datepicker, AddVisits, AddClients },
  data() {
    return {
      visits: [],
      services: [],
      clients: [],
      editForm: {
        id: "",
        state: "",
        date: "",
        description: "",
        services: [],
        client: "",
        discount: 0,
      },
      message: "",
      showMessage: false,
      modalShow: false,
    };
  },
  methods: {
    getVisits() {
      const path = "http://localhost:5000/visits";
      axios
        .get(path)
        .then((res) => {
          this.visits = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
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

    formatDate(dateString) {
      return formatISO9075(new Date(dateString));
    },

    afterAddingClient() {
      this.getClients();
    },

    afterSubmit(message) {
      this.message = message;
      this.showMessage = true;
      this.getVisits();
      setTimeout(() => {
        this.showMessage = false;
      }, 4000);
    },

    initForm() {
      this.editForm.id = "";
      this.editForm.state = "";
      this.editForm.date = "";
      this.editForm.description = "";
      this.editForm.services = [];
      this.editForm.client = "";
      this.editForm.discount = 0;
    },

    updateVisit(payload, visitID) {
      const path = `http://localhost:5000/visits/${visitID}`;
      axios
        .put(path, payload)
        .then((res) => {
          this.getVisits();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getVisits();
        });
    },

    updateVisitState(visitID) {
      const path = `http://localhost:5000/visits/state/${visitID}`;
      axios
        .put(path)
        .then((res) => {
          this.getVisits();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getVisits();
        });
    },

    changeVisitState(visit) {
      this.updateVisitState(visit.id);
    },

    editVisit(visit) {
      this.editForm = visit;
    },

    onSubmitUpdate(e) {
      e.preventDefault();
      const payload = {
        name: this.editForm.name,
        date: formatISO9075(new Date(this.editForm.date)),
        description: this.editForm.description,
        services: this.editForm.services,
        client: this.editForm.client,
        discount: this.editForm.discount,
      };
      this.updateVisit(payload, this.editForm.id);
      this.modalShow = !this.modalShow;
    },

    removeVisit(VisitID) {
      const path = `http://localhost:5000/visits/${VisitID}`;
      axios
        .delete(path)
        .then((res) => {
          this.getVisits();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getVisits();
        });
    },

    deleteVisit(visit) {
      this.removeVisit(visit.id);
    },
  },
  created() {
    this.getVisits();
    this.getServices();
    this.getClients();
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
