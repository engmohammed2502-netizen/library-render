import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-zero-library-project-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gdstorage',  # مكتبة Google Drive
    'library',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

# --- PostgreSQL (Aiven / Production / Local) ---
# سيقرأ تلقائياً DATABASE_URL من متغيرات البيئة في Render
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get(
            'DATABASE_URL',
            f"postgresql://{os.environ.get('DB_USER', 'rsu_user')}:{os.environ.get('DB_PASSWORD', 'rsu_password')}@{os.environ.get('DB_HOST', 'localhost')}:{os.environ.get('DB_PORT', '5432')}/{os.environ.get('DB_NAME', 'rsu_db')}"
        ),
        conn_max_age=600,
        ssl_require=True if os.environ.get('DATABASE_URL') else False
    )
}

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
                'django.template.context_processors.media',
            ],
        },
    },
]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Khartoum'
USE_I18N = True
USE_TZ = True

# --- Static Files ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Media Files (Google Drive Storage) ---
# سيقرأ ملف JSON ومُعرِّف المجلد من متغيرات البيئة
# --- Google Drive Storage Settings ---


google_key_env = os.getenv('GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS')

if google_key_env:
    # تحويل الـ \n النصية لسطر جديد حقيقي مفاهيمي لمكتبة جوجل
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS = google_key_env.replace('\\n', '\n')
    
GOOGLE_DRIVE_STORAGE_MEDIA_ROOT = os.environ.get('GOOGLE_DRIVE_FOLDER_ID')

if GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE_CONTENTS and GOOGLE_DRIVE_STORAGE_MEDIA_ROOT:
    DEFAULT_FILE_STORAGE = 'gdstorage.storage.GoogleDriveStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'library.User'

DATA_UPLOAD_MAX_MEMORY_SIZE = 157286400  # 150 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 157286400  # 150 MB

SESSION_COOKIE_AGE = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# --- CSRF & Security ---
_origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if _origins:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in _origins.split(',')]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://rsu-project.onrender.com',
        'https://*.onrender.com',
        'http://localhost:80',
    ]

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
