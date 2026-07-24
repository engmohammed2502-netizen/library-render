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
    'storages',  # مكتبة django-storages بدل gdstorage
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


# --- Static Files (Whitenoise - محلي على السيرفر، ما بتغير) ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- Backblaze B2 Storage Configuration (S3-Compatible) ---
AWS_ACCESS_KEY_ID = os.environ.get('B2_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('B2_APPLICATION_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.environ.get('B2_ENDPOINT_URL')  # مثال: https://s3.us-west-004.backblazeb2.com
AWS_S3_REGION_NAME = os.environ.get('B2_REGION_NAME')    # مثال: us-west-004

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_QUERYSTRING_AUTH = True       # الملفات Private، فمحتاجين توقيع مؤقت للرابط
AWS_QUERYSTRING_EXPIRE = 3600     # صلاحية رابط الملف لمدة ساعة (عدّل حسب حاجتك)

# تفعيل B2 فقط لو المتغيرات موجودة، وإلا استخدم التخزين المحلي (مفيد أثناء التطوير محلياً)
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME and AWS_S3_ENDPOINT_URL:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# --- Other Settings ---
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
        'https://library-render-8ghy.onrender.com',
        'https://*.onrender.com',
        'http://localhost:80',
    ]

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
