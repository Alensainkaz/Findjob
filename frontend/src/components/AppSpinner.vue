<script setup>
import { t } from '../i18n'
defineProps({ size: { type: Number, default: 16 }, label: { type: String, default: () => t('Loading') } })
</script>

<template>
  <svg class="spinner" :width="size" :height="size" viewBox="0 0 24 24" role="status" :aria-label="label">
    <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.5" opacity=".25" />
    <path d="M21 12a9 9 0 0 0-9-9" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
  </svg>
</template>
