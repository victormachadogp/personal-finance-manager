<template>
    <div class="flex gap-6 self-start">
        <button>
            <ArrowLeft />
        </button>
        <h2 class="font-medium">{{ currentMonth }}</h2>
        <button>
            <ArrowRight />
        </button>
    </div>
</template>

<script setup lang="ts">
import ArrowLeft from './icons/ArrowLeft.vue'
import ArrowRight from './icons/ArrowRight.vue'

const currentMonth = new Date().toLocaleString('default', { month: 'long', year: 'numeric' })

</script>

<style scoped>

</style>