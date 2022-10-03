<template>
  <br />
  <br />
  <h1>Błąd 404</h1>
  <h3>Nie znaleziono strony</h3>
  <p>
    Niestety strona o tym adresie nie istnieje.
    <br />
    Skorzystaj z nawigacji lub użyj przycisku poniżej, aby powrócić na stronę
    główną.
  </p>
  <router-link :to="{ name: 'Home' }" class="btn btn-secondary"
    >Strona główna</router-link
  >
</template>
