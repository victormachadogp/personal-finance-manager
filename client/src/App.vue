<template>
  <div class=" sm:w-9/12 lg:w-7/12 xl:w-5/12 mx-auto">
  <header class="">

      <nav class="flex justify-center gap-5">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
  
  </header>


  <RouterView />
</div>
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

body {
  font-family: 'Inter', sans-serif;
  color: #000;
  background-color: #EBEDF0;
}

</style>