<script setup></script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <router-link :to="{ name: 'Home' }" class="navbar-brand"
          >Car Service</router-link
        >
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <router-link :to="{ name: 'Parts' }" class="nav-link active"
              >Parts</router-link
            >
            <router-link :to="{ name: 'Services' }" class="nav-link active"
              >Services</router-link
            >
            <router-link :to="{ name: 'Clients' }" class="nav-link active"
              >Clients</router-link
            >
            <router-link :to="{ name: 'Visits' }" class="nav-link active"
              >Visits</router-link
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
