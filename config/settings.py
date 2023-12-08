import os
#environ을 기존 import에 추가
import environ
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR는 프로젝트 root 디렉토리를 의미
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True)) #환경변수를 불러올 수 있는 상태로 세팅

#환경변수 파일 읽어오기
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY는 외부에 노출되면 안되므로 .env 파일에 저장
SECRET_KEY = env('SECRET_KEY') #SECEREY_KEY 값 불러오기

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWD_HOSTS는 default로 비어있음
# ALLOWD_HOSTS에는 실제 서비스할 도메인을 넣어야 함
# '*'는 모든 도메인을 허용한다는 의미
# DEBUG가 True일 때는 ALLOWED_HOSTS에 '*'를 넣어도 되지만
# DEBUG가 False일 때는 ALLOWED_HOSTS에 실제 도메인을 넣어야 함
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'pybo.apps.PyboConfig', # pybo 앱 추가
    'common.apps.CommonConfig', # common 앱 추가
    'mapsearch.apps.MapsearchConfig', # mapsearch 앱 추가
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
# MIDDLEWARE는 프로젝트에 사용할 미들웨어를 등록하는 곳
# 미들웨어는 request와 response 사이에서 동작하는 함수
# MIDDLEWARE는 프로젝트가 시작될 때 등록된 순서대로 실행 됨
# MIDDLEWARE에 등록된 미들웨어는 모든 뷰에서 실행 되며 request와 response를 조작할 수 있음
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# ROOT_URLCONF는 프로젝트의 URL들을 모아서 관리하는 곳
# ROOT_URLCONF에 등록된 URL들은 프로젝트가 시작될 때 메모리에 로드됨
# ROOT_URLCONF에는 config/urls.py 파일의 경로를 등록
# config/urls.py 파일은 프로젝트가 생성될 때 자동으로 생성되며 
# 프로젝트에 등록된 앱들의 URL을 모아서 등록하는 곳
ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# sqlite3 데이터베이스를 사용
# 데이터베이스 파일은 BASE_DIR/db.sqlite3에 저장
# 데이터베이스를 변경하려면 DATABASES 설정을 수정하면 됨
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# 언어, 시간대 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'

# USE_I18N, USE_L10N, USE_TZ는 default로 True
# USE_I18N은 다국어 지원을 활성화하는 설정
# USE_L10N은 숫자, 날짜, 시간을 지역화하는 설정
# USE_TZ는 시간대를 활성화하는 설정
# USE_TZ가 True이면 TIME_ZONE 설정에 지정한 시간대를 사용
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL은 static 파일을 참조할 때 사용하는 URL
# STATICFILES_DIRS는 static 파일이 위치한 경로를 지정
# BASE_DIR / 'static'은 config/settings.py 파일의 위치에서 static 디렉터리를 의미
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/'
# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'

CSRF_TRUSTED_ORIGINS = ['https://192.168.56.101'] # CSRF 토큰을 생성할 때 허용할 도메인
