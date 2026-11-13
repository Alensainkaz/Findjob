import { customRef, onScopeDispose } from 'vue'

/** A ref whose subscribers are notified `delay` ms after the last write. */
export function useDebouncedRef(initial, delay = 300) {
  let timer
  let value = initial
  onScopeDispose(() => clearTimeout(timer))
  return customRef((track, trigger) => ({
    get() { track(); return value },
    set(next) {
      value = next
      clearTimeout(timer)
      timer = setTimeout(trigger, delay)
    },
  }))
}
