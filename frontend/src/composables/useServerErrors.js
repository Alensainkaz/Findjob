import { reactive, watch } from 'vue'

/** Server-side Django errors that disappear as soon as the user edits the field. */
export function useServerErrors(initial = {}, state) {
  const errors = reactive({ ...initial })
  for (const key of Object.keys(state)) {
    watch(() => state[key], () => { delete errors[key] })
  }
  return errors
}

/** Vuelidate errors once the field was touched, otherwise server errors. */
export function fieldErrors(v, serverErrors, name, serverName = name) {
  const field = v[name]
  if (field?.$dirty && field.$errors.length) return field.$errors.map(e => e.$message)
  return serverErrors[serverName] || []
}
