<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import AppSpinner from './AppSpinner.vue'
import { csrfToken, postJSON, toast } from '../composables/api'

const props = defineProps({
  email: { type: String, required: true },
  error: { type: String, default: '' },
  resendIn: { type: Number, default: 0 },
  resendUrl: { type: String, required: true },
})

const LENGTH = 6
const digits = ref(Array(LENGTH).fill(''))
const inputs = ref([])
const formEl = ref(null)
const submitting = ref(false)
const error = ref(props.error)
const countdown = ref(props.resendIn)
const resending = ref(false)
let timer

const code = computed(() => digits.value.join(''))

function tick() {
  clearInterval(timer)
  timer = setInterval(() => {
    countdown.value = Math.max(0, countdown.value - 1)
    if (!countdown.value) clearInterval(timer)
  }, 1000)
}

function focusAt(i) {
  nextTick(() => inputs.value[Math.min(Math.max(i, 0), LENGTH - 1)]?.focus())
}

function submitIfComplete() {
  if (code.value.length === LENGTH && !submitting.value) {
    submitting.value = true
    nextTick(() => formEl.value.submit())
  }
}

function onInput(i, e) {
  error.value = ''
  const value = e.target.value.replace(/\D/g, '')
  if (value.length > 1) return fill(value, i)
  digits.value[i] = value
  if (value) focusAt(i + 1)
  submitIfComplete()
}

function fill(value, from = 0) {
  value.slice(0, LENGTH - from).split('').forEach((d, k) => { digits.value[from + k] = d })
  focusAt(Math.min(from + value.length, LENGTH - 1))
  submitIfComplete()
}

function onKeydown(i, e) {
  if (e.key === 'Backspace' && !digits.value[i]) focusAt(i - 1)
  if (e.key === 'ArrowLeft') focusAt(i - 1)
  if (e.key === 'ArrowRight') focusAt(i + 1)
}

function onPaste(e) {
  const value = (e.clipboardData?.getData('text') || '').replace(/\D/g, '')
  if (value) { e.preventDefault(); fill(value) }
}

async function resend() {
  resending.value = true
  try {
    const data = await postJSON(props.resendUrl)
    countdown.value = data.resendIn
    tick()
    digits.value = Array(LENGTH).fill('')
    error.value = ''
    focusAt(0)
    toast('A new code is on its way.', 'success')
  } catch (err) {
    if (err.data?.resendIn) { countdown.value = err.data.resendIn; tick() }
    toast(err.message, 'error')
  } finally {
    resending.value = false
  }
}

onMounted(() => { focusAt(0); if (countdown.value) tick() })
onBeforeUnmount(() => clearInterval(timer))
</script>

<template>
  <form ref="formEl" method="post" class="form" @submit.prevent="submitIfComplete">
    <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken()">
    <input type="hidden" name="code" :value="code">
    <p class="form__lead">We sent a 6-digit code to <strong>{{ email }}</strong>. It expires in 15 minutes.</p>

    <fieldset class="code" :class="{ 'code--invalid': error }" :disabled="submitting">
      <legend class="visually-hidden">Verification code</legend>
      <input
        v-for="(d, i) in digits" :key="i" :ref="(el) => (inputs[i] = el)" :value="d"
        class="code__digit" inputmode="numeric" autocomplete="one-time-code" maxlength="6"
        :aria-label="`Digit ${i + 1}`" @input="onInput(i, $event)" @keydown="onKeydown(i, $event)" @paste="onPaste"
        @focus="$event.target.select()"
      >
    </fieldset>
    <p v-if="error" class="field__error code__error" role="alert">{{ error }}</p>

    <button type="submit" class="btn btn--primary btn--block" :disabled="submitting || code.length < 6">
      <AppSpinner v-if="submitting" />
      {{ submitting ? 'Checking…' : 'Confirm email' }}
    </button>

    <p class="form__switch">
      Didn’t get it?
      <button v-if="!countdown" type="button" class="link-button" :disabled="resending" @click="resend">
        <AppSpinner v-if="resending" :size="14" /> Send a new code
      </button>
      <span v-else class="muted">Send a new code in {{ countdown }} s</span>
    </p>
  </form>
</template>
