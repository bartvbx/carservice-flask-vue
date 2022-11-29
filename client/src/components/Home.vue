<template>
  <br />
  <br />
  <br />
  <br />
  <b-container class="bv-example-row">
    <b-row>
      <b-col
        ><div>
          <b-card title="Parts" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              View, add, update and delete parts.
            </b-card-text>

            <router-link :to="{ name: 'Parts' }" class="btn btn-success"
              >Parts</router-link
            >
          </b-card>
        </div></b-col
      >
      <b-col
        ><div>
          <b-card title="Services" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              View, add, update and delete services.
            </b-card-text>

            <router-link :to="{ name: 'Services' }" class="btn btn-success"
              >Services</router-link
            >
          </b-card>
        </div></b-col
      >
      <div class="w-100"><br /></div>
      <b-col
        ><div>
          <b-card title="Clients" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              View, add, update and delete clients.
            </b-card-text>

            <router-link :to="{ name: 'Clients' }" class="btn btn-success"
              >Clients</router-link
            >
          </b-card>
        </div></b-col
      >
      <b-col
        ><div>
          <b-card title="Visits" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              View, add, update and delete visits.
            </b-card-text>

            <router-link :to="{ name: 'Visits' }" class="btn btn-success"
              >Visits</router-link
            >
          </b-card>
        </div></b-col
      >
    </b-row>
  </b-container>
</template>
