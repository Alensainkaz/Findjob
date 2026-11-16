<script setup>
import { reactive, ref } from 'vue'
import AppIcon from './AppIcon.vue'
import AppSpinner from './AppSpinner.vue'
import { postJSON, toast } from '../composables/api'
import { t } from '../i18n'

const props = defineProps({
  items: { type: Array, default: () => [] },
  browseUrl: { type: String, default: '/' },
})
const items = ref(props.items)
const pending = reactive(new Set())

async function remove(item) {
  pending.add(item.id)
  try {
    await postJSON(item.removeUrl)
    items.value = items.value.filter(i => i.id !== item.id)
    toast(t('{name} removed from saved', { name: item.name }), 'success')
  } catch {
    toast(t('Could not remove it. Try again.'), 'error')
  } finally {
    pending.delete(item.id)
  }
}
</script>

<template>
  <div v-if="!items.length" class="empty">
    <AppIcon name="bookmark" :size="28" />
    <h2 class="empty__title">{{ t('Nothing saved yet') }}</h2>
    <p class="empty__text">{{ t('Save resumes from the board to compare candidates here.') }}</p>
    <a :href="browseUrl" class="btn btn--primary">{{ t('Browse resumes') }} <AppIcon name="arrow-right" :size="16" /></a>
  </div>
  <TransitionGroup v-else tag="div" name="list" class="board__list">
    <article v-for="item in items" :key="item.id" class="resume-row">
      <a :href="item.url" class="resume-row__avatar" tabindex="-1" aria-hidden="true">
        <img v-if="item.image" :src="item.image" alt="" loading="lazy" class="is-loaded">
        <span v-else class="avatar-initials">{{ (item.name[0] || '') + (item.surname[0] || '') }}</span>
      </a>
      <div class="resume-row__body">
        <h3 class="resume-row__name"><a :href="item.url">{{ item.name }} {{ item.surname }}</a></h3>
        <p class="chip">{{ item.speciality }}</p>
        <p class="resume-row__meta"><a :href="`mailto:${item.email}`"><AppIcon name="mail" :size="15" />{{ item.email }}</a></p>
      </div>
      <div class="resume-row__actions">
        <button type="button" class="btn btn--small btn--ghost btn--danger-text" :disabled="pending.has(item.id)" @click="remove(item)">
          <AppSpinner v-if="pending.has(item.id)" :size="14" />
          <AppIcon v-else name="x" :size="16" /> {{ t('Remove') }}
        </button>
      </div>
    </article>
  </TransitionGroup>
</template>
