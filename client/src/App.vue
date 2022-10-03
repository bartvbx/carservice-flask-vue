<script setup></script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link :to="{ name: 'Home' }" class="navbar-brand"
          >Auto serwis</router-link
        >
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link :to="{ name: 'Parts' }" class="nav-link active"
              >Części</router-link
            >
            <router-link :to="{ name: 'Services' }" class="nav-link active"
              >Usługi</router-link
            >
            <router-link :to="{ name: 'Clients' }" class="nav-link active"
              >Klienci</router-link
            >
            <router-link :to="{ name: 'Visits' }" class="nav-link active"
              >Wizyty</router-link
            >
          </div>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style>
#app {
  text-align: center;
}
</style>
