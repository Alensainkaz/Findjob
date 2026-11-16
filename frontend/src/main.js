import './styles/app.css'
import { createApp } from 'vue'
import ResumeBoard from './components/ResumeBoard.vue'
import ResumeForm from './components/ResumeForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import LoginForm from './components/LoginForm.vue'
import VerifyCode from './components/VerifyCode.vue'
import SaveButton from './components/SaveButton.vue'
import SavedList from './components/SavedList.vue'
import ToastHost from './components/ToastHost.vue'

const registry = {
  'resume-board': ResumeBoard,
  'resume-form': ResumeForm,
  'register-form': RegisterForm,
  'login-form': LoginForm,
  'verify-code': VerifyCode,
  'save-button': SaveButton,
  'saved-list': SavedList,
  toasts: ToastHost,
}

// Mount every <div data-vue="name" data-props-id="json-script-id"> on the page.
document.querySelectorAll('[data-vue]').forEach((el) => {
  const component = registry[el.dataset.vue]
  if (!component) return
  const source = el.dataset.propsId && document.getElementById(el.dataset.propsId)
  const parsed = source ? JSON.parse(source.textContent) : null
  const props = parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : {}
  el.innerHTML = '' // drop the server-rendered fallback
  createApp(component, props).mount(el)
  el.classList.add('is-mounted')
})

// Mobile navigation: sidebar drawer
const navToggle = document.querySelector('[data-nav-toggle]')
const nav = document.getElementById('site-nav')
const mobileNav = window.matchMedia('(max-width: 860px)')
nav?.querySelectorAll(':scope > a').forEach((a, i) => a.style.setProperty('--i', i))

function setNav(open, { restoreFocus = true } = {}) {
  if (!navToggle || document.body.classList.contains('nav-open') === open) return
  document.body.classList.toggle('nav-open', open)
  navToggle.setAttribute('aria-expanded', String(open))
  if (open) nav.querySelector(':scope > a')?.focus({ preventScroll: true })
  else if (restoreFocus) navToggle.focus({ preventScroll: true })
}
navToggle?.addEventListener('click', () => setNav(!document.body.classList.contains('nav-open')))
document.querySelectorAll('[data-nav-close]').forEach((el) => el.addEventListener('click', () => setNav(false)))
nav?.addEventListener('click', (e) => { if (e.target.closest('a')?.parentElement === nav) setNav(false, { restoreFocus: false }) })
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setNav(false) })
mobileNav.addEventListener('change', (e) => { if (!e.matches) setNav(false, { restoreFocus: false }) })

// Language menu: close on outside click / Escape
const langMenu = document.querySelector('[data-lang-menu]')
document.addEventListener('click', (e) => { if (langMenu?.open && !langMenu.contains(e.target)) langMenu.open = false })
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && langMenu?.open) { langMenu.open = false; langMenu.querySelector('summary').focus() }
})

// Top progress bar for full page navigations (links and plain forms)
const bar = document.querySelector('.page-progress')
function startProgress() { bar?.classList.add('is-active') }
document.addEventListener('click', (e) => {
  const link = e.target.closest('a[href]')
  if (!link || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || link.target === '_blank') return
  const url = new URL(link.href, location.href)
  if (url.origin === location.origin && !link.hasAttribute('download') && url.href.split('#')[0] !== location.href.split('#')[0]) startProgress()
})
document.addEventListener('submit', (e) => { if (!e.defaultPrevented) startProgress() })
// Vue forms submit programmatically, which skips the submit event
const nativeSubmit = HTMLFormElement.prototype.submit
HTMLFormElement.prototype.submit = function submit() { startProgress(); return nativeSubmit.call(this) }
window.addEventListener('pageshow', () => bar?.classList.remove('is-active'))
