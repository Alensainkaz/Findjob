<script setup>
import { ref } from 'vue'
import AppIcon from './AppIcon.vue'
import AppSpinner from './AppSpinner.vue'
import { postJSON, toast } from '../composables/api'

const props = defineProps({
  saved: Boolean,
  isAuthenticated: Boolean,
  toggleUrl: { type: String, required: true },
  loginUrl: { type: String, required: true },
})
const saved = ref(props.saved)
const pending = ref(false)

async function toggle() {
  if (!props.isAuthenticated) {
    location.href = `${props.loginUrl}?next=${encodeURIComponent(location.pathname)}`
    return
  }
  pending.value = true
  try {
    saved.value = (await postJSON(props.toggleUrl)).saved
    toast(saved.value ? 'Saved for consideration' : 'Removed from saved', 'success')
  } catch {
    toast('Could not update saved resumes. Try again.', 'error')
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <button type="button" class="btn" :class="saved ? 'btn--saved' : 'btn--primary'" :aria-pressed="saved" :disabled="pending" @click="toggle">
    <AppSpinner v-if="pending" />
    <AppIcon v-else :name="saved ? 'bookmark-check' : 'bookmark'" />
    {{ saved ? 'Saved for consideration' : 'Save for consideration' }}
  </button>
</template>
