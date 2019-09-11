<template>
  <b-container fluid id="app">
    <b-row class='navbar-bottom-padding'>
      <b-col>
        <Navbar/>
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <router-view/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'app',
  components: {
    Navbar
  },
};
</script>

<style>
.navbar-bottom-padding {
  margin-bottom: 25px;
}
</style>