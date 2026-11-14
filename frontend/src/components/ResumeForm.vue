<script setup>
import { computed, onBeforeUnmount, reactive, ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { email, helpers, maxLength, required } from '@vuelidate/validators'
import FormField from './FormField.vue'
import AppIcon from './AppIcon.vue'
import AppSpinner from './AppSpinner.vue'
import { csrfToken } from '../composables/api'
import { fieldErrors, useServerErrors } from '../composables/useServerErrors'

const props = defineProps({
  initial: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
  image: { type: String, default: '' },
  specialities: { type: Array, required: true },
  cities: { type: Array, required: true },
  submitLabel: { type: String, default: 'Publish resume' },
  cancelUrl: { type: String, default: '/' },
})

const MAX_MB = 5
const TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']

const state = reactive({
  name: props.initial.name || '',
  surname: props.initial.surname || '',
  father_name: props.initial.father_name || '',
  email: props.initial.email || '',
  speciality: props.initial.speciality || '',
  city: props.initial.city || '',
  education: props.initial.education || '',
  experience: props.initial.experience || '',
  image: null,
})
const server = useServerErrors(props.errors, state)
const preview = ref(props.image)
const dragging = ref(false)
const fileInput = ref(null)
const formEl = ref(null)
const submitting = ref(false)
const specialityFilter = ref('')

const text = (label, max = 100) => ({
  required: helpers.withMessage(`${label} is required`, required),
  maxLength: helpers.withMessage(`At most ${max} characters`, maxLength(max)),
})
const v$ = useVuelidate({
  name: text('First name'),
  surname: text('Last name'),
  father_name: text('Patronymic'),
  email: { ...text('Email'), email: helpers.withMessage('This doesn’t look like an email', email) },
  speciality: { required: helpers.withMessage('Pick a speciality', required) },
  city: { required: helpers.withMessage('Pick the city you want to work in', required) },
  education: text('Education'),
  experience: text('Experience'),
  image: {
    type: helpers.withMessage('Use a JPG, PNG, WebP or GIF image', (f) => !f || TYPES.includes(f.type)),
    size: helpers.withMessage(`The photo must be under ${MAX_MB} MB`, (f) => !f || f.size <= MAX_MB * 1024 * 1024),
  },
}, state)

const filteredSpecialities = computed(() => {
  const q = specialityFilter.value.trim().toLowerCase()
  const list = q ? props.specialities.filter(s => s.label.toLowerCase().includes(q)) : props.specialities
  // keep the current choice visible even when it doesn't match the filter
  const current = props.specialities.find(s => s.value === state.speciality)
  return current && !list.includes(current) ? [current, ...list] : list
})

function setFile(file) {
  state.image = file || null
  v$.value.image.$touch()
  if (preview.value.startsWith('blob:')) URL.revokeObjectURL(preview.value)
  preview.value = file && !v$.value.image.$invalid ? URL.createObjectURL(file) : props.image
}
function onFileChange(e) { setFile(e.target.files[0]) }
function onDrop(e) {
  dragging.value = false
  const file = e.dataTransfer.files[0]
  if (!file) return
  const dt = new DataTransfer()
  dt.items.add(file)
  fileInput.value.files = dt.files
  setFile(file)
}
function clearFile() {
  fileInput.value.value = ''
  setFile(null)
}
onBeforeUnmount(() => { if (preview.value.startsWith('blob:')) URL.revokeObjectURL(preview.value) })

const errorsFor = (name) => fieldErrors(v$.value, server, name)

async function onSubmit() {
  if (!(await v$.value.$validate())) {
    formEl.value.querySelector('[aria-invalid="true"]')?.focus()
    return
  }
  submitting.value = true
  formEl.value.submit()
}

const textFields = [
  { name: 'name', label: 'First name', autocomplete: 'given-name' },
  { name: 'surname', label: 'Last name', autocomplete: 'family-name' },
  { name: 'father_name', label: 'Patronymic', autocomplete: 'additional-name' },
]
</script>

<template>
  <form ref="formEl" method="post" enctype="multipart/form-data" class="form form--wide" novalidate @submit.prevent="onSubmit">
    <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken()">
    <p v-if="server.__all__" class="form__alert" role="alert">{{ server.__all__[0] }}</p>

    <section class="form__section">
      <h2 class="form__section-title">Photo</h2>
      <div
        class="dropzone" :class="{ 'is-dragging': dragging, 'has-image': preview, 'dropzone--invalid': errorsFor('image').length }"
        @dragover.prevent="dragging = true" @dragleave="dragging = false" @drop.prevent="onDrop"
      >
        <img v-if="preview" :src="preview" alt="" class="dropzone__preview">
        <div v-else class="dropzone__placeholder"><AppIcon name="user" :size="28" /></div>
        <div class="dropzone__text">
          <label for="resume-image" class="btn btn--ghost btn--small">
            <AppIcon name="upload" :size="16" /> {{ preview ? 'Replace photo' : 'Upload photo' }}
          </label>
          <button v-if="state.image" type="button" class="link-button" @click="clearFile">Remove</button>
          <p class="field__hint">or drop it here · JPG, PNG, WebP · up to {{ MAX_MB }} MB</p>
          <p v-if="errorsFor('image').length" class="field__error" role="alert">{{ errorsFor('image')[0] }}</p>
        </div>
        <input id="resume-image" ref="fileInput" type="file" name="image" accept="image/*" class="visually-hidden" @change="onFileChange">
      </div>
    </section>

    <section class="form__section">
      <h2 class="form__section-title">About you</h2>
      <div class="form__grid">
        <FormField v-for="f in textFields" :id="`resume-${f.name}`" :key="f.name" :label="f.label" :errors="errorsFor(f.name)">
          <template #default="{ invalid, describedBy }">
            <input :id="`resume-${f.name}`" v-model.trim="state[f.name]" :name="f.name" class="input" :class="{ 'input--invalid': invalid }"
                   :autocomplete="f.autocomplete" maxlength="100" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$[f.name].$touch()">
          </template>
        </FormField>
        <FormField id="resume-email" label="Contact email" :errors="errorsFor('email')">
          <template #default="{ invalid, describedBy }">
            <input id="resume-email" v-model.trim="state.email" name="email" type="email" class="input" :class="{ 'input--invalid': invalid }"
                   autocomplete="email" maxlength="100" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.email.$touch()">
          </template>
        </FormField>
      </div>
    </section>

    <section class="form__section">
      <h2 class="form__section-title">Work</h2>
      <FormField id="resume-speciality" label="Speciality" :errors="errorsFor('speciality')">
        <template #default="{ invalid, describedBy }">
          <div class="combo">
            <div class="input-wrap">
              <AppIcon name="search" class="input-wrap__icon" />
              <input v-model="specialityFilter" type="search" class="input input--with-icon" placeholder="Filter specialities" aria-label="Filter specialities">
            </div>
            <select id="resume-speciality" v-model="state.speciality" name="speciality" class="input select" :class="{ 'input--invalid': invalid }"
                    :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.speciality.$touch()">
              <option value="" disabled>Choose a speciality</option>
              <option v-for="s in filteredSpecialities" :key="s.value" :value="s.value">{{ s.label }}</option>
            </select>
          </div>
        </template>
      </FormField>
      <FormField id="resume-city" label="City you want to work in" :errors="errorsFor('city')">
        <template #default="{ invalid, describedBy }">
          <select id="resume-city" v-model="state.city" name="city" class="input select" :class="{ 'input--invalid': invalid }"
                  :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.city.$touch()">
            <option value="" disabled>Choose a city</option>
            <optgroup v-for="g in cities" :key="g.region" :label="g.region">
              <option v-for="c in g.cities" :key="c.value" :value="c.value">{{ c.label }}</option>
            </optgroup>
          </select>
        </template>
      </FormField>
      <div class="form__grid">
        <FormField id="resume-education" label="Education" :errors="errorsFor('education')" :hint="`${state.education.length}/100`">
          <template #default="{ invalid, describedBy }">
            <input id="resume-education" v-model.trim="state.education" name="education" class="input" :class="{ 'input--invalid': invalid }"
                   maxlength="100" placeholder="e.g. KBTU, Computer Science" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.education.$touch()">
          </template>
        </FormField>
        <FormField id="resume-experience" label="Experience" :errors="errorsFor('experience')" :hint="`${state.experience.length}/100`">
          <template #default="{ invalid, describedBy }">
            <input id="resume-experience" v-model.trim="state.experience" name="experience" class="input" :class="{ 'input--invalid': invalid }"
                   maxlength="100" placeholder="e.g. 3 years, frontend at Kaspi" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.experience.$touch()">
          </template>
        </FormField>
      </div>
    </section>

    <div class="form__actions">
      <a :href="cancelUrl" class="btn btn--ghost">Cancel</a>
      <button type="submit" class="btn btn--primary" :disabled="submitting">
        <AppSpinner v-if="submitting" />
        {{ submitting ? 'Saving…' : submitLabel }}
      </button>
    </div>
  </form>
</template>
