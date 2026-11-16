<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { email, helpers, maxLength, minLength, required, sameAs } from '@vuelidate/validators'
import FormField from './FormField.vue'
import PasswordInput from './PasswordInput.vue'
import AppSpinner from './AppSpinner.vue'
import { csrfToken, getJSON } from '../composables/api'
import { fieldErrors, useServerErrors } from '../composables/useServerErrors'
import { t } from '../i18n'

const props = defineProps({
  initial: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
  checkUrl: { type: String, required: true },
  loginUrl: { type: String, required: true },
})

const state = reactive({
  username: props.initial.username || '',
  email: props.initial.email || '',
  password1: '',
  password2: '',
})
const server = useServerErrors(props.errors, state)
const taken = reactive({ username: false, email: false })
const submitting = ref(false)
const formEl = ref(null)

// Live availability check, debounced per field
const timers = {}
for (const field of ['username', 'email']) {
  watch(() => state[field], (value) => {
    clearTimeout(timers[field])
    taken[field] = false
    if (!value || value.length < 3) return
    timers[field] = setTimeout(async () => {
      try {
        const data = await getJSON(`${props.checkUrl}?${field}=${encodeURIComponent(value)}`)
        taken[field] = Boolean(data[`${field}Taken`])
      } catch { /* the server re-validates anyway */ }
    }, 400)
  })
}

const rules = computed(() => ({
  username: {
    required: helpers.withMessage(t('Choose a username'), required),
    minLength: helpers.withMessage(t('At least 3 characters'), minLength(3)),
    maxLength: helpers.withMessage(t('At most 150 characters'), maxLength(150)),
    allowed: helpers.withMessage(t('Use letters, digits and @ . + - _ only'), helpers.regex(/^[\w.@+-]+$/)),
    free: helpers.withMessage(t('This username is taken'), () => !taken.username),
  },
  email: {
    required: helpers.withMessage(t('Enter your email'), required),
    email: helpers.withMessage(t('This doesn’t look like an email'), email),
    free: helpers.withMessage(t('An account with this email already exists'), () => !taken.email),
  },
  password1: {
    required: helpers.withMessage(t('Create a password'), required),
    minLength: helpers.withMessage(t('At least 8 characters'), minLength(8)),
    notNumeric: helpers.withMessage(t('Can’t be only numbers'), (v) => !/^\d+$/.test(v)),
  },
  password2: {
    required: helpers.withMessage(t('Repeat the password'), required),
    sameAs: helpers.withMessage(t('Passwords don’t match'), sameAs(state.password1)),
  },
}))
const v$ = useVuelidate(rules, state)

const strength = computed(() => {
  const p = state.password1
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[a-z]/.test(p) && /[A-Z]/.test(p)) score++
  if (/\d/.test(p) && /[^\w]/.test(p)) score++
  return Math.max(1, score)
})
const strengthLabel = computed(() => ['', t('Weak'), t('Fair'), t('Good'), t('Strong')][strength.value])

const errorsFor = (name) => fieldErrors(v$.value, server, name)

async function onSubmit() {
  if (!(await v$.value.$validate())) return
  submitting.value = true
  formEl.value.submit()
}
</script>

<template>
  <form ref="formEl" method="post" class="form" novalidate @submit.prevent="onSubmit">
    <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken()">
    <p v-if="server.__all__" class="form__alert" role="alert">{{ server.__all__[0] }}</p>

    <FormField id="reg-username" :label="t('Username')" :errors="errorsFor('username')">
      <template #default="{ invalid, describedBy }">
        <input id="reg-username" v-model.trim="state.username" name="username" class="input" :class="{ 'input--invalid': invalid }"
               autocomplete="username" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.username.$touch()">
      </template>
    </FormField>

    <FormField id="reg-email" :label="t('Email')" :errors="errorsFor('email')" :hint="t('We’ll send a 6-digit code to confirm it.')">
      <template #default="{ invalid, describedBy }">
        <input id="reg-email" v-model.trim="state.email" name="email" type="email" class="input" :class="{ 'input--invalid': invalid }"
               autocomplete="email" inputmode="email" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.email.$touch()">
      </template>
    </FormField>

    <FormField id="reg-password1" :label="t('Password')" :errors="errorsFor('password1')">
      <template #default="{ invalid, describedBy }">
        <PasswordInput id="reg-password1" v-model="state.password1" name="password1" autocomplete="new-password"
                       :invalid="invalid" :described-by="describedBy" @blur="v$.password1.$touch()" />
        <div v-if="state.password1" class="strength" :data-level="strength">
          <span v-for="n in 4" :key="n" class="strength__bar" :class="{ 'is-on': n <= strength }" />
          <span class="strength__label">{{ strengthLabel }}</span>
        </div>
      </template>
    </FormField>

    <FormField id="reg-password2" :label="t('Repeat password')" :errors="errorsFor('password2')">
      <template #default="{ invalid, describedBy }">
        <PasswordInput id="reg-password2" v-model="state.password2" name="password2" autocomplete="new-password"
                       :invalid="invalid" :described-by="describedBy" @blur="v$.password2.$touch()" />
      </template>
    </FormField>

    <button type="submit" class="btn btn--primary btn--block" :disabled="submitting">
      <AppSpinner v-if="submitting" />
      {{ submitting ? t('Creating account…') : t('Create account') }}
    </button>
    <p class="form__switch">{{ t('Already have an account?') }} <a :href="loginUrl">{{ t('Log in') }}</a></p>
  </form>
</template>
