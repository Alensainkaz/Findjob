<script setup>
import { reactive, ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { email, helpers, required } from '@vuelidate/validators'
import FormField from './FormField.vue'
import PasswordInput from './PasswordInput.vue'
import AppSpinner from './AppSpinner.vue'
import { csrfToken } from '../composables/api'
import { fieldErrors, useServerErrors } from '../composables/useServerErrors'
import { t } from '../i18n'

const props = defineProps({
  initial: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) },
  registerUrl: { type: String, required: true },
})

const state = reactive({ email: props.initial.email || '', password: '' })
const server = useServerErrors(props.errors, state)
const submitting = ref(false)
const formEl = ref(null)

const v$ = useVuelidate({
  email: {
    required: helpers.withMessage(t('Enter your email'), required),
    email: helpers.withMessage(t('This doesn’t look like an email'), email),
  },
  password: { required: helpers.withMessage(t('Enter your password'), required) },
}, state)

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

    <FormField id="login-email" :label="t('Email')" :errors="fieldErrors(v$, server, 'email')">
      <template #default="{ invalid, describedBy }">
        <input id="login-email" v-model.trim="state.email" name="email" type="email" class="input" :class="{ 'input--invalid': invalid }"
               autocomplete="email" inputmode="email" :aria-invalid="invalid" :aria-describedby="describedBy" @blur="v$.email.$touch()">
      </template>
    </FormField>

    <FormField id="login-password" :label="t('Password')" :errors="fieldErrors(v$, server, 'password')">
      <template #default="{ invalid, describedBy }">
        <PasswordInput id="login-password" v-model="state.password" name="password" autocomplete="current-password"
                       :invalid="invalid" :described-by="describedBy" @blur="v$.password.$touch()" />
      </template>
    </FormField>

    <button type="submit" class="btn btn--primary btn--block" :disabled="submitting">
      <AppSpinner v-if="submitting" />
      {{ submitting ? t('Logging in…') : t('Log in') }}
    </button>
    <p class="form__switch">{{ t('New to Findy-Job?') }} <a :href="registerUrl">{{ t('Create an account') }}</a></p>
  </form>
</template>
