<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'
import AppHeader from './components/layout/AppHeader.vue';
import { playClickSound, playKeystrokeSound, playBackspaceSound } from '@/composables/useUiSounds.ts'

function handleGlobalClick(e: MouseEvent) {
  const target = (e.target as HTMLElement).closest('.btn')
  if (target) playClickSound()
}

function handleGlobalKeydown(e: KeyboardEvent) {
  const target = e.target as HTMLElement
  const isTextInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA'
  if (!isTextInput) return

  if (e.key === 'Backspace') {
    playBackspaceSound()
  } else if (e.key.length === 1) {
    playKeystrokeSound()
  }
}


onMounted(() => {
  document.addEventListener('click', handleGlobalClick)
  document.addEventListener('keydown', handleGlobalKeydown)
})
onUnmounted(() => {
  document.removeEventListener('click', handleGlobalClick)
  document.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<template>
  <AppHeader></AppHeader>
  <main class="container py-4">
    <RouterView />
  </main>
</template>
