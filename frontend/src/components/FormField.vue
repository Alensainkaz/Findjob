<script setup>
import AppIcon from './AppIcon.vue'

defineProps({
  id: { type: String, required: true },
  label: { type: String, required: true },
  errors: { type: Array, default: () => [] },
  hint: { type: String, default: '' },
})
</script>

<template>
  <div class="field" :class="{ 'field--invalid': errors.length }">
    <label class="field__label" :for="id">{{ label }}</label>
    <slot :invalid="errors.length > 0" :described-by="errors.length ? `${id}-error` : hint ? `${id}-hint` : undefined" />
    <p v-if="errors.length" :id="`${id}-error`" class="field__error" role="alert">
      <AppIcon name="alert" :size="14" />{{ errors[0] }}
    </p>
    <p v-else-if="hint" :id="`${id}-hint`" class="field__hint">{{ hint }}</p>
  </div>
</template>
