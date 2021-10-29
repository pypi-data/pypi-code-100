# # !/usr/bin/env python3
# # -*- coding: UTF-8 -*-
#
# """Django settings
#
# For more information on this file, see
# https://api_docs.djangoproject.com/en/3.0/topics/settings/
#
# For the full list of settings and their values, see
# https://api_docs.djangoproject.com/en/3.0/ref/settings/
# """
#
# import os
# from warnings import warn
#
# import environ
# import pymysql
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# pymysql.version_info = (9, 9, 99, "final", 0)  # https://stackoverflow.com/a/59591269
# pymysql.install_as_MySQLdb()
# env = environ.Env()
#
# # Read environment settings from file only if we are not deployed to App Engine
# running_in_app_engine = os.getenv('GAE_APPLICATION', False)
# if not running_in_app_engine:
#     environ.Env.read_env(os.path.join(os.path.dirname(BASE_DIR), '.env'))
#
# # SECURITY WARNING: Make sure the following settings are properly configured in production
# # App Engine's security features ensure that it is safe to
# # have ALLOWED_HOSTS = ['*'] when the app is deployed. If you deploy a Django
# # app not on App Engine, make sure to set an appropriate host here.
# # See https://docs.djangoproject.com/en/1.10/ref/settings/
# ###############################################################################
# SECRET_KEY = env.str('SECRET_KEY')
# DEBUG = env.bool('DEBUG', default=False)
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# CONTACT_EMAILS = env.list('CONTACT_EMAILS', default=[])
# RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY', default='')
# RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY', default='')
# ZTF_ALERTS_TABLE_NAME = env.str('ZTF_ALERTS_TABLE_NAME', default='ardent-cycling-243415.ztf_alerts.alerts')
# ZTF_SALT2_TABLE_NAME = env.str('ZTF_SALT2_TABLE_NAME', default='ardent-cycling-243415.ztf_alerts.salt2')
# ZTF_SALT2_IMAGE_BUCKET = env.str('ZTF_SALT2_TABLE_NAME', default='ardent-cycling-243415_ztf-sncosmo')
# NOCAPTCHA = True
# ###############################################################################
#
# if not (RECAPTCHA_PUBLIC_KEY or RECAPTCHA_PRIVATE_KEY):
#     warn('Recaptcha keys not set in environment. '
#          'Recaptcha verification may not work correctly')
#
# INSTALLED_APPS = [
#     'django.contrib.admin',  # Django administration interface
#     'django.contrib.auth',  # Core authentication framework and associated models
#     'django.contrib.contenttypes',  # Allows permissions to be associated with models
#     'django.contrib.sessions',  # Session framework for cookies handling
#     'django.contrib.messages',  # Displays one-time notification messages
#     'django.contrib.staticfiles',  # Renders paths to static files
#     'django.contrib.sites',  # Handles multi-site hosting on multiple domains
#     'django_extensions',  # Extends capability of django management commands
#     'guardian',  # Extra authentication backend with per object permissions
#     'bootstrap4',  # Front-end component library for building templates
#     'crispy_forms',  # Makes forms look pretty
#     'captcha',  # Implements Google recaptcha service
#
#     # Custom apps
#     'broker_web.apps.alerts',  # Displays alert information
#     'broker_web.apps.contact',  # Adds a "contact Us" form
#     'broker_web.apps.getting_started',  # Handles the getting started guide
#     'broker_web.apps.objects',  # Displays object information
#     'broker_web.apps.signup',  # Handles user creation / authentication
#     'broker_web.apps.subscriptions',  # Handles alert topic subscriptions
#     'broker_web.apps.utils',  # Handles alert topic subscriptions
# ]
#
# # App configuration
# CRISPY_TEMPLATE_PACK = 'bootstrap4'
#
# # Site configuration
# ROOT_URLCONF = 'broker_web.main.urls'
# SITE_ID = 1  # For description, see https://stackoverflow.com/a/25468782/6466457
# LOGIN_REDIRECT_URL = '/'
# LOGIN_URL = '/users/login/'
# AUTH_USER_MODEL = 'signup.CustomUser'  # Use custom user model for authentication
#
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware'
# ]
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# # Database connection settings
# default_db_name = 'web_backend'
# if running_in_app_engine:
#     # Running on production App Engine, so connect to Google Cloud SQL using
#     # the unix socket at /cloudsql/<your-cloudsql-connection string>
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'HOST': '/cloudsql/ardent-cycling-243415:us-east1:broker-web',
#             'USER': env.str('DB_USER'),
#             'PASSWORD': env.str('DB_PASSWORD'),
#             'NAME': env.str('DB_NAME', default_db_name),
#         }
#     }
#
# elif os.getenv('GAE_REMOTE', False):
#     # Running locally, but connect to Cloud SQL via the proxy.
#     # To start the proxy see https://cloud.google.com/sql/docs/mysql-connect-proxy
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'HOST': '127.0.0.1',
#             'PORT': '3306',
#             'USER': env.str('DB_USER'),
#             'PASSWORD': env.str('DB_PASSWORD'),
#             'NAME': env.str('DB_NAME', default_db_name),
#             'TEST_NAME': f'test_{env.str("DB_NAME", default_db_name)}'
#         }
#     }
#
# else:
#     # Running against a local db
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': env.str('DB_NAME', default_db_name),
#             'USER': env.str('DB_USER'),
#             'PASSWORD': env.str('DB_PASSWORD'),
#             'HOST': env.str('DB_HOST', ''),
#             'PORT': env.str('DB_PORT', ''),
#             'TEST_NAME': f'test_{env.str("DB_NAME", default_db_name)}'
#         }
#     }
#
# # Password validation
# # https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]
#
# # Authentication configuration
# AUTHENTICATION_BACKENDS = (
#     'django.contrib.auth.backends.ModelBackend',
#     'guardian.backends.ObjectPermissionBackend',
# )
#
# # Internationalization
# # https://docs.djangoproject.com/en/3.0/topics/i18n/
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = False
# USE_TZ = True
# DATETIME_FORMAT = 'Y-m-d H:m:s'
# DATE_FORMAT = 'Y-m-d'
#
# # Static files (CSS, JavaScript, Images, etc.)
# # https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# if running_in_app_engine:
#     STATIC_URL = 'https://storage.googleapis.com/broker-web-static/static/'
#
# else:
#     STATIC_URL = '/static/'
