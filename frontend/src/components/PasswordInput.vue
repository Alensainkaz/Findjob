<script setup>
import { ref } from 'vue'
import AppIcon from './AppIcon.vue'
import { t } from '../i18n'

const model = defineModel({ type: String, default: '' })
defineProps({ id: String, name: String, autocomplete: String, invalid: Boolean, describedBy: String })
defineEmits(['blur'])
const visible = ref(false)
</script>

<template>
  <div class="input-wrap">
    <input
      :id="id" v-model="model" :name="name" :type="visible ? 'text' : 'password'"
      class="input" :class="{ 'input--invalid': invalid }" :autocomplete="autocomplete"
      :aria-invalid="invalid" :aria-describedby="describedBy" @blur="$emit('blur')"
    >
    <button type="button" class="input-wrap__toggle" :aria-label="visible ? t('Hide password') : t('Show password')" @click="visible = !visible">
      <AppIcon :name="visible ? 'eye-off' : 'eye'" />
    </button>
  </div>
</template>
