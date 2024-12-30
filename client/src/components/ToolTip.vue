<template>
  <Teleport to="body">
    <div 
      v-if="isVisible" 
      class="fixed z-50 bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-normal max-w-xs"
      :style="tooltipStyle"
    >
      {{ text }}
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const isVisible = ref(false)
const text = ref('')
const position = ref({ x: 0, y: 0 })

const tooltipStyle = computed(() => ({
  left: `${position.value.x}px`,
  top: `${position.value.y}px`
}))

const show = (newText: string, element: HTMLElement) => {
  const rect = element.getBoundingClientRect()
  text.value = newText
  position.value = {
    x: rect.left,
    y: rect.top - 30
  }
  isVisible.value = true
}

const hide = () => {
  isVisible.value = false
}

defineExpose({ show, hide })
</script>