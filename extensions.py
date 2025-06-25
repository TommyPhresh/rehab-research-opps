from flask_login import LoginManager
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
    })

login_manager = LoginManager()

