import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'apps'))

SECRET_KEY = 'uey!i4x26n!$d-73cs%blri)09#xfud_e361ne2h(#s2uj7)l!'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'df_cart',
    # 'df_goods',
    'df_goods.apps.DfGoodsConfig',  # 使用 AppConfig 加载，确保信号和文档注册
    'df_user',
    'df_order',

    'tinymce',  # 使用富文本编辑框要在settings文件中安装
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.FixedUserMiddleware',
]

ROOT_URLCONF = 'daily_fresh_demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 将media_url上传文件路径注册到模板中
            ],
        },
    },
]

WSGI_APPLICATION = 'daily_fresh_demo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'daily_fresh',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

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

USE_I18N = True

# USE_L10N = True

LANGUAGE_CODE = 'zh-hans'  # 后台管理改为中文

TIME_ZONE = 'Asia/Shanghai'  # 时区改为上海

USE_TZ = False  # 数据库取为国际时间

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
# 设置上传文件的路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')   # 指定根目录

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# 富文本编辑框的使用配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

FIXED_USER_ID = 32

# 配置Elasticsearch
# 注意：ES 8.x 默认启用安全认证，需要配置用户名密码
# 开发环境建议在 elasticsearch.yml 中设置 xpack.security.enabled: false
# 注意：ES 8.x 需要完整的 URL 格式（包含 http:// 或 https://）
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'http://localhost:9200',  # ES 8.x 需要完整的 URL
        # 如果启用了安全认证，取消下面的注释并填写正确的用户名密码
        # 'http_auth': ('elastic', 'your_password'),
        'http_auth': None,  # 无认证模式
        'timeout': 30,
    },
}

INSTALLED_APPS += [
    'django_elasticsearch_dsl',
    # 'django_elasticsearch_dsl_drf',
]