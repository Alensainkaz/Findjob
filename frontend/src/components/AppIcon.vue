<script setup>
// Uses the inline SVG sprite rendered once in base.html (templates/partials/icons.html).
defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: 18 },
})
</script>

<template>
  <svg class="icon" :width="size" :height="size" aria-hidden="true" focusable="false">
    <use :href="`#i-${name}`" />
  </svg>
</template>
