from pathlib import Path
import os
import sys
import logging
import logging.handlers
import yagmail

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-qe$a^it&qp@1i@g@$2=#+6g=^e9cl7=l#yveih!y2&04d5hz+q'
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'log_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'log_app.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Создаем директорию для логов, если она не существует
if not os.path.exists('logs'):
    os.makedirs('logs')

# Формат для консольного вывода
console_format = '%(asctime)s - %(levelname)s - %(message)s'
# Формат для файлового вывода
file_format_general = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
file_format_errors = '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s - %(exc_info)s'
file_format_security = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

# Создаем логгер
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Консольный обработчик
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(console_format))

# Файловый обработчик для general.log
general_handler = logging.FileHandler('logs/general.log')
general_handler.setLevel(logging.INFO)
general_handler.setFormatter(logging.Formatter(file_format_general))

# Файловый обработчик для errors.log
errors_handler = logging.FileHandler('logs/errors.log')
errors_handler.setLevel(logging.ERROR)
errors_handler.setFormatter(logging.Formatter(file_format_errors))

# Файловый обработчик для security.log
security_handler = logging.FileHandler('logs/security.log')
security_handler.setLevel(logging.DEBUG)
security_handler.setFormatter(logging.Formatter(file_format_security))

# Фильтры для логирования
class DebugFilter(logging.Filter):
    def filter(self, record):
        return DEBUG

class ProductionFilter(logging.Filter):
    def filter(self, record):
        return not DEBUG

# Применяем фильтры
console_handler.addFilter(DebugFilter())
general_handler.addFilter(ProductionFilter())

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(general_handler)
logger.addHandler(errors_handler)
logger.addHandler(security_handler)

# Обработчик для отправки почты через Gmail
class EmailHandler(logging.Handler):
    def __init__(self, email, password):
        super().__init__()
        self.yag = yagmail.SMTP(email, password)

    def emit(self, record):
        subject = f"Error Log: {record.levelname}"
        body = self.format(record)
        self.yag.send(to='alisa.krushinina@mail.ru', subject=subject, contents=body)


email_handler = EmailHandler('alisa.xorok@gmail.com', 'Rozachainaia01/')
email_handler.setLevel(logging.ERROR)
email_handler.setFormatter(logging.Formatter(file_format_errors))

# Добавляем обработчик почты
logger.addHandler(email_handler)

# Пример использования логгера
logger.debug('Это отладочное сообщение')
logger.info('Это информационное сообщение')
logger.warning('Это предупреждение')
logger.error('Это сообщение об ошибке', exc_info=True)
logger.critical('Это критическое сообщение', exc_info=True)