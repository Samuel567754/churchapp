from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"




INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'sweetify',
    'crispy_forms',
    'crispy_tailwind',
    'contact',
    'membership',
    'blog',
    'finance',
    'event',
    'community',
    'worship',
    'account',
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = '/static/'  # Make sure this starts with a slash

# Directory where collectstatic will collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Your app's static files directory
]


# Compression settings
COMPRESS_ENABLED = True
COMPRESS_ROOT = STATIC_ROOT
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',  # Add this line
]


EMAIL_BACKEND =config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')  # Set to False if MAIL_ENCRYPTION is null
EMAIL_USE_SSL = config('EMAIL_USE_SSL')  # Ensure SSL is also disabled if encryption is null
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = '893747a81fe786'
# EMAIL_HOST_PASSWORD = '04a35305d16d78' 
# EMAIL_USE_TLS = False  # Set to False if MAIL_ENCRYPTION is null
# EMAIL_USE_SSL = False  # Ensure SSL is also disabled if encryption is null
# DEFAULT_FROM_EMAIL = 'hello@example.com'

# # this is for gmail
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@gmail.com'  # Replace with your Gmail address
# EMAIL_HOST_PASSWORD = 'your_app_password'  # Replace with the App Password you created above
# DEFAULT_FROM_EMAIL = 'your_email@gmail.com'  # This is optional but recommended

LOGIN_URL = 'login'

OPENAI_API_KEY = config('OPENAI_API_KEY')

# settings.py
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY')


ROOT_URLCONF = 'ChurchApp.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ChurchApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default: database-backed sessions


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'











JAZZMIN_SETTINGS = {
     # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Church Admin",
    
    
     # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Church Admin",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Church Admin",
    
      # Welcome text on the login screen
    "welcome_sign": "Welcome to the Church Admin",
    
    
      # Copyright on the footer
    "copyright": "Amazing Church of Christ 2024",
    
    
    #  # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "books/img/logo.png",

    # # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    # "login_logo": "books/img/loginlogo.png",

    # # Logo to use for login form in dark themes (defaults to login_logo)
    # "login_logo_dark": None,

    # # CSS classes that are applied to the logo above
    # "site_logo_classes": "custom-admin-logo", 
    
    # "custom_css": "css/admin_custom.css",
 
    # # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    # "site_icon": None,
    
    
     # Links to put along the top menu
    "topmenu_links": [
          # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "event"},
        {"app": "finance"},
        {"app": "membership"},
        {"app": "user"},
        {"app": "contact"},
        {"app": "community"},
        {"app": "worship"},
        {"app": "blog"},
        {'name': 'visit site', 'url': 'http://127.0.0.1:8000', 'new_window': True},
    ],
    
    
     # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    # "search_model": ["auth.User", "catalog.Book"],
    
    
     "show_ui_builder": True,
     
     
     
     
      # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        
        "blog.Category": "fas fa-folder",
        "blog.Post": "fas fa-newspaper",
        "blog.Comment": "fas fa-comment",
        "blog.Tag": "fas fa-tags",
        "blog.Like": "fas fa-thumbs-up", 
        
        
        "community.VolunteerOpportunity": "fas fa-handshake", 
        "community.VolunteerApplication": "fas fa-handshake",
        "community.Testimonial": "fas fa-comment",
        "community.fAQ": "fas fa-question",
        "community.Survey": "fas fa-poll",
        "community.SurveyResponse": "fas fa-poll",
        "community.OutreachProgram": "fas fa-handshake",
        "community.Poll": "fas fa-poll",
        "community.PollOption": "fas fa-poll",
        "community.PollVote": "fas fa-poll",
        "community.Announcement": "fas fa-bullhorn",
        "community.CarouselItem": "fas fa-images",
        
        
        "contact.Contact": "fas fa-address-book",
        "contact.Staff": "fas fa-user",
        "contact.Notification": "fas fa-bell",
        "contact.Newsletter": "fas fa-newspaper",
        "contact.NewsletterSubscription": "fas fa-newspaper",
        
        
        "event.Event": "fas fa-calendar",
        "event.EventRegistration": "fas fa-calendar",
        "event.OutreachProgram": "fas fa-handshake",
        "event.ChurchCalendar": "fas fa-calendar",
        "event.GalleryImage": "fas fa-images",
        
        
        "finance.Donation": "fas fa-wallet",
        "finance.Asset": "fas fa-dollar-sign",
  
        "membership.Member": "fas fa-user",
        "membership.MemberDirectory": "fas fa-users",
        "membership.Ministry": "fas fa-user",
        "membership.Attendance": "fas fa-user",
        "membership.Membership": "fas fa-user",
        
        
        "worship.Appointment": "fas fa-calendar",
        "worship.Sermon": "fas fa-bible",
        "worship.SermonSeries": "fas fa-bible",
        "worship.SermonTag": "fas fa-bible",
        "worship.ServiceSchedule": "fas fa-calendar",
        "worship.Schedule": "fas fa-calendar",
        "worship.Resource": "fas fa-bible",
        "worship.PrayerRequest": "fas fa-pray",
        "worship.LiveStream": "fas fa-video",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
     ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "collapsible",
    
    
    # "changeform_format": "horizontal_tabs",
    # # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    
    
    "related_modal_active": True
}






JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "superhero",
    "dark_mode_theme": "superhero",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}


