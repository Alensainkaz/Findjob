export function csrfToken() {
  return document.querySelector('meta[name="csrf-token"]')?.content || ''
}

async function request(url, options = {}) {
  const response = await fetch(url, {
    credentials: 'same-origin',
    ...options,
    headers: {
      Accept: 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
      ...(options.method && options.method !== 'GET' ? { 'X-CSRFToken': csrfToken() } : {}),
      ...options.headers,
    },
  })
  let data = {}
  try { data = await response.json() } catch { /* empty body */ }
  if (!response.ok) {
    const error = new Error(data.error || `Request failed (${response.status})`)
    error.status = response.status
    error.data = data
    throw error
  }
  return data
}

export const getJSON = (url, { signal } = {}) => request(url, { signal })
export const postJSON = (url) => request(url, { method: 'POST' })

export function toast(text, level = 'info') {
  window.dispatchEvent(new CustomEvent('fj:toast', { detail: { text, level } }))
}
