<script setup>
import { computed, ref } from 'vue'
import AppIcon from './AppIcon.vue'
import AppSpinner from './AppSpinner.vue'

const props = defineProps({
  resume: { type: Object, required: true },
  pending: { type: Boolean, default: false },
})
defineEmits(['toggle-save'])

const loaded = ref(false)
const failed = ref(false)
const initials = computed(() => `${props.resume.name[0] || ''}${props.resume.surname[0] || ''}`.toUpperCase())
</script>

<template>
  <article class="resume-row">
    <a :href="resume.url" class="resume-row__avatar" tabindex="-1" aria-hidden="true">
      <template v-if="resume.image && !failed">
        <span v-if="!loaded" class="skeleton skeleton--avatar" />
        <img :src="resume.image" alt="" loading="lazy" :class="{ 'is-loaded': loaded }" @load="loaded = true" @error="failed = true">
      </template>
      <span v-else class="avatar-initials">{{ initials }}</span>
    </a>

    <div class="resume-row__body">
      <h3 class="resume-row__name">
        <a :href="resume.url">{{ resume.name }} {{ resume.surname }} <span class="muted">{{ resume.fatherName }}</span></a>
      </h3>
      <p class="chip">{{ resume.speciality }}</p>
      <p class="resume-row__meta">
        <span v-if="resume.city"><AppIcon name="pin" :size="15" />{{ resume.city }}</span>
        <span><AppIcon name="cap" :size="15" />{{ resume.education }}</span>
        <span><AppIcon name="briefcase" :size="15" />{{ resume.experience }}</span>
      </p>
    </div>

    <div class="resume-row__actions">
      <button
        type="button" class="btn btn--small" :class="resume.saved ? 'btn--saved' : 'btn--ghost'"
        :aria-pressed="resume.saved" :disabled="pending" @click="$emit('toggle-save', resume)"
      >
        <AppSpinner v-if="pending" :size="14" />
        <AppIcon v-else :name="resume.saved ? 'bookmark-check' : 'bookmark'" :size="16" />
        {{ resume.saved ? 'Saved' : 'Save' }}
      </button>
      <a v-if="resume.editUrl" :href="resume.editUrl" class="icon-button" aria-label="Edit resume"><AppIcon name="pencil" :size="16" /></a>
      <a v-if="resume.deleteUrl" :href="resume.deleteUrl" class="icon-button icon-button--danger" aria-label="Delete resume"><AppIcon name="trash" :size="16" /></a>
    </div>
  </article>
</template>
