from flask import Flask
import FlagEmbedding, logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pandas as pd

from db import close_db
from routes import bp
from extensions import cache, login_manager
from user import register_user_loader
from update import update
from constants import DB_LOCATION


# set up and config code upon startup
def create_app():     
    app = Flask(__name__)
    # login configs
    app.secret_key = "MXt9mp8qaCFg9p8j1eiGI21A$"
    login_manager.init_app(app)
    login_manager.login_view = 'bp.login'
    register_user_loader()
    # cache configs
    cache.init_app(app)
    # database configs
    app.model = FlagEmbedding.BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
    app.db = pd.read_parquet(DB_LOCATION)
    app.teardown_appcontext(close_db)
    # routing registration
    app.register_blueprint(bp)
    # scheduler configs and setup for data pipeline
    logging.basicConfig(level=logging.INFO)
    scheduler = BackgroundScheduler()
    trigger = CronTrigger(day=15, hour=2, minute=0)
    scheduler.add_job(func=lambda: update(app), trigger=trigger)
    scheduler.start()
    
    return app
