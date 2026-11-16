<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import AppIcon from './AppIcon.vue'
import { t } from '../i18n'

const props = defineProps({ messages: { type: Array, default: () => [] } })
const toasts = ref([])
let seq = 0

function push({ text, level = 'info' }) {
  const id = ++seq
  toasts.value.push({ id, text, level })
  setTimeout(() => dismiss(id), 5000)
}
function dismiss(id) {
  toasts.value = toasts.value.filter(t => t.id !== id)
}
const onToast = (e) => push(e.detail)

onMounted(() => {
  props.messages.forEach(push)
  window.addEventListener('fj:toast', onToast)
})
onBeforeUnmount(() => window.removeEventListener('fj:toast', onToast))
</script>

<template>
  <div class="toasts" aria-live="polite">
    <TransitionGroup name="toast">
      <div v-for="t in toasts" :key="t.id" class="toast" :class="`toast--${t.level}`">
        <AppIcon :name="t.level === 'error' ? 'alert' : 'check'" />
        <span>{{ t.text }}</span>
        <button type="button" class="toast__close" :aria-label="t('Dismiss')" @click="dismiss(t.id)">
          <AppIcon name="x" :size="16" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>
