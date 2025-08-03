from flask_login import LoginManager
from flask_caching import Cache
from flask_mail import Mail

cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
    })

login_manager = LoginManager()
mail = Mail()
