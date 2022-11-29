<template>
  <br />
  <br />
  <h1>Error 404</h1>
  <h3>Page not found</h3>
  <p>
    Unfortunately, this page does not exist.
    <br />
    Use the navigation or the button below to return to the home page.
  </p>
  <router-link :to="{ name: 'Home' }" class="btn btn-secondary"
    >Home page</router-link
  >
</template>
