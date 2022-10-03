<template>
  <div class="jumbotron vertical-center">
    <div class="container">
      <div class="row">
        <div class="col-sm-12">
          <br />
          <hr />
          <p>Lista części</p>
          <hr />
          <br />

          <b-alert variant="success" v-if="showMessage" show dismissible>
            {{ message }}
          </b-alert>

          <add-parts @submit="afterSubmit"></add-parts>
          <br />
          <br />

          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Nazwa</th>
                <th scope="col">Opis</th>
                <th scope="col">Cena</th>
                <th scope="col">Akcje</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(part, index) in parts" :key="index">
                <td>{{ part.name }}</td>
                <td>{{ part.description }}</td>
                <td>{{ part.price }}</td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-info btn-sm"
                      id="part-update-modal"
                      @click="
                        editPart(part);
                        modalShow = !modalShow;
                      "
                    >
                      Aktualizuj
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deletePart(part)"
                    >
                      Usuń
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
        ref="editPartModal"
        id="part-update-modal"
        title="Aktualizuj część"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" class="w-100">
          <b-form-group
            id="form-name-edit-group"
            label="Nazwa:"
            label-for="form-name-edit-input"
          >
            <b-form-input
              id="form-name-edit-input"
              type="text"
              v-model="editForm.name"
              required
              placeholder="Wprowadź nazwę części"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-description-edit-group"
            label="Opis:"
            label-for="form-description-edit-input"
          >
            <b-form-input
              id="form-description-edit-input"
              type="text"
              v-model="editForm.description"
              placeholder="Wprowadź opis części"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-price-edit-group"
            label="Cena:"
            label-for="form-price-edit-input"
          >
            <b-form-input
              id="form-price-edit-input"
              type="number"
              min="0"
              v-model="editForm.price"
              required
              placeholder="Wprowadź cenę części"
            >
            </b-form-input>
          </b-form-group>

          <b-button type="submit" variant="outline-info">Aktualizuj</b-button>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AddParts from "./AddParts.vue";
export default {
  components: { AddParts },
  data() {
    return {
      parts: [],
      editForm: {
        id: "",
        name: "",
        description: "",
        price: "",
      },
      message: "",
      showMessage: false,
      modalShow: false,
    };
  },
  methods: {
    getParts() {
      const path = "http://localhost:5000/parts";
      axios
        .get(path)
        .then((res) => {
          this.parts = res.data.parts;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    afterSubmit(message) {
      this.message = message;
      this.showMessage = true;
      this.getParts();
      setTimeout(() => {
        this.showMessage = false;
      }, 4000);
    },

    initForm() {
      this.editForm.name = "";
      this.editForm.description = "";
      this.editForm.price = "";
    },

    updatePart(payload, partID) {
      const path = `http://localhost:5000/parts/${partID}`;
      axios
        .put(path, payload)
        .then((res) => {
          this.getParts();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getParts();
        });
    },

    editPart(part) {
      this.editForm = part;
    },

    onSubmitUpdate(e) {
      e.preventDefault();
      const payload = {
        name: this.editForm.name,
        description: this.editForm.description,
        price: this.editForm.price,
      };
      this.updatePart(payload, this.editForm.id);
      this.modalShow = !this.modalShow;
    },

    removePart(PartID) {
      const path = `http://localhost:5000/parts/${PartID}`;
      axios
        .delete(path)
        .then((res) => {
          this.getParts();
          this.message = res.data.message;
          this.showMessage = true;
          setTimeout(() => {
            this.showMessage = false;
          }, 4000);
        })
        .catch((error) => {
          console.error(error);
          this.getParts();
        });
    },

    deletePart(part) {
      this.removePart(part.id);
    },
  },
  created() {
    this.getParts();
  },
};
</script>
