<template>
  <div class=" ">
  <header class="">

      <nav class="flex justify-center gap-5">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
  
  </header>

  
  <ToolTip ref="tooltipRef" />


  <RouterView />
</div>
</template>

<script setup lang="ts">
import { ref, provide, onMounted } from 'vue'
import { useAccountStore } from './stores/accountStore'
import { RouterLink, RouterView } from 'vue-router'
import ToolTip from './components/ToolTip.vue'

const accountStore = useAccountStore()


const tooltipRef = ref()

provide('showGlobalTooltip', (text: string, element: HTMLElement) => {
  tooltipRef.value?.show(text, element)
})

provide('hideGlobalTooltip', () => {
  tooltipRef.value?.hide()
})

onMounted(async () => {
  await accountStore.fetchAccounts()
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

body {
  font-family: 'Inter', sans-serif;
  color: #000;
  background-color: #EBEDF0;
}

</style>