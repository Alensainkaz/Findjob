<script setup>
import { onBeforeUnmount, reactive, ref, watch } from 'vue'
import ResumeRow from './ResumeRow.vue'
import SkeletonRow from './SkeletonRow.vue'
import AppIcon from './AppIcon.vue'
import AppSpinner from './AppSpinner.vue'
import { getJSON, postJSON, toast } from '../composables/api'
import { useDebouncedRef } from '../composables/useDebouncedRef'
import { t, tn } from '../i18n'

const props = defineProps({
  results: { type: Array, default: () => [] },
  page: { type: Number, default: 1 },
  hasNext: Boolean,
  total: { type: Number, default: 0 },
  q: { type: String, default: '' },
  speciality: { type: String, default: '' },
  specialities: { type: Array, default: () => [] },
  city: { type: String, default: '' },
  cities: { type: Array, default: () => [] },
  isAuthenticated: Boolean,
  loginUrl: { type: String, required: true },
  apiUrl: { type: String, required: true },
  toggleUrl: { type: String, required: true },
})

const items = ref(props.results)
const total = ref(props.total)
const page = ref(props.page)
const hasNext = ref(props.hasNext)
const query = useDebouncedRef(props.q, 300)
const queryInput = ref(props.q)
const speciality = ref(props.speciality)
const city = ref(props.city)
const loading = ref(false)
const loadingMore = ref(false)
const failed = ref(false)
const pending = reactive(new Set())
let controller

watch(queryInput, (v) => { query.value = v })

function params(p) {
  const search = new URLSearchParams()
  if (query.value.trim()) search.set('q', query.value.trim())
  if (speciality.value) search.set('speciality', speciality.value)
  if (city.value) search.set('city', city.value)
  if (p > 1) search.set('page', p)
  return search
}

async function load(p = 1) {
  controller?.abort()
  const current = (controller = new AbortController())
  const append = p > 1
  append ? (loadingMore.value = true) : (loading.value = true)
  failed.value = false
  try {
    const data = await getJSON(`${props.apiUrl}?${params(p)}`, { signal: current.signal })
    if (append) {
      // Offset pages shift when a resume is published in between; skip ids already shown
      const seen = new Set(items.value.map((r) => r.id))
      items.value = [...items.value, ...data.results.filter((r) => !seen.has(r.id))]
    } else {
      items.value = data.results
    }
    page.value = data.page
    hasNext.value = data.hasNext
    total.value = data.total
    if (!append) {
      const qs = params(1).toString()
      history.replaceState(null, '', qs ? `?${qs}` : location.pathname)
    }
  } catch (err) {
    if (err.name !== 'AbortError') failed.value = true
  } finally {
    // An aborted request settles after its replacement started; leave the newer request's flags alone
    if (controller === current) {
      loading.value = false
      loadingMore.value = false
    }
  }
}

watch([query, speciality, city], () => load(1))
onBeforeUnmount(() => controller?.abort())

async function toggleSave(resume) {
  if (!props.isAuthenticated) {
    location.href = `${props.loginUrl}?next=${encodeURIComponent(location.pathname + location.search)}`
    return
  }
  pending.add(resume.id)
  try {
    const data = await postJSON(props.toggleUrl.replace('/0/', `/${resume.id}/`))
    resume.saved = data.saved
    toast(t(data.saved ? '{name} saved for consideration' : '{name} removed from saved', { name: resume.name }), 'success')
  } catch {
    toast(t('Could not update saved resumes. Try again.'), 'error')
  } finally {
    pending.delete(resume.id)
  }
}

function resetFilters() {
  queryInput.value = ''
  query.value = ''
  speciality.value = ''
  city.value = ''
}
</script>

<template>
  <section class="board">
    <form class="board__filters" role="search" @submit.prevent="load(1)">
      <div class="input-wrap board__search">
        <AppIcon name="search" class="input-wrap__icon" />
        <input v-model="queryInput" type="search" name="q" class="input input--with-icon" :placeholder="t('Search by name or speciality')" :aria-label="t('Search resumes')">
        <AppSpinner v-if="loading" class="input-wrap__spinner" :size="16" />
      </div>
      <select v-model="speciality" name="speciality" class="input select board__select" :aria-label="t('Filter by speciality')">
        <option value="">{{ t('All specialities') }}</option>
        <option v-for="s in specialities" :key="s.value" :value="s.value">{{ s.label }}</option>
      </select>
      <select v-model="city" name="city" class="input select board__select" :aria-label="t('Filter by city')">
        <option value="">{{ t('All cities') }}</option>
        <optgroup v-for="g in cities" :key="g.region" :label="g.region">
          <option v-for="c in g.cities" :key="c.value" :value="c.value">{{ c.label }}</option>
        </optgroup>
      </select>
    </form>

    <p class="board__count" aria-live="polite">
      <template v-if="!loading">{{ tn('resumes', total) }}</template>
      <template v-else>{{ t('Searching…') }}</template>
    </p>

    <div v-if="loading" class="board__list">
      <SkeletonRow v-for="n in 4" :key="n" />
    </div>

    <div v-else-if="failed" class="empty">
      <AppIcon name="alert" :size="28" />
      <h2 class="empty__title">{{ t('Couldn’t load resumes') }}</h2>
      <p class="empty__text">{{ t('Check your connection and try again.') }}</p>
      <button type="button" class="btn btn--ghost" @click="load(1)"><AppIcon name="refresh" :size="16" /> {{ t('Retry') }}</button>
    </div>

    <div v-else-if="!items.length" class="empty">
      <AppIcon name="search" :size="28" />
      <h2 class="empty__title">{{ t('No resumes match') }}</h2>
      <p class="empty__text">{{ t('Try another name, or widen the speciality and city filters.') }}</p>
      <button type="button" class="btn btn--ghost" @click="resetFilters">{{ t('Clear filters') }}</button>
    </div>

    <TransitionGroup v-else tag="div" name="list" class="board__list">
      <ResumeRow v-for="r in items" :key="r.id" :resume="r" :pending="pending.has(r.id)" @toggle-save="toggleSave" />
    </TransitionGroup>

    <div v-if="hasNext && !loading && !failed" class="board__more">
      <template v-if="loadingMore"><SkeletonRow v-for="n in 2" :key="`more-${n}`" /></template>
      <button v-else type="button" class="btn btn--ghost" @click="load(page + 1)">{{ t('Show more') }}</button>
    </div>
  </section>
</template>
