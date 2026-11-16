// UI strings for the Vue islands. Keys are the English source text; the page
// language comes from <html lang>, which Django sets from the active locale.
// Django-side strings live in locale/<lang>/LC_MESSAGES/django.po.

const messages = {
  ru: {
    // shared
    'Loading': 'Загрузка',
    'Email': 'Email',
    'Password': 'Пароль',
    'Log in': 'Войти',
    'Remove': 'Удалить',
    'Cancel': 'Отмена',
    'Dismiss': 'Закрыть',
    'Enter your email': 'Введите email',
    'This doesn’t look like an email': 'Это не похоже на email',
    'Could not update saved resumes. Try again.': 'Не удалось обновить избранное. Попробуйте ещё раз.',
    'Request failed ({status})': 'Ошибка запроса ({status})',

    // login
    'Enter your password': 'Введите пароль',
    'Logging in…': 'Входим…',
    'New to Findy-Job?': 'Впервые на Findy-Job?',
    'Create an account': 'Создать аккаунт',
    'Hide password': 'Скрыть пароль',
    'Show password': 'Показать пароль',

    // register
    'Username': 'Имя пользователя',
    'Repeat password': 'Повторите пароль',
    'Choose a username': 'Придумайте имя пользователя',
    'At least 3 characters': 'Не короче 3 символов',
    'At most 150 characters': 'Не длиннее 150 символов',
    'Use letters, digits and @ . + - _ only': 'Только буквы, цифры и @ . + - _',
    'This username is taken': 'Это имя уже занято',
    'An account with this email already exists': 'Аккаунт с этим email уже существует',
    'Create a password': 'Придумайте пароль',
    'At least 8 characters': 'Не короче 8 символов',
    'Can’t be only numbers': 'Пароль не может состоять только из цифр',
    'Repeat the password': 'Повторите пароль',
    'Passwords don’t match': 'Пароли не совпадают',
    'Weak': 'Слабый',
    'Fair': 'Средний',
    'Good': 'Хороший',
    'Strong': 'Надёжный',
    'We’ll send a 6-digit code to confirm it.': 'Мы отправим 6-значный код для подтверждения.',
    'Creating account…': 'Создаём аккаунт…',
    'Create account': 'Создать аккаунт',
    'Already have an account?': 'Уже есть аккаунт?',

    // board
    '{name} saved for consideration': '{name} — в избранном',
    '{name} removed from saved': '{name} — убрано из избранного',
    'Search by name or speciality': 'Поиск по имени или специальности',
    'Search resumes': 'Поиск резюме',
    'Filter by speciality': 'Фильтр по специальности',
    'All specialities': 'Все специальности',
    'Filter by city': 'Фильтр по городу',
    'All cities': 'Все города',
    'resumes': { one: '{n} резюме', few: '{n} резюме', many: '{n} резюме', other: '{n} резюме' },
    'Searching…': 'Ищем…',
    'Couldn’t load resumes': 'Не удалось загрузить резюме',
    'Check your connection and try again.': 'Проверьте подключение и попробуйте снова.',
    'Retry': 'Повторить',
    'No resumes match': 'Ничего не найдено',
    'Try another name, or widen the speciality and city filters.': 'Попробуйте другое имя или расширьте фильтры по специальности и городу.',
    'Clear filters': 'Сбросить фильтры',
    'Show more': 'Показать ещё',

    // resume row / save
    'Saved': 'В избранном',
    'Save': 'Сохранить',
    'Edit resume': 'Редактировать резюме',
    'Delete resume': 'Удалить резюме',
    'Saved for consideration': 'В избранном',
    'Save for consideration': 'Добавить в избранное',
    'Removed from saved': 'Убрано из избранного',

    // saved list
    'Could not remove it. Try again.': 'Не удалось удалить. Попробуйте ещё раз.',
    'Nothing saved yet': 'В избранном пока пусто',
    'Save resumes from the board to compare candidates here.': 'Сохраняйте резюме с доски, чтобы сравнивать кандидатов здесь.',
    'Browse resumes': 'Смотреть резюме',

    // resume form
    'Publish resume': 'Опубликовать резюме',
    '{label} is required': 'Заполните поле «{label}»',
    'At most {max} characters': 'Не длиннее {max} символов',
    'First name': 'Имя',
    'Last name': 'Фамилия',
    'Patronymic': 'Отчество',
    'Pick a speciality': 'Выберите специальность',
    'Pick the city you want to work in': 'Выберите город, в котором хотите работать',
    'Education': 'Образование',
    'Experience': 'Опыт работы',
    'Use a JPG, PNG, WebP or GIF image': 'Загрузите изображение JPG, PNG, WebP или GIF',
    'The photo must be under {max} MB': 'Фото должно быть меньше {max} МБ',
    'Photo': 'Фото',
    'Replace photo': 'Заменить фото',
    'Upload photo': 'Загрузить фото',
    'or drop it here · JPG, PNG, WebP · up to {max} MB': 'или перетащите сюда · JPG, PNG, WebP · до {max} МБ',
    'About you': 'О себе',
    'Contact email': 'Контактный email',
    'Work': 'Работа',
    'Speciality': 'Специальность',
    'Filter specialities': 'Найти специальность',
    'Choose a speciality': 'Выберите специальность',
    'City you want to work in': 'Город, в котором хотите работать',
    'Choose a city': 'Выберите город',
    'e.g. KBTU, Computer Science': 'например, КБТУ, информатика',
    'e.g. 3 years, frontend at Kaspi': 'например, 3 года, фронтенд в Kaspi',
    'Saving…': 'Сохраняем…',

    // verify code
    'A new code is on its way.': 'Новый код уже в пути.',
    'We sent a 6-digit code to {email}. It expires in 15 minutes.': 'Мы отправили 6-значный код на {email}. Он действует 15 минут.',
    'Verification code': 'Код подтверждения',
    'Digit {n}': 'Цифра {n}',
    'Checking…': 'Проверяем…',
    'Confirm email': 'Подтвердить email',
    'Didn’t get it?': 'Не пришёл код?',
    'Send a new code': 'Отправить новый код',
    'Send a new code in {s} s': 'Новый код можно запросить через {s} с',
  },

  kk: {
    // shared
    'Loading': 'Жүктелуде',
    'Email': 'Email',
    'Password': 'Құпиясөз',
    'Log in': 'Кіру',
    'Remove': 'Өшіру',
    'Cancel': 'Бас тарту',
    'Dismiss': 'Жабу',
    'Enter your email': 'Email енгізіңіз',
    'This doesn’t look like an email': 'Бұл email-ге ұқсамайды',
    'Could not update saved resumes. Try again.': 'Таңдаулыларды жаңарту мүмкін болмады. Қайталап көріңіз.',
    'Request failed ({status})': 'Сұраныс сәтсіз аяқталды ({status})',

    // login
    'Enter your password': 'Құпиясөзді енгізіңіз',
    'Logging in…': 'Кіріп жатырмыз…',
    'New to Findy-Job?': 'Findy-Job-та алғаш рет пе?',
    'Create an account': 'Аккаунт ашу',
    'Hide password': 'Құпиясөзді жасыру',
    'Show password': 'Құпиясөзді көрсету',

    // register
    'Username': 'Пайдаланушы аты',
    'Repeat password': 'Құпиясөзді қайталаңыз',
    'Choose a username': 'Пайдаланушы атын ойлап табыңыз',
    'At least 3 characters': 'Кемінде 3 таңба',
    'At most 150 characters': 'Ең көбі 150 таңба',
    'Use letters, digits and @ . + - _ only': 'Тек әріптер, сандар және @ . + - _',
    'This username is taken': 'Бұл ат бос емес',
    'An account with this email already exists': 'Бұл email-мен аккаунт бұрыннан бар',
    'Create a password': 'Құпиясөз ойлап табыңыз',
    'At least 8 characters': 'Кемінде 8 таңба',
    'Can’t be only numbers': 'Құпиясөз тек сандардан тұрмауы керек',
    'Repeat the password': 'Құпиясөзді қайталаңыз',
    'Passwords don’t match': 'Құпиясөздер сәйкес келмейді',
    'Weak': 'Әлсіз',
    'Fair': 'Орташа',
    'Good': 'Жақсы',
    'Strong': 'Мықты',
    'We’ll send a 6-digit code to confirm it.': 'Растау үшін 6 таңбалы код жібереміз.',
    'Creating account…': 'Аккаунт ашылуда…',
    'Create account': 'Аккаунт ашу',
    'Already have an account?': 'Аккаунтыңыз бар ма?',

    // board
    '{name} saved for consideration': '{name} таңдаулыларға қосылды',
    '{name} removed from saved': '{name} таңдаулылардан алынды',
    'Search by name or speciality': 'Аты немесе мамандығы бойынша іздеу',
    'Search resumes': 'Түйіндеме іздеу',
    'Filter by speciality': 'Мамандық бойынша сүзу',
    'All specialities': 'Барлық мамандықтар',
    'Filter by city': 'Қала бойынша сүзу',
    'All cities': 'Барлық қалалар',
    'resumes': { one: '{n} түйіндеме', other: '{n} түйіндеме' },
    'Searching…': 'Іздеп жатырмыз…',
    'Couldn’t load resumes': 'Түйіндемелер жүктелмеді',
    'Check your connection and try again.': 'Интернет байланысын тексеріп, қайталап көріңіз.',
    'Retry': 'Қайталау',
    'No resumes match': 'Ештеңе табылмады',
    'Try another name, or widen the speciality and city filters.': 'Басқа атпен іздеңіз немесе мамандық пен қала сүзгілерін кеңейтіңіз.',
    'Clear filters': 'Сүзгілерді тазалау',
    'Show more': 'Тағы көрсету',

    // resume row / save
    'Saved': 'Таңдаулыда',
    'Save': 'Сақтау',
    'Edit resume': 'Түйіндемені өңдеу',
    'Delete resume': 'Түйіндемені өшіру',
    'Saved for consideration': 'Таңдаулыда',
    'Save for consideration': 'Таңдаулыларға қосу',
    'Removed from saved': 'Таңдаулылардан алынды',

    // saved list
    'Could not remove it. Try again.': 'Өшіру мүмкін болмады. Қайталап көріңіз.',
    'Nothing saved yet': 'Таңдаулылар әзірге бос',
    'Save resumes from the board to compare candidates here.': 'Үміткерлерді осында салыстыру үшін тақтадағы түйіндемелерді сақтаңыз.',
    'Browse resumes': 'Түйіндемелерді қарау',

    // resume form
    'Publish resume': 'Түйіндемені жариялау',
    '{label} is required': '«{label}» өрісін толтырыңыз',
    'At most {max} characters': 'Ең көбі {max} таңба',
    'First name': 'Аты',
    'Last name': 'Тегі',
    'Patronymic': 'Әкесінің аты',
    'Pick a speciality': 'Мамандықты таңдаңыз',
    'Pick the city you want to work in': 'Жұмыс істегіңіз келетін қаланы таңдаңыз',
    'Education': 'Білімі',
    'Experience': 'Жұмыс тәжірибесі',
    'Use a JPG, PNG, WebP or GIF image': 'JPG, PNG, WebP немесе GIF суретін жүктеңіз',
    'The photo must be under {max} MB': 'Фото {max} МБ-тан аспауы керек',
    'Photo': 'Фото',
    'Replace photo': 'Фотоны ауыстыру',
    'Upload photo': 'Фото жүктеу',
    'or drop it here · JPG, PNG, WebP · up to {max} MB': 'немесе осында сүйреңіз · JPG, PNG, WebP · {max} МБ-қа дейін',
    'About you': 'Өзіңіз туралы',
    'Contact email': 'Байланыс email-і',
    'Work': 'Жұмыс',
    'Speciality': 'Мамандығы',
    'Filter specialities': 'Мамандықты іздеу',
    'Choose a speciality': 'Мамандықты таңдаңыз',
    'City you want to work in': 'Жұмыс істегіңіз келетін қала',
    'Choose a city': 'Қаланы таңдаңыз',
    'e.g. KBTU, Computer Science': 'мысалы, ҚБТУ, информатика',
    'e.g. 3 years, frontend at Kaspi': 'мысалы, 3 жыл, Kaspi-де фронтенд',
    'Saving…': 'Сақталуда…',

    // verify code
    'A new code is on its way.': 'Жаңа код жіберілді.',
    'We sent a 6-digit code to {email}. It expires in 15 minutes.': '{email} адресіне 6 таңбалы код жібердік. Ол 15 минут жарамды.',
    'Verification code': 'Растау коды',
    'Digit {n}': '{n}-цифр',
    'Checking…': 'Тексеріп жатырмыз…',
    'Confirm email': 'Email-ді растау',
    'Didn’t get it?': 'Код келмеді ме?',
    'Send a new code': 'Жаңа код жіберу',
    'Send a new code in {s} s': 'Жаңа кодты {s} с кейін сұрауға болады',
  },

  en: {
    'resumes': { one: '{n} resume', other: '{n} resumes' },
  },
}

export const lang = (document.documentElement.lang || 'en').slice(0, 2)
const table = messages[lang] || {}
const plurals = new Intl.PluralRules(lang)

function format(text, params) {
  return text.replace(/\{(\w+)\}/g, (m, key) => (key in params ? params[key] : m))
}

/** Translate an English source string, filling {placeholders} from params. */
export function t(key, params = {}) {
  const value = table[key]
  return format(typeof value === 'string' ? value : key, params)
}

/** Plural form of a counted string, e.g. tn('resumes', 3) → "3 резюме". */
export function tn(key, n) {
  const forms = table[key] || messages.en[key] || {}
  return format(forms[plurals.select(n)] || forms.other || key, { n })
}

/** Split a translation around one {placeholder} so markup can go in between. */
export function tSplit(key, placeholder) {
  const [before, after = ''] = t(key, { [placeholder]: '\u0000' }).split('\u0000')
  return [before, after]
}
