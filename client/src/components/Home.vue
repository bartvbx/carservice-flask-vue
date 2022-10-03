<template>
  <br />
  <br />
  <br />
  <br />
  <b-container class="bv-example-row">
    <b-row>
      <b-col
        ><div>
          <b-card title="Części" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              Wyświetl, dodaj, aktualizuj i usuwaj części.
            </b-card-text>

            <router-link :to="{ name: 'Parts' }" class="btn btn-success"
              >Części</router-link
            >
          </b-card>
        </div></b-col
      >
      <b-col
        ><div>
          <b-card title="Usługi" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              Wyświetl, dodaj, aktualizuj i usuwaj usługi.
            </b-card-text>

            <router-link :to="{ name: 'Services' }" class="btn btn-success"
              >Usługi</router-link
            >
          </b-card>
        </div></b-col
      >
      <div class="w-100"><br /></div>
      <b-col
        ><div>
          <b-card title="Klienci" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              Wyświetl, dodaj, aktualizuj i usuwaj klienów.
            </b-card-text>

            <router-link :to="{ name: 'Clients' }" class="btn btn-success"
              >Klienci</router-link
            >
          </b-card>
        </div></b-col
      >
      <b-col
        ><div>
          <b-card title="Wizyty" style="max-width: 40rem" class="mb-2">
            <b-card-text>
              Wyświetl, dodaj, aktualizuj i usuwaj wizyty.
            </b-card-text>

            <router-link :to="{ name: 'Visits' }" class="btn btn-success"
              >Wizyty</router-link
            >
          </b-card>
        </div></b-col
      >
    </b-row>
  </b-container>
</template>
